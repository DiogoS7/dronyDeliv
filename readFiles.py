# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import constants as c
import fnmatch
import os
import datetime


def readHeader(file_name):
    
    """
    Returns a tuple with the date, time and company specified in file
    Requires: file to be a text file in established format and file_name to be within quotation marks
    Ensures: returnal of a tuple in format (date, time, company)
    """
    
    inFile = open(file_name, "r") 
    inFile.readline() #skips formal indication line
    time = inFile.readline().replace("\n", "") #removes leftover \n from ending of lines in text file
    inFile.readline() 
    date = inFile.readline().replace("\n", "")
    inFile.readline() 
    company = inFile.readline().replace("\n", "") 

    inFile.close()
    
    return (date, time, company)
 
def droneLister(file_name):
    """ 
    Returns a list where each element is a list containing the details of one drone. 
    Requires: "file_name" argument to be a text file in the established format and to be within quotation marks
    Ensures: a list with sublists containing the details of each drone in separate elements
    following the format: [[name_of_drone], [area_of_operation], [weight_capacity],
    [max_range], [distance_travelled], [autonomy], [date_of_availability], [hour_of
    _availability]]
    """
    inFile = open(file_name, "r")
    predroneList = inFile.readlines() #separating function in an early list and a curated list for ease of understanding
    predroneList = predroneList[7:] #avoidance of header lines

    droneList = []

    for i in predroneList: #for each element in predroneList (raw drone details in string class), processes it (stripping and splitting) and appends to final, curated, droneList
        i = i.strip() #removes \n leftover from ending of lines in text file
        droneList.append(i.split(", ")) #appends every detail of the drone as a single element in the drone-specific sublist

    inFile.close()
    return droneList

def parcelLister(file_name):
    """
    Returns a lsit where each element is a list containing the details of one order. This function is identical to droneLister,
    it was created for the sake of simplicity during further development.
    Requires: "file_name" argument to be a text file in the established format and to be within quotation marks
    Ensures: a list with sublists containing the details of each order in separate element
    following the format: [[name_of_client], [area_of_delivery], [date_of_order], 
    [hour_of_order], [distance_from_base], [parcel_weight]]
    """
    inFile = open(file_name, "r")
    preparcelList = inFile.readlines() #separating function in an early list and a curated list for ease of understanding
    preparcelList = preparcelList[7:] #avoidance of header lines

    parcelList = []

    for i in preparcelList: #for each element in preparcelList (raw parcel details in string class), processes it (stripping and splitting) and appends to final, curated, parcelList
        i = i.strip() #removes \n leftover from ending of lines in text file, could be "i.replace("\n", "")"
        parcelList.append(i.split(", ")) #appends every detail of the parcel as a single element in the parcel-specific sublist

    inFile.close()
    return parcelList

def fileFinder(sysarg1, sysarg2):
    """
    Given that the program is meant to simply be executed within the same directory as the drone and parcel files,
    without having to be tampered with by the examining teachers, this function serves the purpose of finding those two files
    and organizing them in a dictionary for ease of use. This function requires no input.
    Returns: dictionary which includes the name of the drone file and the name of the name of the parcel file.
    Usage: for intended use, "fileDict=fileFinder()" should be included in main file
    """
    fileDict= {}
    fileDict["droneFile"] = sysarg1
    fileDict["parcelFile"] = sysarg2

    return fileDict

def validateFile(file_name):
    """
    """
    time = str(c.headerTime)
    date = str(c.headerDate)

    try:
        datetime.datetime.strptime(time, '%h%')
    except ValueError:
        print("Input error: name and header inconsistent in file <name of file>.")
    try:
        datetime.datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        print("Input error: name and header inconsistent in file <name of file>.")

# fileDict = fileFinder()

# print(fileDict)

# caract = readHeader(fileDict["droneFile"])
# print(caract[1])