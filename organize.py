# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

from __future__ import absolute_import
import time_kit as t
import constants as c
import readFiles as r

def DroneAutonomySorter(list):
    list = sorted(list, reverse=True, key=lambda list: list[c.Autonomy])
    return list

def DroneAccumDistanceSorter(list):
    list = sorted(list, key=lambda list: list[c.AccumDistance])
    return list

def DroneNameSorter(list):
    list = sorted(list, key=lambda list: list[c.Name])
    return list

def PossibleDroneLister(drone_list, parcel, used_drones):
    """

    """
    possible_drones = []
    for drone in drone_list:
        if parcel[c.OperationZone] in drone and int(drone[c.MaxDistance])>=int(parcel[c.OrderDistance]) and int(drone[c.Autonomy])>=int(parcel[c.OrderDistance])*2/1000 and int(drone[c.MaxWeight])>=int(parcel[c.OrderWeight]) and (drone not in used_drones): #and time is earlier than parceltime
                possible_drones.append(drone)
    return possible_drones


def droneAssigner(drone_list, parcel_list):
    """
    
    """

    possible_drones_new = []
    DroneParcelCombo = {}
    used_drones = []
    possible_drones = []
    for parcel in parcel_list:
        if parcel==parcel_list[2]:
            for drone in drone_list:
                if parcel[c.OperationZone] in drone and int(drone[c.MaxDistance])>=int(parcel[c.OrderDistance]) and int(drone[c.Autonomy])>=int(parcel[c.OrderDistance])*2/1000 and int(drone[c.MaxWeight])>=int(parcel[c.OrderWeight]) and (drone not in used_drones): #and time is earlier than parceltime
                    possible_drones.append(drone)
            #possible_drones = PossibleDroneLister(drone_list, parcel, used_drones)
            print(possible_drones)
            print("aqui")
            if len(possible_drones)==0:
                DroneParcelCombo[parcel[c.OrderName]] = [parcel, "Cancelled"]
                continue
            if len(possible_drones)==1:
                DroneParcelCombo[parcel[c.OrderName]] = [parcel, possible_drones[0]]
                used_drones.append(possible_drones[0])
                continue
            possible_drones = t.time_sorter(possible_drones) 
            if possible_drones[0][c.AvailableHour]==possible_drones[1][c.AvailableHour] and possible_drones[0][c.AvailableDate]==possible_drones[1][c.AvailableDate]:
                for drone in possible_drones:
                    if drone[c.AvailableHour]==possible_drones[0][c.AvailableHour]:
                        possible_drones_new.append(drone)
                possible_drones = possible_drones_new 
                possible_drones = DroneAutonomySorter(possible_drones)
                if possible_drones[0][c.Autonomy]==possible_drones[1][c.Autonomy]:
                    possible_drones = DroneAccumDistanceSorter(possible_drones)
                    if possible_drones[0][c.AccumDistance]==possible_drones[1][c.AccumDistance]:
                        possible_drones = DroneNameSorter(possible_drones)
            right_drone = possible_drones[0]
            DroneParcelCombo[parcel[c.OrderName]] = [parcel, right_drone]
            used_drones.append(right_drone)
    return DroneParcelCombo 


fileDict = r.fileFinder()
droneList = r.droneLister(fileDict["droneFile"])
parcelList = r.parcelLister(fileDict["parcelFile"])
print(droneAssigner(droneList, parcelList))

