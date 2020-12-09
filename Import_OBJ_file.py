from os import listdir
from os.path import isfile, join, dirname, abspath
path_to_script = dirname(abspath(__file__))
import sys
sys.path.append(join(path_to_script,"Hopscotch_JSON_GUI"))
import HopscotchFileFunctions as HSF
import json
from numpy import array, dot

def exit_cancel(reason = None):
    if reason == None:
        sys.exit("Cancelled\n----------")
    else:
        sys.exit("Cancelled: " + reason + "\n----------")


coords_string = ""
faces_string = ""
list_of_coords = []
list_of_faces = []
list_of_colors = []
material = []
ability_id = ""
loaded_json = ""
obj_file_name = "outside.obj"


#Handle the .obj file
def return_only_first_number(string = "e.g 24//26"):
    return int(string.split("/")[0])

def return_normal_index(string = "e.g 24//26"):
    return int((string.split("/")[2]).split()[0])

def return_according_coord(int_):
    global list_of_coords
    return list_of_coords[int_ - 1]

def calculate_color(normal):
    color = max(-1.0,array(normal).dot(array([1.0,0.5,0.1])))
    return color

with open(obj_file_name, mode="r") as f:
    lines = f.read().splitlines()
    face_index = 0
    material_name = ""
    for line in lines:
        if line[0:2] == "v ":
            coordinate = list(map(float,line[2:].split()))
            list_of_coords.append(coordinate)
        elif line[0:2] == "f ":
            face = list(map(return_only_first_number,line[2:].split()))
            face.append(return_normal_index(line[2:]))
            list_of_faces.append(face)
            material.append(material_name)
            face_index += 1

        elif line[0:2] == "vn":
            face_normal = list(map(float,line[3:].split()))
            face_color = calculate_color(face_normal)
            list_of_colors.append(face_color)
        elif line[0:7] == "usemtl ":
            material_name = line[-3:]

#All below handles interaction with draft

def add_blocks(face_data, color_index, change_material = False):
    global loaded_json
    global ability_id
    variable_names = ["VX1","VY1","VZ1","VX2","VY2","VZ2","VX3","VY3","VZ3",
    "Base Brightness", "Material"]
    n3 = 0
    for n1 in range(3):
        for n2 in range(3):
            #Add coordinate
            loaded_json = HSF.addBlockToAbility(loaded_json, ability_id,
                block_type="set_variable", variable_name=variable_names[n3],
                value=str(face_data[n1][n2]))
            n3 += 1

    #Set face color
    loaded_json = HSF.addBlockToAbility(loaded_json, ability_id,
        block_type="set_variable", variable_name=variable_names[n3],
        value=str(list_of_colors[color_index - 1]))

    #Change material
    if not change_material:
        loaded_json = HSF.addBlockToAbility(loaded_json, ability_id,
            block_type="increase_variable", variable_name=variable_names[10],
            value=1)

    #Add ability
    loaded_json = HSF.addBlockToAbility(loaded_json, ability_id,
        block_type="ability", ability_name="Increase faces by 1")


JSON_files = listdir(join(path_to_script,"Hopscotch_JSON_GUI","json_projects"))

print ("Warning: This script does not work on hopscotch player versions below 1.3.4")
print ("----------\n")
print ("Available drafts:\n")
number = 0
for file_name in JSON_files:
    number += 1
    print (file_name, "(",number,")")

print ("\nChoose a file to open (1 - " + str(number) + "): ",end = "")
fileToOpen = 0
try:
    fileToOpen = int(input("")) - 1
except ValueError:
    exit_cancel("that number aint gonna work")

fullDirectory = join(path_to_script,"Hopscotch_JSON_GUI","json_projects",
JSON_files[fileToOpen])

if input("Do you want to proceed? This will overwrite the file, adding "
        + obj_file_name + " (yes or no)\n") != "yes":
    exit_cancel()

#Open file
print ("\nOpening file...")

with open(fullDirectory, mode = 'r' , encoding= "utf-8") as file_info:
    file_text = file_info.read()
    loaded_json = json.loads(file_text)
    #print (loaded_json)

#Find correct ability to add .obj file to
print ("Searching for object...")
object_name = "Right Triangle 3"

if HSF.getObjectWithName(object_name,loaded_json) != None:
    object_ = HSF.getObjectWithName(object_name,loaded_json)
    rule_id = HSF.getObjectWithName(object_name,loaded_json)["rules"][1]
    ability_id = HSF.getWhenWithID(rule_id,loaded_json)["abilityID"]
else:
    exit_cancel("Object Right Triangle was not found.")

#Remove existing blocks in ability
print ("Clearing ability...")
loaded_json = HSF.emptyAbility(ability_id, loaded_json)

#Add .obj file
print ("Adding blocks...")
print (material, len(material))
index = 0
for int_list in list_of_faces:
    change_material = (material[index] == material[max(index - 1, 0)])
    add_blocks(list(map(return_according_coord, int_list[:-1])), int_list[-1],
        change_material)
    index += 1
#    print (list(map(return_according_coord,int_list)))

#Save file
with open(fullDirectory, mode = 'w' , encoding='utf-8') as f:
    f.write(json.dumps(loaded_json, sort_keys=True, separators=(',', ': ')))
    #print (json.dumps(loaded_json, sort_keys=True, separators=(',', ': ')))

print ("Done! Saved edited file to " + fullDirectory + "\n\n----------")
