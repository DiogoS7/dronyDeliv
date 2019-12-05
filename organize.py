# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

from __future__ import absolute_import
import Time as t
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

def droneAssigner(drone_list, parcel):
    """
    
    """
    possible_drones = []
    for drone in drone_list:
        if parcel[c.OperationZone] in drone and int(drone[c.MaxDistance])>=int(parcel[4]) and int(drone[c.Autonomy])>=int(parcel[4])*2/1000 and int(drone[c.MaxWeight])>=int(parcel[5]):
            possible_drones.append(drone)
    if len(possible_drones)==0:
        return "Cancelled"
    if len(possible_drones)==1:
        return possible_drones[0]
    possible_drones = t.time_sorter(possible_drones) #NON FUNCTIONAL TIME SORTER
    #print(possible_drones)
    if possible_drones[0][c.AvailableHour]==possible_drones[1][c.AvailableHour] and possible_drones[0][c.AvailableDate]==possible_drones[1][c.AvailableDate]: 
        possible_drones = [possible_drones[0], possible_drones[1]]
        # print(possible_drones)
        possible_drones = DroneAutonomySorter(possible_drones)
        if possible_drones[0][c.Autonomy]==possible_drones[1][c.Autonomy]:
            possible_drones = DroneAccumDistanceSorter(possible_drones)
            if possible_drones[0][c.AccumDistance]==possible_drones[1][c.AccumDistance]:
                possible_drones = DroneNameSorter(possible_drones)
    right_drone = possible_drones[0]
    # right_drone = used_drones[right_drone] \\\\\\\\\\\ testar se o drone já foi e voltou e poderá estar disponivel \\\\\\ adicionar for das parcelas
    return right_drone


fileDict = r.fileFinder()
droneList = r.droneLister(fileDict["droneFile"])
parcelList = r.parcelLister(fileDict["parcelFile"])
parcel = parcelList[7]
print(droneAssigner(droneList, parcel))

