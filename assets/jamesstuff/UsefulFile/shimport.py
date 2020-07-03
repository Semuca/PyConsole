import __main__

def Add (items):
    if (len(items) >= 2):
        result = 0
        for item in items:
            try:
                item = float(item)
                result = result + item
            except:
                __main__.InsertText("ERROR: '" + item + "' cannot be converted to a float")
                return None
        __main__.InsertText(str(result))
        return result
    else:
        __main__.InsertText("ERROR: The function 'Add' takes at least two items")
        return None

def Divide (items):
    if (len(items) >= 2):
        result = float(items[0])
        for item in range(len(items) - 1):
            try:
                result = result / float(items[item + 1])
            except:
                __main__.InsertText("ERROR: '" + item + "' cannot be converted to a float")
                return None
        __main__.InsertText(str(result))
        return result
    else:
        __main__.InsertText("ERROR: The function 'Divide' takes at least two items")
        return None

def Multiply (items):
    if (len(items) >= 2):
        result = 1
        for item in items:
            try:
                item = float(item)
                result = result * item
            except:
                __main__.InsertText("ERROR: '" + item + "' cannot be converted to a float")
                return None
        __main__.InsertText(str(result))
        return result
    else:
        __main__.InsertText("ERROR: The function 'Multiply' takes at least two items")
        return None

def Subtract (items):
    if (len(items) >= 2):
        result = float(items[0])
        for item in range(len(items) - 1):
            try:
                result = result - float(items[item + 1])
            except:
                __main__.InsertText("ERROR: '" + item + "' cannot be converted to a float")
                return None
        __main__.InsertText(str(result))
        return result
    else:
        __main__.InsertText("ERROR: The function 'Subtract' takes at least two items")
        return None

functions = {
    "Add" : Add,
    "Divide" : Divide,
    "Multiply" : Multiply,
    "Subtract" : Subtract
}
