# Dominique Massiot
# CEMHTI-CNRS
# personnal web page : http://www.cemhti.cnrs-orleans.fr/?nom=massiot
# dmfit program : http://nmr.cemhti.cnrs-orleans.fr/Default.aspx

import os
import genericpath

# tools to adress the Os system - works for Unix, MaxOs or Windows transparently

def currentDirectory():
    return os.getcwd()

def exists(path):
    """ returns True if file exists in Os """
    return genericpath.exists(path)

def filesize(path):
    """ returns the file size from Os """
    if not genericpath.isfile(path):
        return -1
    return genericpath.getsize(path)

def path_extension(path):
    """ returns the root filename and extension"""
    return os.path.splitext(path)

def getText_from_file (path):
    """ returns the text content of the file """
    if not exists(path):
        print (f"File '{path}' does not exist...")
        return None
    print ("file size : ", filesize(path))
    file = open(path, mode="r")
    text = file.read()
    file.close()
    return text

def getLines_from_file(path, clean=False):
    """ returns the table of lines from text file """
    text = getText_from_file(path)
    if not text:
        return None
    text = text.split("\n")
    if clean:
        text = [t.strip(' \t') for t in text]
    return text

def writeToFile(path, text, checkexist=False):
    """ write text or array of lines to a file - checking for existence if requested """
    if checkexist:
        if exists(path):
            rep = input(f"file '{path}'\nfile already exists - O)verwrite or A)bort ? ").lower()
            if not rep.startswith("o"):
                print ("writeToFile aborted...")
                return False
    file = open(path, mode="w")
    if len(text[0]) <= 1:      # if single line
        file.write(text)
    else:                   # if array of lines
        for line in text:
            file.write (line+"\n")
    file.close()
    print (f"saved in '{os.path.split(path)[-1]}'")
    return True


