import shutil
import tempfile
import unittest
from pathlib import Path

from dronydeliv.cli import main
from dronydeliv.fileio import InputFileError, read_drones, read_orders, validate_pair

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
DRONES = EXAMPLES / "drones10h00_2019y11m5.txt"
PARCELS = EXAMPLES / "parcels10h00_2019y11m5.txt"


class ReadTests(unittest.TestCase):
    def test_reads_example_files(self):
        self.assertEqual(len(read_drones(DRONES)), 4)
        self.assertEqual(len(read_orders(PARCELS)), 6)

    def test_validates_example_pair(self):
        header = validate_pair(DRONES, PARCELS)
        self.assertEqual(header.company, "iQueue")


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def copy(self, source: Path, name: str) -> Path:
        target = self.tmp / name
        shutil.copy(source, target)
        return target

    def test_paths_with_folders_are_accepted(self):
        # The 2019 version sliced the raw argument, so any folder prefix broke it.
        nested = self.tmp / "some" / "folder"
        nested.mkdir(parents=True)
        drones = shutil.copy(DRONES, nested / DRONES.name)
        parcels = shutil.copy(PARCELS, nested / PARCELS.name)
        validate_pair(Path(drones), Path(parcels))

    def test_rejects_name_header_mismatch(self):
        wrong = self.copy(DRONES, "drones11h00_2019y11m5.txt")
        parcels = self.copy(PARCELS, "parcels11h00_2019y11m5.txt")
        with self.assertRaises(InputFileError):
            validate_pair(wrong, parcels)

    def test_rejects_badly_named_file(self):
        bad = self.copy(DRONES, "my_drones.txt")
        with self.assertRaises(InputFileError):
            validate_pair(bad, PARCELS)

    def test_rejects_malformed_record(self):
        broken = self.tmp / DRONES.name
        broken.write_text(DRONES.read_text() + "zulu, Lisbon, 5\n")
        with self.assertRaises(InputFileError):
            read_drones(broken)


class CliTests(unittest.TestCase):
    def test_end_to_end_matches_expected_output(self):
        with tempfile.TemporaryDirectory() as out:
            code = main([str(DRONES), str(PARCELS), "-o", out])
            self.assertEqual(code, 0)
            for name in ("drones10h30_2019y11m5.txt", "timetable10h00_2019y11m5.txt"):
                expected = (EXAMPLES / "expected" / name).read_text()
                self.assertEqual((Path(out) / name).read_text(), expected, name)

    def test_returns_error_code_for_bad_input(self):
        self.assertEqual(main(["missing.txt", str(PARCELS)]), 1)


if __name__ == "__main__":
    unittest.main()
