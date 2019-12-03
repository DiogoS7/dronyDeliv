# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import constants
import readFiles as r
import datetime

def time_compare(time1, time2):
    """
    Compares two time string arguments and returns whichever is earlier (smaller)
    Requires: both time values to be in the format of a string 
    Ensures: earliest of both time strings 
    """

    time1 = datetime.datetime.strptime(str(time1), '%H:%M')
    time2 = datetime.datetime.strptime(str(time2), '%H:%M')

    if time1.time() < time2.time():

        return (str(time1.hour)+":"+str(time1.minute))
    else:
        return (str(time2.hour)+":"+str(time2.minute))

fileDict = r.fileFinder()

values = r.droneLister(fileDict["droneFile"])

time1 = values[1][7]
time2 = values[0][7]

print(time_compare(time1, time2))