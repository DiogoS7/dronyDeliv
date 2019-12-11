# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import time_kit as t
import constants as c
import readFiles as r
import operator as o
import time
import datetime
# from pprint import pprint #testing

def DroneRemover(name, droneList):
    for drone in droneList:
        if drone[0]==name:
            droneList.remove(drone)
    return droneList


def timesort(x):
    for y in x:
        time_stamp = datetime.datetime.strptime(y[c.AvailableHour], '%H:%M')
        return time_stamp

def DroneAutonomySorter(list):
    list = sorted(list, reverse=True, key=lambda list: list[c.Autonomy])
    return list

def DroneAccumDistanceSorter(list):
    list = sorted(list, key=lambda list: list[c.AccumDistance])
    return list

def DroneNameSorter(list):
    list = sorted(list, key=lambda list: list[c.Name])
    return list

def droneAssigner(drone_list, parcel_list):
    """
    
    """

    DroneParcelCombo = {}

    for parcel in parcel_list:
      

        drone_list.sort(key=lambda k: (k[c.OperationZone] != parcel[c.OrderZone], datetime.datetime.strptime(k[c.AvailableDate], '%Y-%M-%d'), datetime.datetime.strptime(k[c.AvailableHour], '%H:%M'), -float(k[c.Autonomy]), float(k[c.AccumDistance]), k[c.Name]))
        
        
        possible1 = drone_list[0][:]
        possible2 = drone_list[1][:]
        possible3 = drone_list[2][:]

       
        
        if possible1[c.OperationZone]!=parcel[c.OrderZone] or float(possible1[c.MaxDistance])<int(parcel[c.OrderDistance]) or float(possible1[c.Autonomy])<(float(parcel[c.OrderDistance])*2/1000) or float(possible1[c.MaxWeight])<float(parcel[c.OrderWeight]):
            if possible2[c.OperationZone]!=parcel[c.OrderZone] or float(possible2[c.MaxDistance])<float(parcel[c.OrderDistance]) or float(possible2[c.Autonomy])<(float(parcel[c.OrderDistance])*2/1000) or float(possible2[c.MaxWeight])<float(parcel[c.OrderWeight]):
                if possible3[c.OperationZone]!=parcel[c.OrderZone] or float(possible3[c.MaxDistance])<float(parcel[c.OrderDistance]) or float(possible3[c.Autonomy])<(float(parcel[c.OrderDistance])*2/1000) or float(possible3[c.MaxWeight])<float(parcel[c.OrderWeight]):
                    DroneParcelCombo[parcel[c.OrderName]] = [parcel, "Cancelled"]
                    continue
                else:
                    right_drone = possible3
            else:
                right_drone = possible2 
        else:
            right_drone = possible1
    
        
        right_drone[c.Autonomy] = round((float(right_drone[c.Autonomy]) - (float(parcel[c.OrderDistance])*2)/1000), 1)
        right_drone[c.AccumDistance] = round((float(right_drone[c.AccumDistance]) + float(parcel[c.OrderDistance])*2/1000), 1)
        right_drone[c.AvailableHour] = t.time_update(t.timeMax(right_drone[c.AvailableHour], parcel[c.OrderHour]), parcel[c.OrderDuration])
        if t.timestampConverter(right_drone[c.AvailableHour])>t.timestampConverter("20:00"):
            right_drone[c.AvailableHour] = t.time_update("08:00", parcel[c.OrderDuration])
        
        
        DroneRemover(right_drone[c.Name], drone_list)
        drone_list.append(right_drone)
        DroneParcelCombo[parcel[c.OrderName]] = [parcel, right_drone]

    
    return DroneParcelCombo 



# fileDict = r.fileFinder()
# droneList = r.droneLister(fileDict["droneFile"])
# parcelList = r.parcelLister(fileDict["parcelFile"])

# pprint(droneAssigner(droneList, parcelList))

