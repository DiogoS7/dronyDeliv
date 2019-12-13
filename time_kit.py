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
    ##### ADDRESS 8AM THING IN DOCSTRING
    time_value = int(time_value)

    time_to_update = datetime.datetime.strptime(str(time_string), '%H:%M')

    time_updated = time_to_update + datetime.timedelta(minutes=time_value)

    time_updated = str(time_updated)

    time_updated = time_updated[11:16]


    return time_updated

def FileNameTimeUpdate(time_string, time_value):
    """
    Receives a string with the value of time and a value which will increment time
    Requires: time value in the format of a string and a integer value to increment 
    Ensures: time value now incremented based on value given 
    """    ################ EDIT BECAUSE FORMAT IS h AND NOT : LIKE TIME_UPDATE
    time_value = int(time_value)

    time_to_update = datetime.datetime.strptime(str(time_string), '%Hh%M')

    time_updated = time_to_update + datetime.timedelta(minutes=time_value)

    time_updated = str(time_updated)

    time_updated = "{0}h{1}".format(time_updated[11:13], time_updated[14:16])


    return time_updated

def date_update(date_string, days_value = 1):
    """

    """
    days_value = int(days_value)

    date_string = date_string.replace(" ","")

    date_to_update = datetime.datetime.strptime(str(date_string), '%Y-%M-%d')

    date_updated = date_to_update + datetime.timedelta(days=days_value)

    date_updated = str(date_updated)

    date_updated = date_updated[:10]

    return date_updated
    
def FileNameDateUpdate(date_string, days_value = 1):
    """

    """
    days_value = int(days_value)
    
    date_to_update = datetime.datetime.strptime(str(date_string), '%d-%M-%Y')

    date_updated = date_to_update + datetime.timedelta(days=days_value)

    date_updated = str(date_updated)

    date_updated = date_updated[:10]

    return date_updated


def timestampConverter(timestamp_string):
    """
    """
    timestamp_datetime = datetime.datetime.strptime(str(timestamp_string), '%H:%M')

    return timestamp_datetime

def FileNameTimestampConverter(timestamp_string):
    """
    """
    timestamp_datetime = datetime.datetime.strptime(str(timestamp_string), '%Hh%M')

    return timestamp_datetime


def timeMax(time1, time2):
    """
    ~~~~~ strings must be in format %H:%M
    """
    time1 = datetime.datetime.strptime(time1, '%H:%M')
    time2 = datetime.datetime.strptime(time2, '%H:%M')
    latter = max((time1, time2))
    latter = str(latter)[11:16]

    return latter

def timeMin(time1, time2):
    """
    ~~~~~ strings must be in format %H:%M
    """
    time1 = datetime.datetime.strptime(time1, '%H:%M')
    time2 = datetime.datetime.strptime(time2, '%H:%M')
    latter = min((time1, time2))
    latter = str(latter)[11:16]

    return latter

def DuplicateDroneSorter(duplicateDroneList):
    """
    helper function for droneWriter(), orders drones in order to remove the deprecated one from the list before printing
    """
    duplicateDroneList.sort(key=lambda k: (datetime.datetime.strptime(k[c.AvailableDate], '%Y-%M-%d'), datetime.datetime.strptime(k[c.AvailableHour], '%H:%M')))
    return duplicateDroneList