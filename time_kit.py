# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import datetime
import constants as c

def time_sorter(droneListUnsorted):
    """
    Receives a list with each index corresponding to a list of each drone's specifications
    Requires: a txt file with a list of drones where each index corresponds to each drone's specifications
    Ensures: a sorted list where the first index corresponds to whichever drone has ready first
    """
    
    droneListSorted = sorted(droneListUnsorted, key=lambda x: datetime.datetime.strptime(x[c.AvailableHour], '%H:%M'))

    return droneListSorted

def time_update(time_string, time_value):
    """
    Receives a string with the value of time and a value which will increment time
    Requires: time value in the format of a string and a integer value to increment 
    Ensures: time value now incremented based on value given
    """

    time_to_update = datetime.datetime.strptime(str(time_string), '%H:%M')

    time_updated = time_to_update + datetime.timedelta(minutes=time_value)

    time_updated = str(time_updated)

    time_updated = time_updated[11:16]

    return time_updated

