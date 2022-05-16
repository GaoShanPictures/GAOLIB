# GAOLIB

GAOLIB Copyright (C) 2022 GAO SHAN PICTURES is a GAO SHAN PICTURES Blender add-on developped to manage a library of poses and animations. This tool will help you store and re-use animations and poses in from and to different Blender files. 

The design of the user interface of this project, and its main purpose are inspired by Studio Library for Maya


## Latest Updates

- The GIF thumbnail for animations matches the framerate defined in Blender. Hovewer there may be some limitations with high framerates, for instance playing a 120 fps GIF happens to be much slower than a 60 fps GIF, probably due to some limitations from the device or from the Qt widgets. 

- When applying a pose from the library, you can choose to blend it with the current pose. The pose used as 'current pose' is the one set in the scene at the moment you move the slider for the first time. If you modify the pose in the scene, to take it into account as the current pose, you will have to select another item in the library and select again the pose you need to reset the 'current pose'. 
<p align="center">
  <img src="https://user-images.githubusercontent.com/103406493/168264512-6f607fda-1383-40c7-b0ac-5cadaffd1df8.png" />
</p>

- You can now choose different colors for the folder icons !  

- A new item type is now available in GAOLIB : the Selection set to store a list of bones.
<p align="center">
  <img src="https://user-images.githubusercontent.com/103406493/168264364-d7e7c186-8f14-4801-8f97-18831f44e750.png" />
</p>

- Former note : 'In order to remove properly the add-on from Blender, the user has to do it from a Blender session in which the Gaolib main window has not been opened. Otherwise, when trying to remove the add-on it will raise an Error in Windows (WinError 32:  The process cannot access the file because it is being used by another process).' bug has been fixed ! However, after installing a new version of GAOLIB, you may need to close and reopen Bender (Read more about it in the note section).

## Prerequisite
GAOLIB works with Blender 2.93. It has not fully been tested on Blender 3, but the first tests seem to be working as well. 

## Installation

See the installation tuto here : https://vimeo.com/698120255/b6e66c4152

Download the zip of the add-on and install it in the 'Add-ons' section of the Blender preferences : 

Edit > Preferences > Add-ons > Install... > Select the zip file in your files > Install Add-on.

Then enable the add-on.
This add-on uses PySide2 and imageio as external dependencies. They can be installed directly from the add-on preferences by clicking on the 'Install dependencies' button. 

In case there is any problem with the installed dependencies, an 'Uninstall dependencies' button is also available. To complete the uninstallation, the user is asked for confirmation in the system console for each dependency used. 


## Usage
See the Demo here : https://vimeo.com/698120055/2228caa23d

After installing, the GAOLIB Pannel should now be available in Blender 3D View.

WARNING : The user has to define a non empty path in the Blender preferences, File Paths section for Temporary files. If not, he/she won't be able to create new items in the library.

<p align="center">
  <img src="https://user-images.githubusercontent.com/103406493/162702699-6e96c988-5fd8-4b09-b8e6-ad86f8cd86e4.png" />
</p>

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

<p align="center">
  <img src="https://user-images.githubusercontent.com/103406493/162738690-006e8049-826a-43b1-9f1b-ea4fec5c2bf3.png" width="600"/>
</p>

## Note
This project is the first version of a work in progress. We are aware that some things can be improved and we are still looking for a way to change them. Amongst them : 

- The user has to define a non empty path in the Blender preferences, File Paths section for Temporary files. If not, he/she won't be able to create new items in the library.

- The user has to choose a ROOT location for his/her library where he/she has all the writing rights.

- For now, in order to create an animation/pose item in the library, the user has to go through 4 steps after clicking '+'> New animation. This process would be more user friendly if it were lighter : 
	
	-- One click on the camera button in the Gaolib Window: Remember the current render path, and set the render path to the temp directory to be able to retrieve the files generated by the creation of the item
	
	-- One click on the Create Pose/Animation button in the Gaolib toolbox : Triggers the render and create the temporary files needed for the item creation
	
	-- One click on the camera button in the Gaolib Window : Set back the old render path and gves a preview of the iem thumbnail
	
	-- One click on the Save Pose/Animation button in the Gaolib window : Actually stores the files related to the pose/animation item in the library.

- To install a new version of GAOLIB, you have to remove the previous version from the addons and install the new zip you've downloaded here. Note that Blender takes the new changed into account if in the same session the old version of GAOLIB hasn't been used. The first time you install a new version, if some things don't work properly, try to close Blender and reopen it. 


## License
Published under GPLv3 license.

## Author
Anne Beurard for GAO SHAN PICTURES

With the help of Beorn Leonard 

Note :

The dependencies management is adapted from Robert Guetzkow work available here :
[https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies](https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies "https://github.com/robertguetzkow/blender-python-examples/tree/master/add_ons/install_dependencies")
