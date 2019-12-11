# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import constants as c
import organize as o
import readFiles as r
import time_kit as t
import sys


if __name__ == "__main__":
    arg1 = str(sys.argv[1])
    arg2 = str(sys.argv[2])
    fileDict = r.fileFinder(arg1, arg2)

droneList = r.droneLister(fileDict["droneFile"])
parcelList = r.parcelLister(fileDict["parcelFile"])



    