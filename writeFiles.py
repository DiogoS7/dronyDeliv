# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import organize as o
import constants as c
import readFiles as r
import time_kit as t
import sys ###TESTING



def droneFileMaker(fileDict):    ############ TEST THIS
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

############################### TESTING CRAP
if __name__ == "__main__":         
    arg1 = str(sys.argv[1])
    arg2 = str(sys.argv[2])
    fileDict = r.fileFinder(arg1, arg2)
###############################

def headerWriter(newFileType, fileDict, newFileName):
    """
    new file type "Drones" or "Timetable"
    """

    originalFile = fileDict["droneFile"]
    date = r.readHeader(originalFile)[c.headerDate]
    time = r.readHeader(originalFile)[c.headerTime]
    company = r.readHeader(originalFile)[c.headerCompany]
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



# headerWriter("Timetable", fileDict, timetableFileMaker(fileDict))
# headerWriter("Drones", fileDict, droneFileMaker(fileDict))


    
    
    
    
    

    
    


def newDroneFileWriter(DroneParcelCombo, newDroneFileName):
    """
    receives updated DroneAssigner() dictionary and droneFileMaker() new file name
    """

########### IF LEN(DAY)=.... IF LEN(DAY)=...+1 (5/05)
    

