import datetime
import json
import sys
from os import environ, mkdir
from os.path import isdir

# Finds the current time and returns it in a human readable format.
def getTime(timeToFind):
    currentTime = datetime.datetime.fromtimestamp(timeToFind)
    return currentTime.strftime("%Y-%m-%d %H:%M:%S")

from .log import doLog

# Retrieves the user configurations from a .json file, or creates a config file from default values if one can't be found.
def getConfig(gvars):

    try:
        with open(gvars.home+"/.oscr/config.json") as configFile:
            try:
                fromConfig = json.load(configFile)
            except json.decoder.JSONDecodeError:
                doLog("Failed to get config; could not decode JSON file. Exiting.", gvars)
                sys.exit(0)
            gvars.config = fromConfig["config"][0]
            gvars = calculateEssentials(gvars)

    except FileNotFoundError:
        user = input("No config file found. Please enter your Reddit username:  /u/")
        os = input("Optionally, you may also enter your operating system. This is only used in the user_agent and can be left blank by simply pressing enter:  ")
        defaultConfig = {
            "blacklist": [
                "claim",
                "done",
                "unclaim",
                "claim -- this was a automated action. please contact me with any questions.",
                "done -- this was a automated action. please contact me with any questions.",
                "unclaim -- this was a automated action. please contact me with any questions.",
                "claiming"
            ],
            "cutoff": 1,
            "cutoffUnit": 3600,
            "limit": 100,
            "logUpdates": True,
            "os": os,
            "recur": True,
            "unit": [
                "minute",
                "minutes",
                60
            ],
            "user": user,
            "torOnly": True,
            "wait": 10
        }
        outConfig = {}
        outConfig["config"] = []
        outConfig["config"].append(defaultConfig)

        try:
            dumpConfig(outConfig, gvars)
        except FileNotFoundError:
            doLog("home/.oscr directory not found; creating.", gvars)
            if not isdir(gvars.home+"/.oscr"):
                mkdir(gvars.home+"/.oscr")
                dumpConfig(outConfig, gvars)
            
        gvars.config = outConfig["config"][0]

    # Performs any necessary one-time calculations and changes relating to the config
    gvars = calculateEssentials(gvars)
    
    return gvars.config

def calculateEssentials(gvars):
    
    if not str(gvars.config["limit"]).isnumeric() or gvars.config["limit"] >= 1000:
        gvars.config["limit"] = None
    try:
        gvars.config["cutoffSec"] = gvars.config["cutoff"]*gvars.config["cutoffUnit"]
    except (KeyError, TypeError):
        gvars.config["cutoffSec"] = gvars.config["cutoff"]*3600
    gvars.config["waitTime"] = gvars.config["wait"]*gvars.config["unit"][2]
    
    return gvars

# Attempts to update the config file
def dumpConfig(outConfig, gvars):
    
    with open(gvars.home+"/.oscr/config.json", "w") as outFile:
        outFile.write(json.dumps(outConfig, indent=4, sort_keys=True))
    return True

# Creates praw.ini file, if it is missing
def createIni(gvars):

    savePath = defineSavePath(gvars)
    doLog("praw.ini missing, incomplete or incorrect. It will need to be created.", gvars)
    iniVars = {
        "client_id": input("Please input your client id:  "),
        "client_secret": input("Please input your client secret:  "),
        "username": input("Please input your Reddit username:  /u/"),
        "password": input("Please input your Reddit password:  ")
    }
    with open(savePath+"/praw.ini", "a+") as file:
        file.write("[oscr]\n")
        for i in iniVars:
            file.write(i+"="+iniVars[i]+"\n")
    return True
   
def reformatIni(gvars):
    
    savePath = defineSavePath(gvars)
    
    try:
        
        with open(savePath+"/praw.ini", "r+") as file:
            
            content = file.read().splitlines()
            
            # If file is empty
            if content == []:
                doLog("praw.ini file is empty. Proceeding to create.", gvars)
                createIni(gvars)
            
            # If file is not empty
            else:
                success = False
                file.seek(0)
                
                # Replace necessary line and write all lines to file
                for line in content:
                    if line == "[cdrcredentials]":
                        doLog(f"Replacing line '{line}' with '[oscr]'.", gvars)
                        line = "[oscr]          "
                        success = True
                    elif line in ["[oscr]", "[oscr]          "]:
                        success = True
                    file.write(line+"\n")
                
                # If successfully formatted to OSCR
                if success:
                    return True
                
                # If no cdrcredentials or oscr section was found
                else:
                    doLog("praw.ini file is missing a section for OSCR. Proceeding to create.", gvars)
                    createIni(gvars)
                    return True
                    
    except FileNotFoundError:
        createIni(gvars)
    return True

def defineSavePath(gvars):
    
    platformConfs = {
        "linux": "/.config",
        "darwin": "/.config"
    }
    if sys.platform.startswith("win"):
        savePath = environ["APPDATA"]
    else:
        savePath = gvars.home + platformConfs[sys.platform]
    
    return savePath
          
# Retrieves the date the comment was posted at.
def getDate(comment):
    return comment.created_utc
