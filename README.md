# GAOLIB

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

GAOLIB Copyright (C) 2022 GAO SHAN PICTURES is a GAO SHAN PICTURES Blender add-on developped to manage a library of poses and animations. This tool will help you store and re-use animations and poses (and constraints !) in from and to different Blender files. 

The design of the user interface of this project, and its main purpose are inspired by Studio Library for Maya


## Latest Updates
- GAOLIB Now Available for blender 4.5 ! 
<!--
Warning : In Preferences > System > Display Graphics the choosing Vulkan for Backend seems a bit less instable than OpenGL (less crashes)
-->

- New Feature : Option to Paste or Blend mirrored pose (not available on items created with the previous versions of Gaolib)

- The four steps of creating an item is now just 2 : click the camera button + click Save, and your new item is created !

- New Feature : New CONSTRAINT SET item available.

- New Features : Recursive display of items in central view option, apply pose when double click item option and blend pose when wheel click option are available in the settings window.

- Former note : 'In order to remove properly the add-on from Blender, the user has to do it from a Blender session in which the Gaolib main window has not been opened. Otherwise, when trying to remove the add-on it will raise an Error in Windows (WinError 32:  The process cannot access the file because it is being used by another process).' bug has been fixed ! However, after installing a new version of GAOLIB, you may need to close and reopen Bender (Read more about it in the note section).

## Prerequisite
GAOLIB works with Blender 2.93 and above.

## Installation

See the installation tuto here : https://vimeo.com/698120255/b6e66c4152

Download the zip of the add-on and install it in the 'Add-ons' section of the Blender preferences : 

Edit > Preferences > Add-ons > Install... > Select the zip file in your files > Install Add-on.

Then enable the add-on.
This add-on uses Pyside6 and imageio as external dependencies. They can be installed directly from the add-on preferences by clicking on the 'Install dependencies' button. 

In case there is any problem with the installed dependencies, an 'Uninstall dependencies' button is also available. To complete the uninstallation, the user is asked for confirmation in the system console for each dependency used. REMEMBER TO OPEN THE CONSOLE BEFORE TRYING TO UNINSTALL THE DEPENDENCIES.

### WARNING 

- To install GAOLIB, the user needs to run Blender as administrator to be able to install properly the dependencies (May apply to Windows users only).

- For some Linux users, the PySide6 dependency may need the user to manually install an additional lib called libxcb-cursor0 to work properly. Running the following command on a debian based system should work:

sudo apt install libxcb-cursor0

## Usage
See the Demo here : https://vimeo.com/698120055/2228caa23d

Note : The tool has evolved since the creation of this video, some processes have been improved.

After installing, the GAOLIB Pannel should now be available in Blender 3D View.

WARNING : The user has to define a non empty path in the Blender preferences, File Paths section for Temporary files. If not, he/she won't be able to create new items in the library.

<p align="center">
  <img src="https://github.com/user-attachments/assets/6e208eb8-5e3c-4981-9bb2-4ebf6ef9f216" />
</p>

### Three operators are available : 

<p align="center">
  <img src="https://user-images.githubusercontent.com/103406493/162738690-006e8049-826a-43b1-9f1b-ea4fec5c2bf3.png" width="600"/>
</p>

- GAOLIB  : Starts the main window of the tool. On the first use, you will be asked to define the location of the root folder of your library. A ROOT directory will be created in the given location.

- Get context : When the Gaolib window is created, it uses the context of the current 3D View from which it has been called. If this region is deleted, the user has to use Get context form another 3D View to be able to create new items.

- Show overlay hidden : After creating a pose/animation, some overlays can be hidden for its preview to be clean. This button sets back the deactivated overlays.


### Creating a new item (+ button in the main window) : 

<p align="center">
  <img src="https://github.com/user-attachments/assets/aaf042d5-6bd6-43a3-b5a3-901a33bdd8d4" width="150"/>
</p>

- New Pose : 
Click the Camera button to create a thumbnail for the pose item, choose a name and click save.
The pose is created if the selected object in the scene is an armature and the mode is set to Pose Mode. The pose only contains the selected bones.

- New Animation : 
Click the Camera button to create a GIF for the pose item, choose a name and the parameters and click save.
The animation is created if the selected object in the scene is an armature and the mode is set to Pose Mode. The pose only contains the selected bones.

- New Constraint Set : To store the bone constraints linking two objects.
Select the objects linked by a (bone) constraint, go to POSE mode, select the bones involved in the constraint and create the item. To apply the constrain item, select the objects and bones involved, if they are not the same objects as when for the item creation, match the objects in the comboboxes and apply (Warning : For now, applying a stored "child of" constraint does not automatically call "set inverse"). The CONSTRAINT SET item does not handle the pose of the objects. To have the same pose, create a POSE item for each object in addition to the CONSTRAINT SET and apply each one of them.

- New Selection Set :
Store a selection of bones.

- New Folder :
Organize your library into a hierarchy of folders.

## Note
This project is a work in progress. We are aware that some things can be improved and we are still looking for a way to change them. Amongst them : 

- The user has to define a non empty path in the Blender preferences, File Paths section for Temporary files. If not, he/she won't be able to create new items in the library.

- The user has to choose a ROOT location for his/her library where he/she has all the writing rights.

- EDIT : FIXED ! For now, in order to create an animation/pose item in the library, the user has to go through 4 steps after clicking '+'> New animation. This process would be more user friendly if it were lighter : 
	
	-- One click on the camera button in the Gaolib Window: Remember the current render path, and set the render path to the temp directory to be able to retrieve the files generated by the creation of the item
	
	-- One click on the Create Pose/Animation button in the Gaolib toolbox : Triggers the render and create the temporary files needed for the item creation
	
	-- One click on the camera button in the Gaolib Window : Set back the old render path and gves a preview of the iem thumbnail
	
	-- One click on the Save Pose/Animation button in the Gaolib window : Actually stores the files related to the pose/animation item in the library.

- To install a new version of GAOLIB, you have to remove the previous version from the addons and install the new zip you've downloaded here. Note that Blender takes the new changed into account if in the same session the old version of GAOLIB hasn't been used. The first time you install a new version, if some things don't work properly, try to close Blender and reopen it. 

- The pose pasting only supports Quaternion and Euler rotation modes. Axis angles are not supported. 

## ABOUT THE DEPENDENCIES MANAGEMENT : 
![image](https://user-images.githubusercontent.com/103406493/180926775-3db48c11-2030-420c-bb69-1530f9ca2a7f.png)

GAOLIB requires the following packages to be installed : PySide6 and imageio. It should be possible to install them from the Blender Preferences, in the Add-ons section, selecting the GAOLIB Add-on. However, if the installation doesn't work (cf image above), the users has to install the dependencies on their own, that is to say in Blender's python console, the commands 'import PySide6' and 'import imageio' should not raise any error.
There are several ways to acheive that. 

- One of them uses pip, for me the command to run in a terminal looks like this (make sure you give the right path to blender's python.exe, for each version of blender h e path will change, see one example below): 

"C:/Program Files/Blender Foundation/Blender #.#/#.#/python/bin/python.exe" -m pip install PySide6

"C:/Program Files/Blender Foundation/Blender #.#/#.#/python/bin/python.exe" -m pip install imageio

- Another way, if you already have the dependency package installed somewhere for a python using the same version than the python in blender, in Blender's python console you can use : 

import sys

sys.path.append('/location/of/your/dependency')

Note that with this method, you'd have to call these two lines for each dependency every time you reopen Blender.


## License
Published under GPLv3 license.

## Author
Anne Beurard for GAO SHAN PICTURES

With the help of Beorn Leonard 

Note :

The dependencies management is adapted from Robert Guetzkow work available here :
[https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies](https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies "https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies")
