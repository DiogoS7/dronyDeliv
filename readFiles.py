# 2019-2020 Programação 1 (LTI)
# Grupo 16
# 55373 José Almeida
# 55375 Diogo Santos 


def readHeader(file_name):
    
    """
    Returns a tuple with the day, time and company specified in file
    Requires: file to be a text file in established format and file_name to be within quotation marks
    Ensures: returnal of a tuple in format (day, time, company)
    """
    
    inFile = open(file_name, "r") 
    inFile.readline() #skips formal indication line
    time = inFile.readline().replace("\n", "") #removes leftover \n from ending of lines in text file
    inFile.readline() 
    day = inFile.readline().replace("\n", "")
    inFile.readline() 
    company = inFile.readline().replace("\n", "") 

    inFile.close()
    
    return (day, time, company)
 
def droneLister(file_name):
    """ 
    Returns a list where each element is a list containing the details of one drone. 
    Requires: "file_name" argument to be a text file in the established format and to be within quotation marks
    Ensures: a list with sublists containing the details of each drone separately. 
    following the format: [[name_of_drone], [area_of_operation], [weight_capacity],
    [max_range], [distance_travelled], [autonomy], [date_of_availability], [hour_of
    _availability]]
    """
    inFile = open(file_name, "r")
    predroneList = inFile.readlines() #separating function in an early list and a curated list for ease of understanding
    predroneList = predroneList[7:] #avoidance of header lines

    droneList = []

    for i in predroneList: #for each element in predroneList (raw drone details in string class), processes it (stripping and splitting) and appends to final, curated, droneList
        i = i.strip() #removes \n leftover from ending of lines in text file
        droneList.append(i.split(", ")) #appends every detail of the drone as a single element in the drone-specific sublist

    inFile.close()
    return droneList