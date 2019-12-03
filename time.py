# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import constants
import readFiles as r
import datetime

def time_sorter(values):
    """
    Receives a list with each index corresponding to a list of each drone's specifications
    Requires: a txt file with a list of drones where each index corresponds to each drone's specifications
    Ensures: a sorted list where the first index corresponds to whichever drone has an earlier time
    """
        
    time1 = values[0][7]
    time2 = values[1][7]
    time3 = values[2][7]
    time4 = values[3][7]

    #Falta perceber como fazer strip so ao tempo sem incluir data e segundos
    time1 = datetime.datetime.strptime(str(time1), '%H:%M')
    time2 = datetime.datetime.strptime(str(time2), '%H:%M')
    time3 = datetime.datetime.strptime(str(time3), '%H:%M')
    time4 = datetime.datetime.strptime(str(time4), '%H:%M')

    if time1 < time2 and time1 < time3 and time1 < time4:
        print(time1)
    elif time2 < time1 and time2 < time3 and time2 < time4:
        print(time2)
    elif time3 < time1 and time3 < time2 and time3 < time4:
        print(time3)
    else:
        print(time4)

filedict = r.fileFinder()
values = r.droneLister(filedict["droneFile"])

time_sorter(values)