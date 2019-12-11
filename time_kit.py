# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

# This module is named "time_kit" because the name "time" interfered with standard time module in python library

import datetime
import constants as c

def time_difference(time1, time2):
    """
    2 strings in : format
    """
    time1 = datetime.datetime.strptime(str(time1), '%H:%M')
    time2 = datetime.datetime.strptime(str(time2), '%H:%M')

    time_difference = max(time1, time2) - min(time1, time2)

    return str(time_difference)[2:4]



def time_update(time_string, time_value):
    """
    Receives a string with the value of time and a value which will increment time
    Requires: time value in the format of a string and a integer value to increment 
    Ensures: time value now incremented based on value given
    """
    time_value = int(time_value)

    time_to_update = datetime.datetime.strptime(str(time_string), '%H:%M')

    time_updated = time_to_update + datetime.timedelta(minutes=time_value)

    time_updated = str(time_updated)

    time_updated = time_updated[11:16]

    return time_updated

def timeMax(time1, time2):
    """
    ~~~~~ strings must be in format %H:%M
    """
    time1 = datetime.datetime.strptime(time1, '%H:%M')
    time2 = datetime.datetime.strptime(time2, '%H:%M')
    latter = max((time1, time2))
    latter = str(latter)[11:16]

    return latter
