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


