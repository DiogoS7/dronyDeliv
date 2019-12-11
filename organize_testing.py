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
        # drone_list.sort(key=o.itemgetter(parcel[c.OrderZone], t.time_sorter, c.Autonomy, c.AccumDistance, c.Name))
        print(parcel)

        #drone_list = t.time_sorter(drone_list)
        #drone_list.sort(key= lambda drone: (drone[c.OperationZone]!=parcel[c.OrderZone]))   
        drone_list.sort(key=lambda k: (k[1] != parcel[c.OrderZone], datetime.datetime.strptime(k[c.AvailableHour], '%H:%M'), , -int(k[c.Autonomy]), int(k[c.AccumDistance]), k(c.Name))) # SORT OUT THE NAME AND IT'S DONE
        
        #drone_list.sort(key= lambda x:(-int(x[c.Autonomy]), -int(x[c.AccumDistance]), x[c.Name]))
        
        print(drone_list)
        input()
        
        right_drone = drone_list[0]
        
        if right_drone[c.MaxDistance]<parcel[c.OrderDistance] or float(right_drone[c.Autonomy])<(int(parcel[c.OrderDistance])*2/1000) or right_drone[c.MaxWeight]<parcel[c.OrderWeight]:
            DroneParcelCombo[parcel[c.OrderName]] = [parcel, "Cancelled"]
        else:
            DroneParcelCombo[parcel[c.OrderName]] = [parcel, right_drone[c.Name]]
            right_drone[c.AvailableHour] = t.time_comparator(right_drone[c.AvailableHour], parcel[c.OrderHour])
            right_drone[c.Autonomy] = int(right_drone[c.Autonomy]) - (int(parcel[c.OrderDistance])*2)/1000
            right_drone[c.AccumDistance] = right_drone[c.AccumDistance] + parcel[c.OrderDistance]*2
            drone_list[0] = right_drone

    return None #DroneParcelCombo 



fileDict = r.fileFinder()
droneList = r.droneLister(fileDict["droneFile"])
parcelList = r.parcelLister(fileDict["parcelFile"])

#droneList.sort(key = lambda x:(x[c.OperationZone], x[c.AvailableHour], -x[c.Autonomy], -x[c.AccumDistance], x[c.Name]))
print(droneAssigner(droneList, parcelList))
