# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55375 Diogo Santos
# 55373 José Almeida

import readFiles as r
import organize as o
import time_kit as t

def write():
    """
    """ 

    #file_name = name + str(int(time) + 30) + date + company
    return 

def writeTimetable():
    """  
    """

    fileDict = r.fileFinder()
    ParcelFileName = fileDict["parcelFile"]    
    Header = r.readHeader(ParcelFileName)
    time = Header[0]
    day = Header[1]
    company = Header[2]
    
    inFile = open(, "w")
    inFile.write("Time:\n")
    inFile.write(t.time_update(time, 30))
    inFile.write("\nDay:\n")
    inFile.write(day)
    inFile.write("\nCompany:\n")
    inFile.write(company)
    inFile.write("\nParcels:\n")
    return