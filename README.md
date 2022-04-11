# GAOLIB

GAOLIB is a GAO SHAN PICTURES Blender add-on developped to manage a library of poses and animations. This tool will help you store and re-use animations and poses in from and to different Blender files. 

## Prerequisite
GAOLIB works with Blender 2.93. It has not fully been tested on Blender 3, but the first tests seem to be working as well. To install it, please visit the Blender Download web page : https://www.blender.org/download/.

## Installation
Download the zip of the add-on and install it in the 'Add-ons' section of the Blender preferences : 

Edit > Preferences > Add-ons > Install... > Select the zip file in your files > Install Add-on.

Then enable the add-on.
This add-on uses PySide2 and imageio as external dependencies. They can be installed directly from the add-on preferences by clicking on the 'Install dependencies' button. 

In case there is any problem with the installed dependencies, an 'Uninstall dependencies' button is also available. To complete the uninstallation, the user is asked for confirmation in the system console for each dependency used. 


## Usage
The GAOLIB Pannel should now be available in Blender 3D View. 
Four operators are available : 

- GAOLIB  : Starts the main window of the tool. On the first use, you will be asked to define the location of the root folder of your library. A ROOT directory will be created in the given location.

- Create Pose : Creates a new pose item to be stored in the library. 
To use after the following actions in the main window. 
	'+' button > New Pose > 'Camera' button. The pose is created if the selected object in the scene is an armature and the mode is set to Pose Mode. The pose only contains the selected bones.

- Create Animation : Creates a new animation item to be stored in the library. 
To use after the following actions in the main window. 
	'+' button > New Animation> 'Camera' button.
The animation is created if the selected object in the scene is an armature and the mode is set to Pose Mode. The pose only contains the selected bones.

- Show overlay hidden : After creating a pose/animation, some overlays can be hidden for its preview to be clean. This button sets back the deactivated overlays.


## Author
Anne Beurard

Note :

The dependencies management is adapted from Robert Guetzkow work available here :
[https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies](https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies "https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies")
