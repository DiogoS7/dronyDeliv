# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos


import constants as c
import readFiles

def droneAssigner(drone_list, parcel): #INCOMPLETE, NEEDS TIME COMPARATOR
    """
    Has to be used once per parcel
    """
    possible_drones = []
    for drone in drone_list:
        if parcel[c.OperationZone] in drone and drone[c.MaxDistance]>=parcel[4] and drone[c.Autonomy]>=(parcel[4]*2/1000): #if drone operates within the same area, has enough reach and has more autonomy than twice the range needed, it'll be considered
            possible_drones.append(drone)
    if possible_drones[0][tempo]==possible_drones[1][tempo]: #TIME COMPARISON: NEEDS TIME COMPARISON FUNCTION FROM TIME.PY
        possible_drones = sorted(possible_drones, reverse=True, key=lambda possible_drones: possible_drones[c.Autonomy])
        if possible_drones[0][c.Autonomy]==possible_drones[1][c.Autonomy]:
            possible_drones = sorted(possible_drones, key=lambda possible_drones: possible_drones[c.AccumDistance])
            if possible_drones[0][c.AccumDistance]==possible_drones[1][c.AccumDistance]:
                possible_drones = sorted(possible_drones, key=lambda possible_drones: possible_drones[c.Name]
    right_drone = possible_drones[0][0]
    return right_drone
     