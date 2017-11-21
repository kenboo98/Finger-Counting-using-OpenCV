import os
import sys
import json

# data path to config.json
root_dir = os.path.dirname(sys.modules['__main__'].__file__)
data_path = os.path.join(root_dir, "configuration", "config.json")

# read and return the required data, will send as string
def getConfig(section, var):
    with open(data_path, 'r') as fl:
         # data contains the config information
         data = json.load(fl)
         return data.get(section).get(var)

# write data to configuration file
def writeConfig(section, var, data):
     with open(data_path, 'r+') as fl:
         # read and store data
         jsonData = json.load(fl)
         del jsonData[section][var]
         jsonData[section][var] = data
         fl.close()

     # to write data
     with open(data_path, 'w') as fl:
         json.dump(jsonData, fl)
         fl.close()
