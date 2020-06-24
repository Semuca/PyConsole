import os
import sys
from tkinter import *

sys.dont_write_bytecode = True

root = Tk()
root.title("Console")
root.geometry("800x450+0+0")
root.minsize(200, 55)

originPath = os.getcwd() + "/assets/"
currentDir = ""

editable = False

def Back (items):
    if (not items):
        global currentDir
        firstPoint = 0
        for i in range(len(currentDir)):
            if (i + 1 == len(currentDir)):
                currentDir = currentDir[0:firstPoint]
                break
            if (currentDir[i] == "/"):
                firstPoint = i + 1
        ChangeBackground("  >> " + currentDir)
        Listfiles(None)
        return originPath + currentDir
    else:
        InsertText("ERROR: This function 'Back' does not take items")
        return None

def GoTo (items):
    if (len(items) == 1):
        global currentDir
        folder = items[0]
        if (os.path.isdir(originPath + currentDir + folder)):
            currentDir = currentDir + folder + "/"
            InsertText("Navigated to: " + originPath + currentDir)
            ChangeBackground("  >> " + currentDir)
            Listfiles(None)
            return originPath + currentDir
        else:
            InsertText("ERROR: '" + folder + "' is not a valid file")
            return None
    else:
        InsertText("ERROR: The function 'GoTo' takes one item")
        return None

def Help (items):
    if (len(items) < 2):
        try:
            if (not items):
                index = 0
            else:
                index = (int(items[0]) - 1) * 10
            functionsList = sorted(functions.keys())
            if (index <= len(functionsList) and index >= 0):
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

def Import (items):
    if (len(items) == 1):
        try:
            sys.path.append(originPath + currentDir)
            module = __import__(items[0])
            functions.update(module.functions)
            InsertText("Imported functions:")
            for i in module.functions:
                InsertText(i)
            return items[0]
        except:
            InsertText("ERROR: '" + items[0] + "' is not a valid file")
            return None

def Listfiles (items):
    if (not items):
        result = ""
        filelist = os.listdir(originPath + currentDir)
        try:
            filelist.remove(".DS_Store")
        except:
            pass
        for i in filelist:
            InsertText(i)
        return filelist
    else:
        InsertText("ERROR: This function 'Listfiles' does not take items")
        return None

def Open (items):
    if (len(items) == 1):
        try:
            top = Toplevel()
            top.title(items[0])
            img = PhotoImage(file = originPath + currentDir + items[0])
            labelImage = Label(top, image = img, bg = "black", text = currentDir + items[0])
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

def Read (items):
    if (len(items) == 1):
        try:
            file = open(originPath + currentDir + items[0], "r")
            top = Toplevel()
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

functions = {
    "Back" : Back,
    "GoTo" : GoTo,
    "Help" : Help,
    "Import" : Import,
    "Listfiles" : Listfiles,
    "Open" : Open,
    "Read" : Read
}

def ImageConfigure(event):
    text = event.widget.cget("text")
    img = PhotoImage(file= originPath + text)
    if (event.height < img.height()):
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
    global background
    global editable
    rawCommand = current.get()
    InsertText(rawCommand)
    console.delete(len(background), "end")
    command = rawCommand[len(background):]
    readValue = 0
    readFunction = 0
    bracketlevel = -1
    values = []
    functionOrder = []
    value = None
    for i in range(len(command)):
        if (command[i] == "("):
            readValue = i + 1
            bracketlevel = bracketlevel + 1
            function = command[readFunction:i]
            readFunction = i + 1
            _func = []
            if (function in functions):
                values.append(_func)
                functionOrder.append(function)
            else:
                InsertText("ERROR: '" + function + "' is not a valid function")
                bracketlevel = -1
                break
        if (command[i] == ","):
            if (command[readValue:i] != "" and bracketlevel != -1):
                values[bracketlevel].append(command[readValue:i])
            readValue = i + 1
            readFunction = i + 1
        if (command[i] == ")"):
            if (bracketlevel != -1):
                if (command[readValue:i] != ""):
                    values[bracketlevel].append(command[readValue:i])
                value = None
                value = functions[functionOrder[bracketlevel]](values[bracketlevel])
                if (value == None):
                    bracketlevel = -1
                    break
                bracketlevel = bracketlevel - 1
                if (bracketlevel > -1):
                    values[bracketlevel].append(str(value))
            readValue = i + 1
        elif (command[i] == " "):
            readFunction = i + 1
    if (bracketlevel != -1):
        InsertText("ERROR: brackets are not closed")

def InsertText(newText):
    text.insert(0, str(newText))
    try:
        text.pop(56)
    except:
        pass
    prev = ""
    for i in range(len(text)):
        prev = text[i] + "\n" + prev
    prevCommands.config(text = prev)

def ChangeBackground(newBackground):
    global background
    global editable
    background = newBackground
    editable = True
    console.delete(0, END)
    console.insert(0, background)
    editable = False

def CheckStr(text):
    global background
    global editable
    if (text[:len(background)] == background or editable == True):
        return True
    else:
        return False

text = []

prev = ""
curentDir = ""
background = "  >> "
current = StringVar()
validatecmd = root.register(CheckStr)

main = Frame(root, bg = "black")
main.pack(fill = BOTH, expand = True)
main.pack_propagate(False)

prevCommands = Label(main, justify = LEFT, anchor = SW, text = prev, bg = "black", fg = "white", font = "Helvetica 12")
prevCommands.pack(expand = True, fill = BOTH)

console = Entry(root, bg = "black", fg = "white", insertbackground = "white", insertborderwidth = 50, font = "Helvetica 12", textvariable = current, relief = SUNKEN, cursor = "xterm", validate = "key", validatecommand = (validatecmd, "%P"))
console.pack(fill = X)
console.bind("<Return>", RunCommand)
console.insert(0, "  >> ")

root.mainloop()
