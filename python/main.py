import pathlib as pth
import os
import json
import sys
import sqlite3


try:
    from InquirerPy import inquirer
except ImportError:
    print("The library 'InquirerPy' is not present, install it using 'pip install InquirerPy' to proceed.")
    sys.exit()


# The function that initializes the config and stuff 
def inicnf():
    if not os.path.exists(CONFIGPATH):
        temp = {
            "db": str(FINDME / "data.db"),
        }

        with open(CONFIGPATH, "w") as f:
            json.dump(temp, f, indent=4)
        
        return(True)
    else:
        return(True)    


# The function that makes reading and writing to config a whole lot easier
def hconfig(action,key,value=None):
    if inicnf():
        with open(CONFIGPATH, "r") as f:
            temp = json.load(f)

        if action == 'read':
            return temp.get(key)
        elif action == 'change':
            temp[key] = value
            with open(CONFIGPATH, "w") as f:
                json.dump(temp, f, indent=4)
        else:
            print("invalid input for action", action)


# The function the initalizes the database
def inidb():
    conn = sqlite3.connect(hconfig('read','db'))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            terms TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    return True


# The function that manages writing stuff to the db


# The two functions that make it easier to get input or confirm smth
def inquircnfrm(message,defau):
    return inquirer.confirm(
        message=message,
        default=defau
    ).execute()

def inquirinp(message,defau):
    return inquirer.text(
        message=message,
        default=defau
    ).execute()


# The function that gets the folder's that are to be indexed
def getdir():
    tmp = []
    print("Please enter the directories of the folders that would need to be scanned. Type 'done' when finished.")
    while True:
        temp = inquirinp(">>",'')
        if temp.lower() == 'done':
            break
        elif pth.Path(temp).exists() and pth.Path(temp).is_dir():
            if temp in tmp:
                print("This directory is already recorded.")
                continue
            else:
                tmp.append(temp)
                continue
        else:
            print("The input you entered is invalid. Please try again.")
            continue
    return(tmp)



# The function that checks the file to see if it's a supported format
def checkfile(file):
    a = pth.Path(file).suffix.lower()
    if a in EXTENTIONS:
        return True
    else:
        return False


# The function that gets all the indexable files from the directories
def getfiles(dir):
    temp = []

    for root, b, files in os.walk(dir,onerror=lambda error: None):
        for file in files:
            if checkfile(file):
                temp.append(os.path.normpath(os.path.join(root, file)))


    return temp


# The function that handles getting and indexing the directories
def index():
    files = []
    dirs = getdir()
    print("The given directories will now be indexed. There might be a spike in memory usage.")
    for a in dirs:
        files += getfiles(a)

    print(files)




EXTENTIONS = [".txt",".md"]
FINDME = pth.Path(__file__).resolve().parent.resolve().parent
# print(FINDME)                                   # Works fine :>
CONFIGPATH = FINDME / "config.json"


inidb()
index()


