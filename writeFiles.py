# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import organize as o
import constants as c
import readFiles as r
import time_kit as t

def droneFileMaker(fileDict):    ############ TEST THIS
    originalFile = fileDict["droneFile"]
    originalFile = open(originalFile, "r")

    day = r.readHeader()[c.headerDay]
    updatedDay = day
    time = r.readHeader()[c.headerTime]

    updatedTime = str(t.time_update(time, 30))

    if t.FileNameTimestampConverter(updatedTime)>t.FileNameTimestampConverter("23h59"):
        updatedDay = t.FileNameDateUpdate(day)


########### IF LEN(DAY)=.... IF LEN(DAY)=...+1 (5/05)
    updatedFile = open("drones{0}h{1}_{2}y{3}m{4}.txt".format(updatedTime[:2], updatedTime[2:4], updatedDay[5:9], updatedDay[2:4], updatedDay[:1]), "w")


