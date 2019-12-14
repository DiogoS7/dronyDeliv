# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import organize as o
import constants as c
import readFiles as r
import time_kit as t
import datetime
from copy import deepcopy


def droneFileMaker(fileDict):
    """
    Creates new drone file and returns it's name.
    Requires: fileDict to be a dictionary containing the names of the input files.
    Returns: the new drone file's name.
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
    Creates timetable file and returns it's name.
    Requires: fileDict to be a dictionary containing the names of the input files.
    Returns: the timetable file's name.
    """

    originalFile = fileDict["parcelFile"]

    date = r.readHeader(originalFile)[c.headerDate]
    time = r.readHeader(originalFile)[c.headerTime]
    
    # simplifying date
    
    if len(date)==9:
        Day = date[:1]
        Year = date[5:9]
        Month = date[2:4]

    elif len(date)==10:
        Day = date[:2]
        Year = date[6:10]
        Month = date[3:5]

    updatedFileName = "timetable{0}h{1}_{2}y{3}m{4}.txt".format(time[:2], time[3:5], Year, Month, Day)
    
    updatedFile = open(updatedFileName, "w")
    updatedFile.close()
    

    return updatedFileName



def headerWriter(newFileType, fileDict, newFileName):
    """
    Updates the input file header and writes it on the desired new file.
    Requires: newFileType argument to be a string and to either be "Drones" or "Timetable". fileDict argument to be a dictionary containing the names of the input files. newFileName to be a string representing the name of the new file that is going to be written on.
    Ensures: updated header lines are written on the designated new file.
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
    Writes body of new drone file based on results from o.DroneAssigner().
    Requires: droneAssignerTuple to be a tuple including the dictionary that has the drone/parcel matches and a list of unassigned drones. newFileName has to be a string representing the name of the file to be written on.
    Returns: nothing.
    """
    
    DroneParcelCombo = deepcopy(droneAssignerTuple[0])
    UnassignedDrones = deepcopy(droneAssignerTuple[2])
    
    
    
    droneFile = open(newFileName, "a")

    valueList = deepcopy(list(DroneParcelCombo.values()))
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
    """
    Writes body of timetable file based on results from o.DroneAssigner().
    Requires: droneAssignerTuple to be a tuple including the dictionary that has the drone/parcel matches, a list of unassigned drones and a list of cancelled orders. newFileName has to be a string representing the name of the file to be written on.
    Returns: nothing.
    """
    parcelFile = open(newFileName, "a")
    DroneParcelCombo = deepcopy(droneAssignerTuple[0])
    CancelledOrders = deepcopy(droneAssignerTuple[1])
    valueList = deepcopy(list(DroneParcelCombo.values()))
    assignedDrones = [item[c.DroneInCombo] for item in valueList] # creates a list of assigned drones based on the values from the DroneParcelCombo dictionary
    DroneParcelCombo_Specified = {}
    updatedParcels = []
    writtenDrones = [] # list to keep track of the assigned drones that have been written in the timetable file. Updates with each line written
    CancelledOrders.sort(key=lambda k: (k[c.OrderName])) # sorts cancelled orders by their name
    if len(CancelledOrders)>0:
        for order in CancelledOrders:
            orderDate = order[c.OrderDate].replace(" ","")
            orderHour = order[c.OrderHour]
            orderName = order[c.OrderName]
            parcelFile.write("{0}, {1}, {2}, cancelled\n".format(orderDate, orderHour, orderName))
    
    valueList = deepcopy(list(DroneParcelCombo.values()))
    Parcels = [item[c.ParcelInCombo] for item in valueList] # creates list of parcels based on the values from the DroneParcelCombo dictionary.
    Parcels.sort(key=lambda k: (datetime.datetime.strptime(k[c.OrderDate].replace(" ",""), '%Y-%M-%d'), datetime.datetime.strptime(k[c.OrderHour], '%H:%M'), k[c.OrderName])) 
    
    for parcel, drone in valueList:
        DroneParcelCombo_Specified[parcel[c.OrderName]] = drone[c.Name] # creates simpler dictionary that includes only the parcel's client name and assigned drone
    
    
    assignedDroneNames = [item[c.Name] for item in assignedDrones]
    for order in Parcels:
        orderDate = order[c.OrderDate].replace(" ","")
        orderHour = order[c.OrderHour]
        orderName = order[c.OrderName]
        orderDrone = DroneParcelCombo_Specified[order[c.OrderName]]
        orderDuration = order[c.OrderDuration]

        # the following block of code serves the purpose of understanding if a given drone has been used more than once, in order to write the correct parcel departure hour and date in the timetable file

        if (assignedDroneNames.count(orderDrone) > 1) and (orderDrone in writtenDrones):
            assignedDrones.sort(key = lambda k: (datetime.datetime.strptime(k[c.AvailableDate], '%Y-%M-%d'), datetime.datetime.strptime(k[c.AvailableHour], '%H:%M')))
            assignedDroneNames = [item[c.Name] for item in assignedDrones]
            usedDroneIndex = assignedDroneNames.index(orderDrone)
            orderHour = assignedDrones[usedDroneIndex][c.AvailableHour]
            if t.timestampConverter(parcel[c.OrderHour]) > t.timestampConverter(assignedDrones[usedDroneIndex][c.AvailableHour]):
                orderHour = order[c.OrderHour]
        
        if t.timestampConverter(t.time_update(orderHour, orderDuration)) > t.timestampConverter("20:00"):
            orderHour = "08:00"
            orderDate = t.date_update(parcel[c.OrderDate])
        updatedParcel = []
        updatedParcel.append(orderDate)
        updatedParcel.append(orderHour)
        updatedParcel.append(orderName) 
        updatedParcel.append(orderDrone)
        updatedParcels.append(list(updatedParcel))
        writtenDrones.append(orderDrone)

    updatedParcels.sort(key= lambda k: (datetime.datetime.strptime(k[c.updatedParcelDate].replace(" ",""), '%Y-%M-%d'), datetime.datetime.strptime(k[c.updatedParcelHour], '%H:%M')))

    for order in updatedParcels:
        
        order = str(order)
        order = order.replace("[","")
        order = order.replace("'","")
        order = order.replace("]","")
        parcelFile.write(order + "\n")
    
    parcelFile.close()
    
    return




import sys

if __name__ == "__main__":
    arg1 = str(sys.argv[1])
    arg2 = str(sys.argv[2])
    fileDict = r.fileFinder(arg1, arg2)