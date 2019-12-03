# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import constants
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
    #itime1 = datetime.datetime.strptime(str(time1), '%H:%M')
    #itime2 = datetime.datetime.strptime(str(time2), '%H:%M')
    #itime3 = datetime.datetime.strptime(str(time3), '%H:%M')
    print(time1, time2, time3)

droneList = open("droneList.txt")
values = list(droneList.read())

print(values[0])

time_sorter(values)