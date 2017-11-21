import os
import sys
import json

# data path to config.json
root_dir = os.path.dirname(sys.modules['__main__'].__file__)
# the config file can be used in two ways which changes the data_path
# if called from detection when it's been run to test, the folder has a __main__
# and hence we need to get the parent

# read and return the required data, will send as string
def getConfig(section, var):
    try:
        data_path = os.path.join(root_dir, "configuration", "config.json")
        with open(data_path, 'r') as fl:
             # data contains the config information
             data = json.load(fl)
             return data.get(section).get(var)

    except FileNotFoundError:
        data_path = os.path.join(os.path.join(root_dir,os.pardir), "configuration", "config.json")
        with open(data_path, 'r') as fl:
            # data contains the config information
            data = json.load(fl)
            return data.get(section).get(var)

# write data to configuration file
def writeConfig(section, var, data):
    try:
        data_path = os.path.join(root_dir, "configuration", "config.json")
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

    except FileNotFoundError:
        data_path = os.path.join(os.path.join(root_dir,os.pardir), "configuration", "config.json")
        data_path = os.path.join(root_dir, "configuration", "config.json")
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
