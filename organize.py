# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos

import time_kit as t
import constants as c
import readFiles as r
import datetime

def duplicateRemover(list):
    """
    Helper function for writeFiles.droneWriter() which helps remove duplicate drones from a list of drones.
    Requires: list argument to be a list in which every element is a list containing the details of a drone in the established format ([[name_of_drone], [area_of_operation], [weight_capacity],[max_range], [distance_travelled], [autonomy], [date_of_availability], [hour_of_availability]]).
    Ensures: returnal of a list of drones identical to the received list, but without any duplicated drones.
    """
    unique_list = []
    unique_name_list = []
    for elem in list:
        if elem[c.Name] not in unique_name_list:
            unique_list.append(elem)
            unique_name_list.append(elem[c.Name])
    return unique_list


def DroneRemover(name, droneList):
    """
    Helper function for droneAssigner(), removes designated drone from designated list.
    Requires: name argument to be a string and to be the name of the drone (index position 0) and droneList to be a list of drones which follows the established format ([[name_of_drone], [area_of_operation], [weight_capacity],[max_range], [distance_travelled], [autonomy], [date_of_availability], [hour_of_availability]]).
    Ensures: A list identical to the received list, but without the drone which has the name given as input in its index position 0.
    """
    for drone in droneList:
        if drone[c.Name]==name:
            droneList.remove(drone)
    return droneList


def droneAssigner(drone_list, parcel_list):
    """
    Reads a list of drones and a list of parcels and ultimately decides which drone gets assigned to which parcel, specifying which drones were left unassigned and which parcels were cancelled.
    Requires: drone_list and parcel_list to be, respectively, a list of drones in which each element follows the established format ([[name_of_drone], [area_of_operation], [weight_capacity],[max_range], [distance_travelled], [autonomy], [date_of_availability], [hour_of_availability]]) and a list of parcels in which  each element follows the established format ([client],[area_from],[date_ordered], [hour_ordered], [distance base to delivery(meters)], [package weight],[time_necessary_for delivery]).
    Ensures: returnal of a tuple including: a dictionary with the data of the drone/parcel combinations (DroneParcelCombo), a list of orders that were cancelled (CancelledOrders) and a list of drones left unassigned (UnassignedDrones).
    """
    DroneParcelCombo = {}
    CancelledOrders = []
    original_drone_list = drone_list[:] # saves a list of original drones for future comparison (to determine unassigned drones)
    used_drones = [] 
    UnassignedDrones = []

    for parcel in parcel_list:
      
        # usage of sort() method to organize the list of drones in a way that prioritizes the desired drones by the given attributes, in their order of selection (same area as parcel, availability, highest to lowest autonomy, lowest to highest accumulated distance, and finally by alphanumeric order of their name)

        drone_list.sort(key=lambda k: (k[c.OperationZone] != parcel[c.OrderZone], datetime.datetime.strptime(k[c.AvailableDate], '%Y-%M-%d'), datetime.datetime.strptime(k[c.AvailableHour], '%H:%M'), -float(k[c.Autonomy]), float(k[c.AccumDistance]), k[c.Name]))
        
        # determining the 3 most best drones to use

        possible1 = drone_list[0][:]
        possible2 = drone_list[1][:]
        possible3 = drone_list[2][:]

        # comparing the 3 best drones and picking the right one
        
        if possible1[c.OperationZone]!=parcel[c.OrderZone] or float(possible1[c.MaxDistance])<int(parcel[c.OrderDistance]) or float(possible1[c.Autonomy])<(float(parcel[c.OrderDistance])*2/1000) or float(possible1[c.MaxWeight])<float(parcel[c.OrderWeight]):
            if possible2[c.OperationZone]!=parcel[c.OrderZone] or float(possible2[c.MaxDistance])<float(parcel[c.OrderDistance]) or float(possible2[c.Autonomy])<(float(parcel[c.OrderDistance])*2/1000) or float(possible2[c.MaxWeight])<float(parcel[c.OrderWeight]):
                if possible3[c.OperationZone]!=parcel[c.OrderZone] or float(possible3[c.MaxDistance])<float(parcel[c.OrderDistance]) or float(possible3[c.Autonomy])<(float(parcel[c.OrderDistance])*2/1000) or float(possible3[c.MaxWeight])<float(parcel[c.OrderWeight]):
                    CancelledOrders.append(parcel)
                    continue
                else:
                    right_drone = possible3
            else:
                right_drone = possible2 
        else:
            right_drone = possible1
    
        # updating the details of the right drone affected by completing the given parcel
        
        right_drone[c.Autonomy] = round((float(right_drone[c.Autonomy]) - (float(parcel[c.OrderDistance])*2)/1000), 1)
        right_drone[c.AccumDistance] = round((float(right_drone[c.AccumDistance]) + float(parcel[c.OrderDistance])*2/1000), 1)
        right_drone[c.AvailableHour] = t.time_update(t.timeMax(right_drone[c.AvailableHour], parcel[c.OrderHour]), parcel[c.OrderDuration])
        if t.timestampConverter(right_drone[c.AvailableHour])>t.timestampConverter("20:00"):
            right_drone[c.AvailableHour] = t.time_update("08:00", parcel[c.OrderDuration])
            right_drone[c.AvailableDate] = t.date_update(parcel[c.OrderDate])
        
        
        # using DroneRemover() to remove the old entry of the used drone to the new updated entry of that same drone

        DroneRemover(right_drone[c.Name], drone_list)
        drone_list.append(right_drone)
        used_drones.append(right_drone[c.Name]) # appending the drone to the used drones list to figure out wich drones were left unassigned
        DroneParcelCombo[parcel[c.OrderName]] = [parcel, right_drone] # defining which drone matches with which parcel in the combination dictionary
        
    # figuring out which drones were left unassigned

    for original_drone in original_drone_list:
        if original_drone[c.Name] not in used_drones:
            UnassignedDrones.append(original_drone)
    
    return (DroneParcelCombo, CancelledOrders, UnassignedDrones)