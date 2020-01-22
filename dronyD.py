# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

# Main File: being the main file, this is where the functions written in the helper modules and called and were the program's flow is defined.

import constants as c
import organize as o
import readFiles as r
import time_kit as t
import writeFiles as w
import sys
from pprint import pprint
from copy import deepcopy

if __name__ == "__main__":
    arg1 = str(sys.argv[1])
    arg2 = str(sys.argv[2])
    fileDict = r.fileFinder(arg1, arg2)

droneFile = fileDict["droneFile"]
parcelFile = fileDict["parcelFile"]


r.fileValidater(droneFile, parcelFile)

droneList = r.droneLister(droneFile)
parcelList = r.parcelLister(parcelFile)

# TimetableFileName = w.timetableFileMaker(fileDict)
# w.headerWriter("Timetable", fileDict, TimetableFileName)
# w.timetableWriter(o.droneAssigner(droneList, parcelList), TimetableFileName)

# newDroneFileName = w.droneFileMaker(fileDict)
# w.headerWriter("Drones", fileDict, newDroneFileName)
# w.droneWriter(o.droneAssigner(droneList, parcelList), newDroneFileName)

a = o.droneAssigner(droneList, parcelList)
b = deepcopy(a)

newDroneFileName = w.droneFileMaker(fileDict)
w.headerWriter("Drones", fileDict, newDroneFileName)
w.droneWriter(a, newDroneFileName)


TimetableFileName = w.timetableFileMaker(fileDict)
w.headerWriter("Timetable", fileDict, TimetableFileName)
w.timetableWriter(b, TimetableFileName)
