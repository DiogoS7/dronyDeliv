"""Render docs/social-preview.png from scripts/social_preview.html.

Needs Playwright with Chromium:
    pip install playwright && playwright install chromium
    python scripts/render_social_preview.py

Upload the PNG in the repo's Settings > General > Social preview.
"""

from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "scripts" / "social_preview.html"
OUT = ROOT / "docs" / "social-preview.png"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 640})
        page.goto(SOURCE.as_uri())
        page.evaluate("document.fonts.ready")
        page.screenshot(path=str(OUT))
        browser.close()
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
