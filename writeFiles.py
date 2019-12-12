# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import organize as o
import constants as c
import readFiles as r
import time_kit as t
import sys ###TESTING
from pprint import pprint ###TESTING
import datetime



def droneFileMaker(fileDict):
    """
    Creates new file and returns it's name
    """

    originalFile = fileDict["droneFile"]

    date = r.readHeader(originalFile)[c.headerDate]
    updatedDate = date
    time = r.readHeader(originalFile)[c.headerTime]
    updatedTime = str(t.FileNameTimeUpdate(time, 30))
    
    if t.FileNameTimestampConverter(updatedTime)>t.FileNameTimestampConverter("23h59"):
        updatedDate = t.FileNameDateUpdate(date)
    
    # simplifying updatedDate
    
    
    if len(date)==9:
        updatedDay = updatedDate[:1]
        updatedYear = updatedDate[5:9]
        updatedMonth = updatedDate[2:4]

    elif len(date)==10:
        updatedDay = updatedDate[:2]
        updatedYear = updatedDate[6:10]
        updatedMonth = updatedDate[3:5]

    updatedFileName = "drones{0}h{1}_{2}y{3}m{4}.txt".format(updatedTime[:2], updatedTime[3:5], updatedYear, updatedMonth, updatedDay)
    
    updatedFile = open(updatedFileName, "w")
    updatedFile.close()
    
    return updatedFileName

def timetableFileMaker(fileDict):
    """
    Creates new file and returns it's name
    """

    originalFile = fileDict["parcelFile"]

    date = r.readHeader(originalFile)[c.headerDate]
    updatedDate = date
    time = r.readHeader(originalFile)[c.headerTime]
    updatedTime = str(t.FileNameTimeUpdate(time, 30))
    
    if t.FileNameTimestampConverter(updatedTime)>t.FileNameTimestampConverter("23h59"):
        updatedDate = t.FileNameDateUpdate(date)
    
    # simplifying updatedDate
    
    
    if len(date)==9:
        updatedDay = updatedDate[:1]
        updatedYear = updatedDate[5:9]
        updatedMonth = updatedDate[2:4]

    elif len(date)==10:
        updatedDay = updatedDate[:2]
        updatedYear = updatedDate[6:10]
        updatedMonth = updatedDate[3:5]

    updatedFileName = "timetable{0}h{1}_{2}y{3}m{4}.txt".format(updatedTime[:2], updatedTime[3:5], updatedYear, updatedMonth, updatedDay)
    
    updatedFile = open(updatedFileName, "w")
    updatedFile.close()
    

    return updatedFileName



def headerWriter(newFileType, fileDict, newFileName):
    """
    new file type "Drones" or "Timetable"
    """

    originalFile = fileDict["droneFile"]
    date = r.readHeader(originalFile)[c.headerDate]
    time = r.readHeader(originalFile)[c.headerTime]
    updatedTime = time
    company = r.readHeader(originalFile)[c.headerCompany]
    if newFileType=="Drones":
        updatedTime = str(t.FileNameTimeUpdate(time, 30))
    
    if t.FileNameTimestampConverter(updatedTime)>t.FileNameTimestampConverter("23h59"):
        updatedDate = t.FileNameDateUpdate(date)
    else:
        updatedDate = date

    newFile = open(newFileName, "a")
    newFile.write("Time:\n")
    newFile.write(updatedTime+"\n")
    newFile.write("Day:\n")
    newFile.write(updatedDate+"\n")
    newFile.write("Company:\n")
    newFile.write(company+"\n")
    if newFileType=="Drones":
        newFile.write("Drones:\n")
    if newFileType=="Timetable":
        newFile.write("Timeline:\n")
    newFile.close()

def droneWriter(droneAssignerTuple, newFileName):
    """
    writes body of new dronefile based on results from o.DroneAssigner()
    """
    
    DroneParcelCombo = droneAssignerTuple[0]
    UnassignedDrones = droneAssignerTuple[2]
    
    
    
    droneFile = open(newFileName, "a")

    valueList = list(DroneParcelCombo.values())
    assignedDrones = [item[c.DroneInCombo] for item in valueList]
    allDrones = assignedDrones + UnassignedDrones
    allDrones.sort(key=lambda k: (datetime.datetime.strptime(k[c.AvailableDate], '%Y-%M-%d'), datetime.datetime.strptime(k[c.AvailableHour], '%H:%M'), -float(k[c.Autonomy]), k[c.Name]))
    allDrones.reverse()
    allDrones = o.duplicateRemover(allDrones)
    allDrones.reverse() 
    


    for drone in allDrones:
        droneString = str(drone)
        droneString = droneString.replace("[","")
        droneString = droneString.replace("'","")
        droneString = droneString.replace("]","")
        droneFile.write(droneString + "\n")

    droneFile.close()

    return 

def timetableWriter(droneAssignerTuple, newFileName):
    


droneWriter(o.droneAssigner(droneList, parcelList), "drones20h00_2019y11m5.txt")
droneWriter(o.droneAssigner(droneList, parcelList), "timetable19:30_2019y11m5.txt")


    

