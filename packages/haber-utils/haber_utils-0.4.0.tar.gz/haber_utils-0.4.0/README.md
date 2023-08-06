CreateNewDirec
------
**Description:**

Will create a new directory. If the directory already exists it will delete the files within it.

**Inputs:**
- base_direc: string that represents the directory in which the new directory will be made
- name: string that represents the name of the new directory

**Outputs:**
- new_direc: string that represents the path of the new directory

UpdateProgress
------
**Description:**

Will print a status bar with the progress of the current progress.

**Inputs:**
- progress: float that is the current progress of the process
- symbol: an additional value to be printed (type is variable), not required then input ""

**Outputs:**
- prints a status bar showing the completion of the process

WriteDictToCSV
------
**Description:**

Will write a dict or a list of dicts to a csv.

**Inputs:**
- base_direc: string that represents the directory in which the file will be written
- details: dict or list of dicts that will be written into the target file
- csv_name: string that represents the name of the csv

**Outputs:**
- new_csv: string that represents the path of the created csv_file

CheckIfFileExists
------
**Description:**

Checks if a file currently exists.

**Inputs:**
- filename: string that represents the path of the file to be checked

**Outputs:**
- bool: True if the file exists or False if it does not

ConvertDictToList
------
**Description:**

Will convert a dictionary to a list without its respective keys.

**Inputs:**
- details: dict that the information will be converted to list format

**Outputs:**
- output_list: list that holds the extracted information

WriteOrAppendCSV
------
**Description:**

Will create or append a csv with a row of information for a specified csv and dictionary.

**Inputs:**
- csv_file: string that is the path for the csv file that will either be created or appended with the data
- details: dict that contains the data to append or write to the specified csv_file

**Outputs:**
- csv_file: string that is the path for the csv file that will either be created or appended with the data

RoundValueDown
------
**Description:**

Will round down a float to the specified amount of decimal places.

**Inputs:**
- number: float that represents the number that will be rounded down
- decimals: int that represents the number of decimal points to be rounded to

**Outputs:**
- new_val: float that is number round to decimals amount of decimal points