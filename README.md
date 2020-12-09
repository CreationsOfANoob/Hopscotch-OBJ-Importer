# Hopscotch-OBJ-Importer
Python script to import .obj 3D models into a Hopscotch project file.

The .obj file needs to be placed in the main folder. The .json draft files are placed in Hopscotch_JSON_GUI/json_projects

Requirements:
* Numpy
* Python 3.x

I downloaded a program called Anaconda to manage Python packages, it seems to be really useful. (then use Spyder via Anaconda)

The obj file needs to contain only triangulated faces (no quads or n-gons). Materials are supported, will be included in the HS project as a material index variable for each face.

Use the template .json project. The way I wrote the importer requires a specific object and some specific variables to exist in the project.
This could probably be improved upon by, for example, including a formatted obj file as a string in the actual HS project. 
