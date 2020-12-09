from HopscotchFileFunctions import *
import os
import json

#Set the mode: "Independent" starts the text interface
mode = ""

if mode == "Independent":
    pathToScript = os.path.dirname(os.path.abspath(__file__))
    JSON_files = os.listdir((pathToScript + "/json_projects"))

    print ("Tillgängliga filer:\n")
    number = 0
    for i in JSON_files:
        number += 1
        print (i, "(",number,")")

        print ("\nVilken fil vill du öppna?")
        fileToOpen = int(input("")) - 1

        fullDirectory = pathToScript + "/json_projects/" + JSON_files[fileToOpen]

indentL = 0
indentStr = "  "
lastIndentWasStart = False
lastIndentL = 0

printString = "" #The string that contains all print_ commands

def print_(*arg):
    global printString
    printString = printString + ''.join(map(str, arg)) + "\n"

def indent():
    return indentL * indentStr
#    if indentL == 0:
#        return ("")
#
#    returnString = ""
#    global lastIndentWasStart
#    previousIterationWasStart = False
#
#    for n in range(indentL):
#        if n == indentL - 1 and not lastIndentWasStart and indentL != lastIndentL:
#            returnString += indentStr + "┌"
#            previousIterationWasStart = True
#        else:
#            previousIterationWasStart = False
#            returnString += indentStr + "│"
#    if previousIterationWasStart:
#        lastIndentWasStart = True
#    else:
#        lastIndentWasStart = False
#    lastIndentL = indentL
#    return (returnString)

def getParameterString(block,python_object):
    strToReturn = ""
    for i in block.get("parameters",[None]):
        if i != None:
            strToReturn += " " + getStrOfParam(i,python_object)
    return strToReturn

def printBlocksOfAbility(abilityID,python_object):
    global indentL
    for B in getAbilityWithID(abilityID,python_object).get("blocks",[]):
        if B == []:
            return

        indentL += 1

        if B["block_class"] == "control":
            strToPrint = B["description"]

            strToPrint += getParameterString(B,python_object)

            print_ (indent(),strToPrint)

            printBlocksOfAbility(B["controlScript"]["abilityID"],python_object)

        elif B["block_class"] == "conditionalControl":
            strToPrint = B["description"] + " "

            strToPrint = strToPrint + getStrOfParam(B["parameters"][0]["datum"]["params"][0],python_object)
            strToPrint = strToPrint + B["parameters"][0]["datum"]["description"]
            strToPrint = strToPrint + B["parameters"][0]["datum"]["params"][1]["value"]

            print_ (indent(),strToPrint)

            printBlocksOfAbility(B["controlScript"]["abilityID"],python_object)

            if B.get("controlFalseScript", None) != None:
                print_ (indent(),"else:")
                printBlocksOfAbility(B["controlFalseScript"]["abilityID"],python_object)

        else:
            strToPrint = B["description"]

            strToPrint += getParameterString(B,python_object)


            print_ (indent(),strToPrint)

        indentL -= 1

def printAllCode(JSON_data):
    global printString
    global indentL
    python_object = json.loads(JSON_data)
    printString = ""

    print_("────────────────────────────────────\nObjects:\n")
    for Obj in python_object["objects"]:
        indentL = 0
        print_ (Obj["name"],":",'''"''',Obj["text"],'''"''',"   (",Obj["xPosition"],",",Obj["yPosition"],")")

        for R in getRulesOfObject(Obj,python_object):
            indentL += 1
            print_ (indent(),"When ",getStrEventOfWhen(R,python_object))

            printBlocksOfAbility(R["abilityID"],python_object)
            print_ ("\n")

            indentL -= 1

    print_("\n────────────────────────────────────\nCustom Rules:\n")
    for Ability in python_object["customRules"]:
        indentL = 0
        print_ (Ability["name"],":")

        for R in getRulesOfObject(Ability,python_object):
            indentL += 1
            print_ (indent(),"When ",getStrEventOfWhen(R,python_object))

            printBlocksOfAbility(R["abilityID"],python_object)
            print_ ("\n")

            indentL -= 1


    return printString


if mode == "Independent":
    with open(fullDirectory,mode = "r",encoding = "utf-8") as f:
        f.seek(0)
        JSON_datastring = f.read()
        print (printAllCode(JSON_datastring))
