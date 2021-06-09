import __main__

def Add (items): #Adds all floats passed - Takes two or more parameters
    if (len(items) >= 2):
        result = 0
        for item in items:
            try:
                item = float(item)
                result = result + item
            except:
                return __main__.ThrowInvalidValueError(item)
        return result
    else:
        return __main__.ThrowParametersError("Add", 2, 100)

def Divide (items): #Divides the first item by the next, then the product of that by the next, and so on - Takes two or more parameters
    if (len(items) >= 2):
        result = float(items[0])
        for item in range(len(items) - 1):
            try:
                result = result / float(items[item + 1])
            except:
                return __main__.ThrowInvalidValueError(item)
        return result
    else:
        return __main__.ThrowParametersError("Divide", 2, 100)

def Multiply (items): #Multiplies all floats passed - Takes two or more parameters
    if (len(items) >= 2):
        result = 1
        for item in items:
            try:
                item = float(item)
                result = result * item
            except:
                return __main__.ThrowInvalidValueError(item)
        return result
    else:
        __main__.InsertText("ERROR: The function 'Multiply' takes at least two items")
        return __main__.ThrowParametersError("Multiply", 2, 100)

def Subtract (items): #Subtracts the first item by the next, then the product of that by the next, and so on - Takes two or more parameters
    if (len(items) >= 2):
        result = float(items[0])
        for item in range(len(items) - 1):
            try:
                result = result - float(items[item + 1])
            except:
                return __main__.ThrowInvalidValueError(item)
        return result
    else:
        return __main__.ThrowParametersError("Subtract", 2, 100)

functions = { #Lists the functions to be read by PyConsole
    "Add" : Add,
    "Divide" : Divide,
    "Multiply" : Multiply,
    "Subtract" : Subtract
}
