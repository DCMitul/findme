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
    # The path column has the path of the files and the terms column contains every word in that file
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


# The functions that manage writing stuff to the db
# The function that writes to the data table
def writetodata(loc,terms):
    conn = sqlite3.connect(hconfig("read",'db'))
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO data (path, terms) VALUES(?, ?)
    """, (loc, terms))

    conn.commit()
    conn.close()


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


# The functions that manage getting terms from specific file types
def txt(fl):
    tmp = []
    with open(fl, 'r') as file:
        for line in file:
            result = line.strip()
            result = result.replace(",",".")
            result = result.replace(" ",".")
            result = result.replace("/",".")
            result = result.replace(";",".")
            result = result.replace("'",".")
            result = result.replace("]",".")
            result = result.replace("[",".")
            result = result.replace("*",".")
            result = result.replace("+",".")
            result = result.replace("\\",".")
            result = result.replace("<",".")
            result = result.replace(">",".")
            result = result.replace("?",".")
            result = result.replace(":",".")
            result = result.replace("|",".")
            result = result.replace("{",".")
            result = result.replace("}",".")
            result = result.replace('"',".")
            result = result.replace(')',".")
            result = result.replace('(',".")
            result = result.replace('^',".")
            result = result.replace('!',".")
            result = result.replace('`',".")
            # result = result.replace('',".")
            # result = result.replace('',".")
            # result = result.replace('',".")
            # result = result.replace('',".")
            # result = result.replace('',".")
            result = result.split('.')
            # print(result)
            result = [x for x in result if x != " "]
            result = [x for x in result if x != ""]
            # print(result)
            tmp += result
    return(tmp)


def md(fl):
    pass


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


# The function that returns all the terms from the given file
def getterms(file):
    tmpe = pth.Path(file).suffix.lower()
    if tmpe == ".txt":
        return(txt(file))
    elif tmpe == ".md":
        md(file)



# The function that handles making the row and sending it to the function that adds stuff to the db
def makerow():
    files = []
    dirs = getdir()
    print("The given directories will now be indexed. There might be a spike in memory and cpu usage.")
    for a in dirs:
        files += getfiles(a)

    for file in files:
        terms = getterms(file)
        terms = list(set(terms))
        terms = json.dumps(terms)
        # print(terms)
        writetodata(file,terms)




EXTENTIONS = [".txt",".md"]
FINDME = pth.Path(__file__).resolve().parent.resolve().parent
# print(FINDME)                                   # Works fine :>
CONFIGPATH = FINDME / "config.json"


inidb()
makerow()



