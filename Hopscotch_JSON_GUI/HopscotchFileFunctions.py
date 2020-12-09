from copy import deepcopy


block_type_templates = {"set_variable":{"block_class" : "method", "type" : 45,
"description" : "Set", "parameters" : [{"defaultValue" : "", "value" : "",
"key" : "", "datum" : { "type" : 8004, "variable" : "",
"description" : "Variable"}, "type" : 47}, {"defaultValue" : "10",
"value" : "10", "key" : "to", "type" : 48}]},"increase_variable":{"block_class":
"method","description":"Increase","type":44,"parameters":[{"defaultValue":"",
"value":"","key":"","datum":{"type":8003,"variable":"","description":"Variable"}
,"type":47},{"defaultValue":"1","value":"1","key":"by","type":48}]},"ability":
{"block_class":"control","description":"","controlScript":{"abilityID":""},
"type":123},"wait":{"parameters":[{"defaultValue":"500","value":"",
"key":"milliseconds","type":42}],"description":"Wait","type":35,
"block_class":"method"}}


def getRules(fileDictionary):
    return fileDictionary["rules"]

def getCustomRules(fileDictionary):
    return fileDictionary["customRules"]

def getObjects(fileDictionary):
    return fileDictionary["objects"]

def getAbilities(fileDictionary):
    return fileDictionary["abilities"]

def getVariables(fileDictionary):
    return fileDictionary["variables"]


def getAbilityWithID(ID, fileDictionary):
    for ability in getAbilities(fileDictionary):
        if ability["abilityID"] == ID:
            return ability

def getVariableWithID(ID, fileDictionary):
    for variable in getVariables(fileDictionary):
        if variable["objectIdString"] == ID:
            return variable


def getWhenWithID(ID, fileDictionary):
    for rule in getRules(fileDictionary):
        if rule["id"] == ID:
            return rule
    for rule in getCustomRules(fileDictionary):
        if rule["id"] == ID:
            return rule

def getCustomRuleWithName(name, fileDictionary):
    for rule in getCustomRules(fileDictionary):
        if rule["name"] == name:
            return rule

def getAbilityWithName(name, fileDictionary):
    for ability in getAbilities(fileDictionary):
        if ability.get("name",0) != 0:
            if ability["name"] == name:
                return ability


def getVariableWithName(name, fileDictionary):
    for variable in getVariables(fileDictionary):
        if variable["name"] == name:
            return variable
    print("Variable", name, "was not found")


def getObjectWithName(name, fileDictionary):
    for object_ in getObjects(fileDictionary):
        if object_["name"] == name:
            return object_


def getRulesOfObject(HSobject, fileDictionary):
    rules = []
    IDs = HSobject["rules"]
    print (IDs,"\n")
    for rule in fileDictionary["rules"]:
        print (rule["id"],"\n\n")
        if rule["id"] in IDs:
            rules.append(rule)
            print ("added")
    print (rules)
    return rules


def getStrOfDatum(datum, filedictionary):
    if datum.get("params",0) != 0:
        if len(datum["params"]) == 1:
            strToReturn = getStrOfParam(datum["params"][0],filedictionary)# + " " + datum["description"]
        else:
            strToReturn = getStrOfParam(datum["params"][0],filedictionary) + " " + datum["description"] + getStrOfParam(datum["params"][1],filedictionary)
    else:
        if datum.get("variable",0) == 0:
            strToReturn = datum["description"]
        else:
            strToReturn = getVariableWithID(datum["variable"],filedictionary)["name"]
    return strToReturn

def getStrOfParam(param, filedictionary):
    if param.get("datum",0) != 0:
        return "(" + getStrOfDatum(param["datum"],filedictionary) + ")"
    else:
        return param["value"]


def getStrEventOfWhen(HSrule, filedictionary):
    result = ""
    if HSrule["parameters"][0]["datum"]["block_class"] == "conditionalOperator":
        result = result + getStrOfParam(HSrule["parameters"][0]["datum"]["params"][0],filedictionary)
        result = result + HSrule["parameters"][0]["datum"]["description"]
        result = result + HSrule["parameters"][0]["datum"]["params"][1]["value"]
    else:
        result = HSrule["parameters"][0]["datum"]["description"]
    return result

def emptyAbility(ability_id, fileDictionary):
    getAbilityWithID(ability_id, fileDictionary)["blocks"] = []
    return fileDictionary

def addBlockToAbility(fileDictionary, ability_id, block_type = "set_variable",
    variable_name = None, value = 0, ability_name = None):
    global block_type_templates

    block_to_add = deepcopy(block_type_templates[block_type])

    if block_type in ["set_variable", "increase_variable"]:
        if variable_name != None:
            variable_id = getVariableWithName(variable_name,
                    fileDictionary)["objectIdString"]
            variable_type = getVariableWithName(variable_name,
                    fileDictionary)["objectIdString"]

            if variable_type == 8000:
                block_to_add["parameters"][0]["datum"]["type"] = 8004
            elif variable_type == 8003:
                block_to_add["parameters"][0]["datum"]["type"] = 8003

            if variable_id != None:
                block_to_add["parameters"][0]["datum"]["variable"] = variable_id
        block_to_add["parameters"][1]["value"] = value

    elif block_type == "ability":
        add_ability_id = getAbilityWithName(ability_name, fileDictionary)["abilityID"]
        block_to_add["controlScript"]["abilityID"] = add_ability_id
        block_to_add["description"] = ability_name
    elif block_type == "wait":
        block_to_add["parameters"][0]["value"] = str(value)


    getAbilityWithID(ability_id, fileDictionary)["blocks"].append(block_to_add)

    return fileDictionary

def abilityExists(ID, fileDictionary):
    for i in fileDictionary["abilities"]:
        if i["abilityID"] == ID:
            return True
    return False

def remove_emoji(stringToFix):
    import re
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\ud83d\u0000-\uddff"  # symbols & pictographs (2 of 2)
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return (emoji_pattern.sub(r'', stringToFix)) # no emoji
