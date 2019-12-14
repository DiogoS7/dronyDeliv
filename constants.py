# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55375 Diogo Santos
# 55373 José Almeida

# This module is used for the recording of constants used throughout the application

# Value of the index number corresponding to the name of a drone in list 
Name = 0

# Value of the index number corresponding to, respectively, the day, time and company found in readFiles.readHeader() return tuple
headerDate = 0
headerTime = 1
headerCompany = 2 
headerScope = 3

# Value of the index number corresponding to the name of the operation zone in list
OperationZone = 1

# Value of the index number corresponding to the maximum weight carryable by a drone in list
MaxWeight = 2

# Value of the index number corresponding to the maximum distance a drone in list can travel
MaxDistance = 3

# Value of the index number corresponding to the accumulated distance a drone in list has travelled
AccumDistance = 4

# Value of the index number corresponding to the autonomy of a drone in list
Autonomy = 5

# Value of the index number corresponding to the date when a deliver has been completed and the drone in list has returned to base 
AvailableDate = 6

# Value of the index number corresponding to the hour when a deliver has been completed and the drone in list has returned to base
AvailableHour = 7

# Value of the index number corresponding to the name of the client who ordered a certain parcel in list
OrderName = 0

# Value of the index number corresponding to the zone of the client who ordered a certain parcel in list
OrderZone = 1

# Value of the index number corresponding to the date when the parcel in list can be delivered
OrderDate = 2

# Value of the index number corresponding to the hour when the parcel in list can be delivered
OrderHour = 3

# Value of the index number corresponding to the distance from the parcel deliver location to the drone's base
OrderDistance = 4

# Value of the index number corresponding to the weight of a certain parcel
OrderWeight = 5

# Value of the index number corresponding to the time necessary for the deliver and return of the assigned drone
OrderDuration = 6

# Value of the index number corresponding to the position of time value in a list of each drone's specifications
TimeIndex = 7

# Value of the index number corresponding to, respectively, the drone and the parcel in DroneParcelCombo.values() (regarding DroneParcelCombo dictionary, that returns from organize.droneAssigner())

DroneInCombo = 1
ParcelInCombo = 0

# Value of the index number corresponding to, respectively, DroneParcelCombo and CancelledOrders from the tuple returned by organize.droneAssigner()

DroneParcelCombo = 0
CancelledOrders = 1


# Value of the index number corresponding to, respectively, updatedParcelDate and updatedParcel hour in function writeFiles.timetableWriter()
updatedParcelDate = 0
updatedParcelHour = 1
