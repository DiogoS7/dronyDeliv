# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

# This module is named "time_kit" because the name "time" interfered with Python's built in "time" module. 

import datetime
import constants as c

def time_difference(time1, time2):
    """
    Calculates the time interval between time1 and time2 arguments.
    Requires: time1 and time2 arguments to be two strings in the "HOURS:MINUTES" ('%H:%M') format.
    Ensures: returnal of the time interval between time1 and time2
    """
    time1 = datetime.datetime.strptime(str(time1), '%H:%M')
    time2 = datetime.datetime.strptime(str(time2), '%H:%M')

    time_difference = max(time1, time2) - min(time1, time2)

    return str(time_difference)[2:4]



def time_update(time_string, time_value):
    """
    Receives a string with the value of time and a string with the value to update time string with.
    Requires: time_string to be a string in the "HOURS:MINUTES" ('%H:%M') format and time_value to be an integer representing minutes.
    Ensures: returns a string representing (time_string) with (time_value) minutes incremented.
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
    Receives a string with the value of time and a string with the value to update time string with. Similar to time_update() but works for a different string format.
    Requires: time_string to be a string in the "HOURShMINUTES" ('%Hh%M') format and time_value to be an integer representing minutes.
    Ensures: returnal of a string representing time_string with time_value minutes incremented.
    """    ################ EDIT BECAUSE FORMAT IS h AND NOT : LIKE TIME_UPDATE
    time_value = int(time_value)

    time_to_update = datetime.datetime.strptime(str(time_string), '%Hh%M')

    time_updated = time_to_update + datetime.timedelta(minutes=time_value)

    time_updated = str(time_updated)

    time_updated = "{0}h{1}".format(time_updated[11:13], time_updated[14:16])


    return time_updated

def date_update(date_string, days_value = 1):
    """
    Receives a string representing the date and adds days_value days to it. If no days_value argument is given, will add 1 day.
    Requires:  date_string to be a string in the "YEAR-MONTH-DAY" ('%Y-%M-%d') format and days_value to be an integer representing the days to add
    Ensures: returnal of a string representing date_string with days_value days incremented.
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
    Receives a string representing the date and adds days_value days to it. If no days_value argument is given, will add 1 day. Similar to date_update() but works for a different string format.
    Requires:  date_string to be a string in the "DAY-MONTH-YEAR" ('%d-%M-%Y') format and days_value to be an integer representing the days to add.
    Ensures: returnal of a string representing date_string with days_value days incremented.
    """
    days_value = int(days_value)
    
    date_to_update = datetime.datetime.strptime(str(date_string), '%d-%M-%Y')

    date_updated = date_to_update + datetime.timedelta(days=days_value)

    date_updated = str(date_updated)

    date_updated = date_updated[:10]

    return date_updated


def timestampConverter(timestamp_string):
    """
    Receives a timestamp and converts it to datetime type for ease of comparison with other timestamps.
    Requires: timestamp_string argument to be a string in the "HOURS:MINUTES" ('%H:%M') format.
    Ensures: returnal of the same timestamp but in  datetime type.
    """
    timestamp_datetime = datetime.datetime.strptime(str(timestamp_string), '%H:%M')

    return timestamp_datetime

def FileNameTimestampConverter(timestamp_string):
    """
    Receives a timestamp and converts it to datetime type for ease of comparison with other timestamps. Similar to timestampConverter() but works for a different string format.
    Requires: timestamp_string argument to be a string in the "HOURShMINUTES" ('%Hh%M') format.
    Ensures: returnal of the same timestamp but in  datetime type.
    """
    timestamp_datetime = datetime.datetime.strptime(str(timestamp_string), '%Hh%M')

    return timestamp_datetime


def timeMax(time1, time2):
    """
    Receives to timestamps and compares them, returning the latest of the two.
    Require: time1 and time2 arguments must be in the "HOURS:MINUTES" ('%H:%M') format.
    Ensures: returnal of the latest of the two.
    """
    time1 = datetime.datetime.strptime(time1, '%H:%M')
    time2 = datetime.datetime.strptime(time2, '%H:%M')
    latter = max((time1, time2))
    latter = str(latter)[11:16]

    return latter

def timeMin(time1, time2):
    """
    Receives to timestamps and compares them, returning the earliest of the two.
    Require: time1 and time2 arguments must be in the "HOURS:MINUTES" ('%H:%M') format.
    Ensures: returnal of the earliest of the two.
    """
    time1 = datetime.datetime.strptime(time1, '%H:%M')
    time2 = datetime.datetime.strptime(time2, '%H:%M')
    latter = min((time1, time2))
    latter = str(latter)[11:16]

    return latter

def DuplicateDroneSorter(duplicateDroneList):
    """
    Helper function for droneWriter(), sorts drones by their availability time.
    Requires: duplicateDroneList to be a list of which each element is a list containing the details of a drone in the established format ([[name_of_drone], [area_of_operation], [weight_capacity], [max_range], [distance_travelled], [autonomy], [date_of_availability], [hour_of_availability]]).
    Returns: the same duplicateDroneList, sorted by the following attributes: availability date, availability hour.
    """
    duplicateDroneList.sort(key=lambda k: (datetime.datetime.strptime(k[c.AvailableDate], '%Y-%M-%d'), datetime.datetime.strptime(k[c.AvailableHour], '%H:%M')))
    return duplicateDroneList