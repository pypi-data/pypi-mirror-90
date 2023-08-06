# Author: Ron Haber
# Date: 3.1.2021
# This library is to be used for the purposes of reducing the amount of code that I rewrite and copy

import os, sys
import json, csv
import math

def CreateNewDirec(base_direc: str, name: str):
    '''
    Will create a new directory. 
    If the directory already exists it will delete the files within it.

    :param base_direc: string that represents the directory in which the 
                        new directory will be made
    :param name: string that represents the name of the new directory
    :return new_direc: string that represents the path of the new directory
    '''
    if(base_direc[-1] == '/' or base_direc[-1] == '\\'):
        base_direc = base_direc[:-1] # will remove the final slash
    new_direc = os.path.join(base_direc, name)
    if(os.path.isdir(new_direc)):
        for f in os.listdir(new_direc):
            os.remove(os.path.join(new_direc, f))
        # return False # Temporary for the purposes of pausing the script
    else:
        os.mkdir(new_direc)
    return new_direc # without the final slash

def UpdateProgress(progress: float, symbol):
    '''
    Will print a status bar with the progress of the current progress.

    :param progress:float that is the current progress of the process
    :param symbol: an additional value to be printed (type is variable),
                    not required then input ""
    '''
    bar_length = 25
    status = ""
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(bar_length*progress))
    text = "\rPercent Complete: [{0}] {1}% {2}".format( "#"*block + "-"*(bar_length-block), progress*100, str(symbol), " ",status)
    sys.stdout.write(text)
    sys.stdout.flush()

def WriteDictToCSV(base_direc: str, details, csv_name: str):
    '''
    Will write a dict or a list of dicts to a csv.

    :param base_direc: string that represents the directory
                        in which the file will be written
    :param details: dict or list of dicts that will be written
                    into the target file
    :param: csv_name: string that represents the name of the csv
    :return new_csv: string that represents the path of the created
                     csv_file
    '''
    if(base_direc[-1] == '/' or base_direc[-1] == '\\'):
        base_direc = base_direc[:-1] # will remove the final slash
    csv_name = csv_name + '.csv'
    new_csv = os.path.join(base_direc, csv_name)
    if(type(details) == dict):
        data = [details]
    else:
        data = list(details)
    try:
        keys = data[0].keys()
    except IndexError:
        raise TypeError("The data passed is not a dictionary, a list of dictionaries or is empty.")
        return
    with open(new_csv, 'w') as new_file:
        writer = csv.DictWriter(new_file, keys)
        writer.writeheader()
        writer.writerows(data)
    return new_csv

def CheckIfFileExists(filename: str):
    '''
    Checks if a file currently exists.

    :param filename: string that represents the path of the file 
                    to be checked
    :return: True if the file exists or False if it does not
    '''
    return os.path.isfile(filename)

def ConvertDictToList(details: dict):
    '''
    Will convert a dictionary to a list without its respective keys.

    :param details: dict that the information will be converted to 
                    list format
    :return output_list: list that holds the extracted information
    '''
    mid_list = list(details.items())
    output_list = []
    for item in mid_list:
        output_list.append(item[1]) # This gets the value not the keys
    return output_list

def WriteOrAppendCSV(csv_file: str, details: dict):
    '''
    Will create or append a csv with a row of information for a 
    specified csv and dictionary.

    :param csv_file: string that is the path for the csv file 
                    that will either be created or appended with
                    the data
    :param details: dict that contains the data to append or write
                    to the specified csv_file
    :return csv_file: string that is the path for the csv file that
                    will either be created or appended with the data
    '''
    if(type(details) != dict):
        raise TypeError("Details must be of dict type")
    if(CheckIfFileExists(csv_file)):
        # Append
        list_to_append = CreateNewDirec(details)
        with open(csv_file, 'a') as old_file:
            writer = csv.writer(old_file)
            writer.writerow(list_to_append)
    else:
        keys = details.keys()
        with open(csv_file, 'w') as new_file:
            writer = csv.DictWriter(new_csv, keys)
            writer.writeheader()
            writer.writerow(details)
    return csv_file

def RoundValueDown(number: float, decimals: int):
    '''
    Will round down a float to the specified amount of decimal
    places.

    :param number: float that represents the number that will be
                    rounded down
    :param decimals: int that represents the number of decimal points
                    to be rounded to
    :return new_val: float that is number round to decimals amount of
                    decimal points
    '''
    if(decimals == 0):
        return math.floor(number)
    factor = 10 ** decimals
    new_val = math.floor(number * factor)/factor
    return new_val