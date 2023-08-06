import os

os.system("")

def CreateFile(name, ifexists = False):
    name = str(name)

    f = None
    if ifexists:
        if not os.path.exists(name):
            f = open(name, 'x')
    else:
        f = open(name, 'x')
    return f

def DeleteFile(name):
    name = str(name)

    # os.remove(name)
    if os.path.exists(name):
        os.remove(name)
    else:
        print("\033[91m" + "The file does not exist" + "\033[0m")

def DeleteDirectory(name):
    name = str(name)

    # os.rmdir(name)
    if os.path.exists(name):
        os.rmdir(name)
    else:
        print("\033[91m" + "The directory does not exist" + "\033[0m")
    
def ReadFile(name):
    name = str(name)

    f = open(name, 'r')
    contents = f.read()
    return contents

def ReadFileLines(name):
    name = str(name)

    f = open(name, 'r')
    contents = f.readlines()
    return contents

def ReadFileLine(name, line):
    name = str(name)
    line = int(line)

    f = open(name, 'r')
    lines = f.readlines()
    line = lines[line - 1]
    return line

def WriteFile(name, text):
    name = str(name)
    text = str(text)

    f = open(name, 'w')
    f.write(text)
    return f
    
def AppendFile(name, text):
    name = str(name)
    text = str(text)

    f = open(name, 'a')
    f.write(text)
    return f
    
def CheckFileExists(name):
    name = str(name)

    exists = os.path.exists(name)
    return exists

def Create(name, ifexists = False):
    return CreateFile(name, ifexists)

def Delete(name):
    DeleteFile(name)

def DeleteDir(name):
    DeleteDirectory(name)
    
def Read(name):
    return ReadFile(name)

def ReadLines(name):
    return ReadFileLines(name)

def ReadLine(name, line):
    return ReadFileLine(name, line)

def Write(name, text):
    return WriteFile(name, text)
    
def Append(name, text):
    return AppendFile(name, text)
    
def CheckExists(name):
    return CheckFileExists(name)