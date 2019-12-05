# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import readFiles as r
import datetime

def time_sorter(values):
    """
    Receives a list with each index corresponding to a list of each drone's specifications
    Requires: a txt file with a list of drones where each index corresponds to each drone's specifications
    Ensures: a sorted list where the first index corresponds to whichever drone has ready first
    """
    
    time1 = values[0][7]
    time2 = values[1][7]
    time3 = values[2][7]
    time4 = values[3][7]
    time5 = values[4][7]
    time6 = values[5][7]
    time7 = values[6][7]
    time8 = values[7][7]
    time9 = values[8][7]

    time1 = datetime.datetime.strptime(time1, '%H:%M').time()
    time2 = datetime.datetime.strptime(time2, '%H:%M').time()
    time3 = datetime.datetime.strptime(time3, '%H:%M').time()
    time4 = datetime.datetime.strptime(time4, '%H:%M').time()
    time5 = datetime.datetime.strptime(time5, '%H:%M').time()
    time6 = datetime.datetime.strptime(time6, '%H:%M').time()
    time7 = datetime.datetime.strptime(time7, '%H:%M').time()
    time8 = datetime.datetime.strptime(time8, '%H:%M').time()
    time9 = datetime.datetime.strptime(time9, '%H:%M').time()

    timedict = {}

    if time1 < time2 and time1 < time3 and time1 < time4 and time1 < time5 and time1 < time6 and time1 < time7 and time1 < time8 and time1 < time9:
        timedict[str(values[0])] = values[0]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time2 < time1 and time2 < time3 and time2 < time4 and time2 < time5 and time2 < time6 and time2 < time7 and time2 < time8 and time2 < time9:
        timedict[str(values[1])] = values[1]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time3 < time1 and time3 < time2 and time3 < time4 and time3 < time5 and time3 < time6 and time3 < time7 and time3 < time8 and time3 < time9:
        timedict[str(values[2])] = values[2]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time4 < time1 and time4 < time2 and time4 < time3 and time4 < time5 and time4 < time6 and time4 < time7 and time4 < time8 and time4 < time9:
        timedict[str(values[3])] = values[3]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time5 < time1 and time5 < time2 and time5 < time3 and time5 < time4 and time5 < time6 and time5 < time7 and time5 < time8 and time5 < time9:
        timedict[str(values[4])] = values[4]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time6 < time1 and time6 < time2 and time6 < time3 and time6 < time4 and time6 < time5 and time6 < time7 and time6 < time8 and time6 < time9:
        timedict[str(values[5])] = values[5]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time7 < time1 and time7 < time2 and time7 < time3 and time7 < time4 and time7 < time5 and time7 < time6 and time7 < time8 and time7 < time9:
        timedict[str(values[6])] = values[6]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time8 < time1 and time8 < time2 and time8 < time3 and time8 < time4 and time8 < time5 and time8 < time6 and time8 < time7 and time8 < time9:
        timedict[str(values[7])] = values[7]
        timelist = list(timedict)
        print(timelist)
        return timelist
    elif time9 < time1 and time9 < time2 and time9 < time3 and time9 < time4 and time9 < time5 and time9 < time6 and time9 < time7 and time9 < time8:
        timedict[str(values[8])] = values[8] 
        timelist = list(timedict)
        print(timelist)
        return timelist

filedict = r.fileFinder()
values = r.droneLister(filedict["droneFile"])

time_sorter(values)