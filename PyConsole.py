import os
import sys
from tkinter import *

sys.dont_write_bytecode = True #Prevents .pyc or .pyo files appearing when importing modules

root = Tk() #Creates and sets up window
root.title("Console")
root.geometry("800x450+0+0")
root.minsize(200, 55)

originPath = os.getcwd() + "/assets/" #Sets directory
currentDir = ""

editable = False #Determines if the header of the entry can be changed. Used in ChangeHeader

def Back (items): #Takes the directory one file back - Takes no parameters
    if (not items):
        global currentDir
        firstPoint = 0
        for i in range(len(currentDir)): #Starts from the end of the current directory filename and works back until it hits a bracket and resizes the text
            if (i + 1 == len(currentDir)):
                currentDir = currentDir[0:firstPoint]
                break
            if (currentDir[i] == "/"):
                firstPoint = i + 1
        ChangeHeader("  >> " + currentDir)
        Listfiles(None)
        return originPath + currentDir
    else:
        InsertText("ERROR: This function 'Back' does not take items")
        return None

def GoTo (items): #Goes to a specified folder in the current directory - Takes one parameter
    if (len(items) == 1):
        global currentDir
        folder = items[0]
        if (os.path.isdir(originPath + currentDir + folder)):
            currentDir = currentDir + folder + "/" #Changes current directory to match
            InsertText("Navigated to: " + originPath + currentDir)
            ChangeHeader("  >> " + currentDir)
            Listfiles(None) #Automatically lists directory files
            return originPath + currentDir
        else:
            InsertText("ERROR: '" + folder + "' is not a valid file")
            return None
    else:
        InsertText("ERROR: The function 'GoTo' takes one item")
        return None

def Help (items): #Lists all known functions - Takes no parameters or one parameter
    if (len(items) < 2):
        try:
            if (not items): #Sets index for the page based off parameter - If no parameter is mentioned, page 1 is assumed
                index = 0
            else:
                index = (int(items[0]) - 1) * 10
            functionsList = sorted(functions.keys())
            if (index <= len(functionsList) and index >= 0): #Tests if index is range
                for i in range(10):
                    try:
                        InsertText(functionsList[index + i])
                    except:
                        pass
            else:
                InsertText("ERROR: Page '" + items[0] + "' does not exist")
                return None
        except:
            InsertText("ERROR: '" + items[0] + "' is not a valid file")
            return None
    else:
        InsertText("ERROR: This function 'Help' takes one or no items")
        return None

def Import (items): #Imports a module from a .py file (Filename excludes the .py extension) - Takes one parameter
    if (len(items) == 1):
        try:
            sys.path.append(originPath + currentDir) #Sets the path so the module can be imported
            module = __import__(items[0])
            functions.update(module.functions)
            InsertText("Imported functions:")
            for i in module.functions:
                InsertText(i)
            return items[0]
        except:
            InsertText("ERROR: '" + items[0] + "' is not a valid file")
            return None

def Listfiles (items): #Lists all files in the current directory - Takes no parameters
    if (not items):
        result = ""
        filelist = os.listdir(originPath + currentDir)
        try:
            filelist.remove(".DS_Store") #Removes .DS_Store files on mac
        except:
            pass
        for i in filelist:
            InsertText(i)
        return filelist
    else:
        InsertText("ERROR: This function 'Listfiles' does not take items")
        return None

def Open (items): #Opens a .png file - Takes one parameter
    if (len(items) == 1):
        try:
            top = Toplevel() #Creates Toplevel and PhotoImage in label
            top.title(items[0])
            img = PhotoImage(file = originPath + currentDir + items[0])
            labelImage = Label(top, image = img, bg = "black", text = currentDir + items[0]) #Stores image directory in text
            labelImage.image = img
            labelImage.bind("<Configure>", ImageConfigure)
            labelImage.pack(expand = True, fill = BOTH)
            return items[0]
        except:
            InsertText("ERROR: '" + items[0] + "' is not a valid file")
            return None
    else:
        InsertText("ERROR: The function 'Open' takes one item")
        return None

def Read (items): #Reads a .txt file - Takes one parameter
    if (len(items) == 1):
        try:
            file = open(originPath + currentDir + items[0], "r")
            top = Toplevel() #Creates Toplevel and label
            top.title(items[0])
            contents = Label(top, text = file.read(), justify = LEFT, anchor = NW, bg = "black", fg = "white", font = "Courier 20")
            contents.pack(fill = BOTH, expand = True)
            return file.read()
        except:
            InsertText("ERROR: '" + items[0] + "' is not a valid file")
            return None
    else:
        InsertText("ERROR: The function 'Read' takes one item")
        return None

functions = { #Built-in Function list 
    "Back" : Back,
    "GoTo" : GoTo,
    "Help" : Help,
    "Import" : Import,
    "Listfiles" : Listfiles,
    "Open" : Open,
    "Read" : Read
}

def ImageConfigure(event): #Configures the image size based on window size from the toplevel created in Open
    text = event.widget.cget("text") #Gets directory text from the image label so it can find the image
    img = PhotoImage(file = originPath + text)
    if (event.height < img.height()): #Configures image height/width
        img = img.subsample(1, int((img.height() * 2) / event.height) + 1)
    else:
        img = img.zoom(1, int(event.height / (img.height() * 2)) + 1)
    if (event.width < img.width()):
        img = img.subsample(int((img.width() * 2) / event.width) + 1, 1)
    else:
        img = img.zoom(int(event.width / (img.width() * 2)) + 1, 1)
    event.widget.configure(image = img)
    event.widget.image = img
    event.widget.pack(expand = True, fill = BOTH)

def RunCommand(event):
    global prev
    global header
    global editable
    rawCommand = current.get() #Gets text from entry
    InsertText(rawCommand) #Inserts entry in console
    console.delete(len(header), "end") #Clears entry
    command = rawCommand[len(header):] #Removes the initial text from the command
    readValue = 0
    readFunction = 0
    bracketlevel = -1
    values = []
    functionOrder = []
    value = None
    for i in range(len(command)): #Runs through each letter in the command
        if (command[i] == "("): #If a bracket is found, the function is read from the bookmark and the bookmark is replaced after the bracket
            readValue = i + 1
            bracketlevel = bracketlevel + 1 #Bracket level is raised
            function = command[readFunction:i] #Find function
            readFunction = i + 1
            _func = []
            if (function in functions): #Make sure function exists
                values.append(_func)
                functionOrder.append(function)
            else:
                InsertText("ERROR: '" + function + "' is not a valid function")
                bracketlevel = -1
                break
        if (command[i] == ","): #If a comma is found, read a value from the bookmark and put it in the values in the bracketlevel
            if (command[readValue:i] != "" and bracketlevel != -1):
                values[bracketlevel].append(command[readValue:i])
            readValue = i + 1
            readFunction = i + 1
        if (command[i] == ")"): #If a closed bracket 
            if (bracketlevel != -1):
                if (command[readValue:i] != ""): #Includes parameters if they exist
                    values[bracketlevel].append(command[readValue:i])
                value = None
                value = functions[functionOrder[bracketlevel]](values[bracketlevel]) #Pass function and parameters
                if (value == None): #If an error has occured, break
                    bracketlevel = -1
                    break
                bracketlevel = bracketlevel - 1
                if (bracketlevel > -1): #If the brackets are closed, append the value
                    values[bracketlevel].append(str(value))
            readValue = i + 1
        elif (command[i] == " "): #Reset function bookmark if there is a space
            readFunction = i + 1
    if (bracketlevel != -1): #Make sure brackets are closed
        InsertText("ERROR: brackets are not closed")

def InsertText(newText): #Insert text into the console
    text.insert(0, str(newText))
    try:
        text.pop(56) #Keep only 56 lines
    except:
        pass
    prev = ""
    for i in range(len(text)): #Compile text
        prev = text[i] + "\n" + prev
    prevCommands.config(text = prev)

def ChangeHeader(newHeader): #Change the header of the entry
    global header
    global editable
    header = newHeader
    editable = True #Toggle the editable variable to allow the header to be changed
    console.delete(0, END)
    console.insert(0, header)
    editable = False

def CheckStr(text): #Every time the entry is edited, check to see if the header has been edited
    global header
    global editable
    if (text[:len(header)] == header or editable == True):
        return True
    else:
        return False

text = []

prev = "" #Setup string variables and CheckStr function
curentDir = ""
header = "  >> "
current = StringVar()
validatecmd = root.register(CheckStr)

main = Frame(root, bg = "black") #Setup Frame
main.pack(fill = BOTH, expand = True)
main.pack_propagate(False)

prevCommands = Label(main, justify = LEFT, anchor = SW, text = prev, bg = "black", fg = "white", font = "Helvetica 12") #Setup Console
prevCommands.pack(expand = True, fill = BOTH)

#Setup Entry
console = Entry(root, bg = "black", fg = "white", insertbackground = "white", insertborderwidth = 50, font = "Helvetica 12", textvariable = current, relief = SUNKEN, cursor = "xterm", validate = "key", validatecommand = (validatecmd, "%P"))
console.pack(fill = X)
console.bind("<Return>", RunCommand)
console.insert(0, "  >> ")

root.mainloop() #Tkinter mainloop
