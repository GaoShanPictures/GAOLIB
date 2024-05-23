#   Copyright (C) 2022 GAO SHAN PICTURES

#   This file is a part of GAOLIB.

#   GAOLIB is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>

__author__ = "Anne Beurard"


import json
import os
import shutil
import traceback

try:
    import bpy
except:
    print("Blenderutils : import error bpy")

from PySide2 import QtCore, QtWidgets


def context_set(c, m=False):
    """Set current Context"""
    bpy.context.area.type = c
    if m:
        bpy.context.space_data.mode = m


def importAction(filepath):
    """Import one action from given blend file"""
    actionList = [act for act in bpy.data.actions]
    # load my .blend file
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.actions = data_from.actions  # collect action
    # Return first action from the blend file
    action = None
    for act in bpy.data.actions:
        if act not in actionList:
            action = act
            break
    return action


def importObject(filepath):
    """Import object from given blend file"""
    objectList = [o for o in bpy.data.objects]
    mainCollection = bpy.context.scene.collection
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.objects = data_from.objects  # collect object

    obj = None
    for o in bpy.data.objects:
        if o not in objectList:
            obj = o
            break
    # Link imported object to main collection
    if obj is not None:
        for new_obj in data_to.objects:
            if new_obj.name == obj.name:
                mainCollection.objects.link(new_obj)
    return obj


def ShowDialog(text, title=None):
    """Qt dialog box to display text message"""
    print(text)
    msgBox = QtWidgets.QMessageBox()
    msgBox.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowStaysOnTopHint)
    msgBox.setStyleSheet(
        "QWidget {background-color: #222; color: #b1b1b1}\nQPushButton:hover { color: green }"
    )
    if title:
        msgBox.setWindowTitle(title)
    msgBox.setText(text)
    msgBox.exec_()


def ShowMessageBox(message="", title="Message Box", icon="INFO"):
    """Blender info message"""

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def selectBones(jsonPath):
    """Read pose/animation json file and select listed bones of selected object"""
    itemdata = {}
    with open(jsonPath) as file:
        itemdata = json.load(file)
    bones = []
    for key in itemdata["metadata"].keys():
        if key == "boneNames":
            bones = itemdata["metadata"]["boneNames"]

    clearBoneSelection()

    objects = getSelectedObjects()
    if len(objects) != 1:
        ShowDialog(
            "NO OR TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action"
        )
        return
    obj = objects[0]
    if obj.type != "ARMATURE":
        ShowDialog("Please, select an ARMATURE object.", title="Abort action")
        return
    print("SELECT BONES")
    # Select bones
    for bone in bones:
        if obj.pose.bones.get(bone):
            obj.data.bones.get(bone).select = True
        else:
            print("Not found : " + bone)


def copyAnim(animDir):
    """Copy animation temp file to library"""
    tempDir = bpy.context.preferences.filepaths.temporary_directory
    tempAnim = os.path.join(tempDir, "animation.blend")
    tempCopy = os.path.join(animDir, "animation.blend")
    shutil.copyfile(tempAnim, tempCopy)


def getSelectedObjects():
    """Return list of selected objects"""
    objects = []
    for obj in bpy.data.objects:
        if obj.select_get():
            objects.append(obj)
    return objects


def getSelectedBones():
    """Return list of selected bones"""
    bones = []
    objects = getSelectedObjects()
    if len(objects) != 1:
        ShowDialog(
            "NO OR TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action"
        )
        return None
    if objects[0].type != "ARMATURE":
        ShowDialog("Please, select an ARMATURE object.", title="Abort action")
        return None
    for obj in objects:
        for bone in obj.data.bones:
            if bone.select:
                posebone = obj.pose.bones[bone.name]
                bones.append(posebone)
    return bones


def updateSelectionSet(infoWidget, add=True):
    # Get item json file
    item = infoWidget.item
    itemPath = item.path
    jsonFile = None
    for file in os.listdir(itemPath):
        if file == "selection_set.json":
            jsonPath = os.path.join(itemPath, file)
    if not jsonPath:
        ShowDialog("Found no selection_set.json in " + itemPath, title="Abort action")

    # Rend json
    itemdata = {}
    with open(jsonPath) as file:
        itemdata = json.load(file)
    # Init bones list with bones from json file
    bones = []
    for key in itemdata["metadata"].keys():
        if key == "boneNames":
            bones = itemdata["metadata"]["boneNames"]
    # Modify bones list with selected bones
    selectedBones = [bone.name for bone in getSelectedBones()]
    for bone in selectedBones:
        if add and bone not in bones:
            bones.append(bone)
        elif not add and bone in bones:
            bones.remove(bone)
    # Modify json datas
    itemdata["metadata"]["boneNames"] = bones
    itemdata["metadata"]["content"] = str(len(bones)) + " bone(s)"
    # write json
    with open(jsonPath, "w") as file:
        json.dump(itemdata, file, indent=4, sort_keys=True)
    # Update displayed informations
    infoWidget.contentLabel.setText(itemdata["metadata"]["content"])
    selectBones(jsonPath)


def pasteAnim(animDir, sourceFrameIn, sourceFrameOut, infoWidget):
    # Remember selection
    selection = getSelectedBones()
    if not selection:
        return
    # Read item infos on GAOLIB window
    quickPaste = infoWidget.quickPasteCheckBox.isChecked()
    nbFrames = sourceFrameOut - sourceFrameIn
    startFrameOption = infoWidget.startFrameComboBox.currentText()
    if startFrameOption == "From start frame":
        frameIn = bpy.context.scene.frame_start
        frameOut = frameIn + nbFrames
    elif startFrameOption == "From source start":
        frameIn = sourceFrameIn
        frameOut = sourceFrameOut
    else:
        frameIn = bpy.context.scene.frame_current
        frameOut = bpy.context.scene.frame_current + nbFrames

    # Get selected object
    selectedObjects = getSelectedObjects()
    if len(selectedObjects) != 1:
        ShowDialog(
            "NO OR TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action"
        )
        return
    selectedObject = selectedObjects[0]

    # Append action
    animPath = os.path.join(animDir, "animation.blend")

    fileActions = []
    with bpy.data.libraries.load(str(animPath)) as (data_from, _):
        fileActions = [act for act in data_from.actions]
    if len(fileActions) == 1:
        objectName = fileActions[0]
    else:
        ShowDialog(
            "COPIED FILE CONTAINS ZERO OR MORE THAN ONE ACTIONS.", title="Abort action"
        )
        return

    action = importAction(animPath)
    if action is None:
        ShowDialog("APPEND ACTION WENT WRONG.", title="Abort action")
        return
    # PASTE action
    if quickPaste:
        # Paste entire action in new action
        action.name = os.path.basename(animDir).split(".")[0] + "_ACTION"
        if selectedObject.animation_data is None:
            selectedObject.animation_data_create()
        selectedObject.animation_data.action = action
        ShowDialog("Quick Paste Action done !")

    else:
        # Paste into current action the keyframes corresponding to selected range
        action.name = "TEMP_ACTION"

        # Delete frame range anim
        for bone in selection:
            for frame in range(frameIn, frameOut + 1):
                if (
                    selectedObject.animation_data
                    and selectedObject.animation_data.action is not None
                ):
                    bone.keyframe_delete(data_path="location", frame=frame)
                    bone.keyframe_delete(data_path="rotation_euler", frame=frame)
                    bone.keyframe_delete(data_path="scale", frame=frame)

                    for key in bone.keys():
                        try:
                            bone.keyframe_delete(
                                data_path='["' + key + '"]', frame=frame
                            )
                        except:
                            # print('Impossible to delete keyframe for prop ' + key + ' for ' + bone.name + 'for frame ' + str(frame))
                            pass
                else:
                    break
        if selectedObject.animation_data is None:
            selectedObject.animation_data_create()
        # If no action on selected object, create one
        if selectedObject.animation_data.action is None:
            gaolibAction = bpy.data.actions.new("gaolib_action")
            selectedObject.animation_data.action = gaolibAction

        count_op = 0
        # Retrieve source action keyframe points and copy them into target action
        for i in range(len(action.fcurves)):
            fc = action.fcurves[i]
            for kp in fc.keyframe_points:
                sourceFrame = kp.co.x
                if sourceFrameIn <= sourceFrame <= sourceFrameOut:
                    data_path = fc.data_path
                    bone = None
                    try:
                        bone = eval(("selectedObject." + data_path).split("]")[0] + "]")
                    except Exception as e:
                        print("WARNING : " + str(e))
                    if bone in selection:
                        index = fc.array_index
                        value = kp.co.y
                        frame = frameIn + sourceFrame - sourceFrameIn

                        bpy.context.scene.frame_current = int(frame)
                        try:
                            index = fc.array_index
                            cmd = (
                                "selectedObject."
                                + data_path
                                + "["
                                + str(index)
                                + "] = "
                                + str(value)
                            )
                            exec(cmd)
                            count_op += 1
                        except TypeError:
                            index = -1
                            cmd = "selectedObject." + data_path + " = " + str(value)
                            if not "rotation_mode" in data_path:
                                exec(cmd)
                                count_op += 1
                            else:
                                rot = int(value)
                                rotmodeDict = {
                                    0: "QUATERNION",
                                    1: "XYZ",
                                    2: "XZY",
                                    3: "YXZ",
                                    4: "YZX",
                                    5: "ZXY",
                                    6: "ZYX",
                                    7: "AXIS_ANGLE",
                                }
                                cmd = (
                                    "selectedObject."
                                    + data_path
                                    + " = '"
                                    + rotmodeDict[rot]
                                    + "'"
                                )
                                exec(cmd)
                                count_op += 1

                        except Exception as e:
                            ShowDialog(
                                "Paste anim exception : " + str(e), title="Abort action"
                            )
                            return
                        count_op += 1
                        selectedObject.keyframe_insert(
                            data_path=data_path, index=index, frame=frame
                        )
            # if onePurcent != 0 and i % onePurcent == 0:
            #     # Print progress in console
            #     print(str(int(i * progressStep) + 5) + ' %')
        print("operations : " + str(count_op))

        # Group channels by bones
        bones = {}
        for fc in selectedObject.animation_data.action.fcurves:
            bone = fc.data_path.split('["')[1].split('"]')[0]
            if bone not in bones.keys():
                bones[bone] = []
            bones[bone].append(fc)

        for key in bones.keys():
            group = selectedObject.animation_data.action.groups.get(key)
            if not group:
                group = selectedObject.animation_data.action.groups.new(key)
            for fc in bones[key]:
                if fc.group == None:
                    fc.group = group

        bpy.data.actions.remove(action)
        ShowDialog("Paste animation done !")


def copyPose(poseDir):
    """Copy pose temporary file to library"""
    tempDir = bpy.context.preferences.filepaths.temporary_directory
    tempPose = os.path.join(tempDir, "copybuffer_pose.blend")
    tempCopy = os.path.join(poseDir, "pose.blend")
    shutil.copyfile(tempPose, tempCopy)


def getCurrentPose():
    """Return dict with current pose informations"""
    selection = []
    objects = getSelectedObjects()
    if len(objects) != 1:
        ShowDialog(
            "NO OR TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action"
        )
        return None
    if objects[0].type != "ARMATURE":
        ShowDialog("Please, select an ARMATURE object.", title="Abort action")
        return None
    for obj in objects:
        for bone in obj.data.bones:
            posebone = obj.pose.bones[bone.name]
            selection.append(posebone)

    currentPose = {}
    for selectedbone in selection:
        rotationMode = selectedbone.rotation_mode
        location = selectedbone.location.copy()

        if rotationMode != "QUATERNION":
            rotation = selectedbone.rotation_euler.copy()
        if rotationMode == "QUATERNION":
            rotation = selectedbone.rotation_quaternion.copy()
        scale = selectedbone.scale.copy()
        properties = {}
        for key in selectedbone.keys():
            try:
                properties[key] = eval("selectedbone." + key)
            except:
                properties[key] = eval('selectedbone["' + key + '"]')
        currentPose[selectedbone] = {
            "rotationMode": rotationMode,
            "location": location,
            "rotation": rotation,
            "scale": scale,
            "properties": properties,
        }
    return currentPose


def getRefPoseFromLib(poseDir, selection):
    """Retrieve pose from given poseDir directory"""
    selectionNames = [posebone.bone.name for posebone in selection]
    # Append pose object
    posePath = os.path.join(poseDir, "pose.blend")
    fileObjects = []
    with bpy.data.libraries.load(str(posePath)) as (data_from, _):
        fileObjects = [obj for obj in data_from.objects]
    if len(fileObjects) == 1:
        objectName = fileObjects[0]
    else:
        ShowDialog(
            "COPIED FILE CONTAINS ZERO OR MORE THAN ONE OBJECT", title="Abort action"
        )
        return

    refPose = importObject(posePath)
    pose = refPose.pose
    refBones = []
    for posebone in pose.bones:
        if posebone.name in selectionNames:
            posebone.bone.select = True
            refBones.append(posebone)
    return refPose


def pastePose(poseDir, flipped=False, blend=1, currentPose=None, additiveMode=False):
    """Paste pose from library on selected armature object for selected bones"""
    insertKeyframes = bpy.context.scene.tool_settings.use_keyframe_insert_auto
    # Remember selection
    selection = getSelectedBones()
    # Remember current pose
    if not currentPose:
        currentPose = getCurrentPose()
    # get pose selection set
    itemdata = {}
    jsonPath = os.path.join(poseDir, "pose.json")
    with open(jsonPath) as file:
        itemdata = json.load(file)
    selectionSetBones = []
    for key in itemdata["metadata"].keys():
        if key == "boneNames":
            selectionSetBones = itemdata["metadata"]["boneNames"]
    # Append pose object
    refPose = getRefPoseFromLib(poseDir, selection)
    pose = refPose.pose
    exceptionMessage = None
    # Copy properties from ref bones current object
    try:
        for posebone in pose.bones:
            for selectedbone in selection:
                if not selectedbone.name in selectionSetBones:
                    # ignore bones outside original pose selection set
                    continue
                if posebone.name == selectedbone.name:
                    # Manage if different rotation modes used (WARNING : axis angle not supported !)
                    rotationMode = posebone.rotation_mode

                    # AXIS_ANGLE rotation mode not supported !
                    if (
                        rotationMode == "AXIS_ANGLE"
                        or selectedbone.rotation_mode == "AXIS_ANGLE"
                    ):
                        # Delete pose
                        bpy.context.scene.collection.objects.unlink(refPose)
                        # Clean orphans
                        removeOrphans()
                        raise Exception(
                            "AXIS_ANGLE Rotation mode not supported, use QUATERNION or Euler."
                        )
                    elif (
                        rotationMode == "QUATERNION"
                        and currentPose[selectedbone]["rotationMode"] != "QUATERNION"
                    ):
                        currentPoseRotation = currentPose[selectedbone][
                            "rotation"
                        ].to_quaternion()
                    elif (
                        rotationMode != "QUATERNION"
                        and currentPose[selectedbone]["rotationMode"] == "QUATERNION"
                    ):
                        currentPoseRotation = currentPose[selectedbone][
                            "rotation"
                        ].to_euler()
                    elif rotationMode == currentPose[selectedbone]["rotationMode"]:
                        currentPoseRotation = currentPose[selectedbone]["rotation"]
                    else:
                        # Delete pose
                        bpy.context.scene.collection.objects.unlink(refPose)
                        # Clean orphans
                        removeOrphans()
                        raise Exception(
                            "Conversion between Rotation modes other than QUATERNION and Euler are not supported !"
                        )

                    selectedbone.rotation_mode = rotationMode
                    # Set pose for selected bones
                    for axis in range(3):
                        if not selectedbone.lock_location[axis]:
                            if additiveMode:
                                (
                                    blend * posebone.location[axis]
                                    + currentPose[selectedbone]["location"][axis]
                                )
                            else:
                                selectedbone.location[axis] = (
                                    blend * posebone.location[axis]
                                    + (1 - blend)
                                    * currentPose[selectedbone]["location"][axis]
                                )
                        if rotationMode != "QUATERNION":
                            if not selectedbone.lock_rotation[axis]:
                                if additiveMode:
                                    selectedbone.rotation_euler[axis] = (
                                        blend * posebone.rotation_euler[axis]
                                        + currentPoseRotation[axis]
                                    )
                                else:
                                    selectedbone.rotation_euler[axis] = (
                                        blend * posebone.rotation_euler[axis]
                                        + (1 - blend) * currentPoseRotation[axis]
                                    )
                        if not selectedbone.lock_scale[axis]:
                            if additiveMode:
                                selectedbone.scale[axis] = (
                                    blend * posebone.scale[axis]
                                    + currentPose[selectedbone]["scale"][axis]
                                    - blend
                                )
                            else:
                                selectedbone.scale[axis] = (
                                    blend * posebone.scale[axis]
                                    + (1 - blend)
                                    * currentPose[selectedbone]["scale"][axis]
                                )
                    if rotationMode == "QUATERNION":
                        if not selectedbone.lock_rotation_w:
                            if additiveMode:
                                selectedbone.rotation_quaternion[0] = (
                                    blend * posebone.rotation_quaternion[0]
                                    + currentPoseRotation[0]
                                    - blend
                                )
                            else:
                                selectedbone.rotation_quaternion[0] = (
                                    blend * posebone.rotation_quaternion[0]
                                    + (1 - blend) * currentPoseRotation[0]
                                )
                        for axis in range(3):
                            if not selectedbone.lock_rotation[axis]:
                                if additiveMode:
                                    selectedbone.rotation_quaternion[axis + 1] = (
                                        blend * posebone.rotation_quaternion[axis + 1]
                                        + currentPoseRotation[axis + 1]
                                    )
                                else:
                                    selectedbone.rotation_quaternion[axis + 1] = (
                                        blend * posebone.rotation_quaternion[axis + 1]
                                        + (1 - blend) * currentPoseRotation[axis + 1]
                                    )

                    for key in posebone.keys():
                        try:
                            exec("selectedbone." + key + " = posebone." + key)
                        except:
                            try:
                                exec(
                                    'selectedbone["'
                                    + key
                                    + '"] = posebone["'
                                    + key
                                    + '"]'
                                )
                            except:
                                print(
                                    "IMPOSSIBLE TO HANDLE PROPERTY "
                                    + key
                                    + " FOR "
                                    + selectedbone.name
                                )
                    # Key the pasted pose
                    if insertKeyframes:
                        selectedbone.keyframe_insert(data_path="rotation_mode")
                        for axis in range(3):
                            if not selectedbone.lock_location[axis]:
                                selectedbone.keyframe_insert(
                                    data_path="location", index=axis
                                )
                            if rotationMode != "QUATERNION":
                                if not selectedbone.lock_rotation[axis]:
                                    selectedbone.keyframe_insert(
                                        data_path="rotation_euler", index=axis
                                    )
                            if not selectedbone.lock_scale[axis]:
                                selectedbone.keyframe_insert(
                                    data_path="scale", index=axis
                                )
                        if rotationMode == "QUATERNION":
                            for axis in range(3):
                                if not selectedbone.lock_rotation[axis]:
                                    selectedbone.keyframe_insert(
                                        data_path="rotation_quaternion", index=axis + 1
                                    )
                                    selectedbone.keyframe_insert(
                                        data_path="rotation_quaternion", index=0
                                    )
                        for key in posebone.keys():
                            try:
                                selectedbone.keyframe_insert(
                                    data_path='["' + key + '"]'
                                )
                            except Exception as e:
                                print(
                                    "IMPOSSIBLE TO ADD KEYFRAME FOR PROP "
                                    + key
                                    + " FOR "
                                    + selectedbone.name
                                )
                    break
        # Group channels by bones
        if insertKeyframes:
            # Get selected object
            selectedObjects = getSelectedObjects()
            selectedObject = selectedObjects[0]
            bones = {}
            if not selectedObject.animation_data:
                selectedObject.animation_data_create()
            if not selectedObject.animation_data.action:
                selectedObject.animation_data.action = bpy.data.actions.new(
                    "anim_" + selectedObject.name + "Action"
                )
            for fc in selectedObject.animation_data.action.fcurves:
                try:
                    bone = fc.data_path.split('["')[1].split('"]')[0]
                    if bone not in bones.keys():
                        bones[bone] = []
                    bones[bone].append(fc)
                except:
                    pass
            for key in bones.keys():
                group = selectedObject.animation_data.action.groups.get(key)
                if not group:
                    group = selectedObject.animation_data.action.groups.new(key)
                for fc in bones[key]:
                    if fc.group == None:
                        fc.group = group
    except Exception as e:
        print("Blend Pose Exception : " + str(e) + "\n" + str(traceback.format_exc()))
        exceptionMessage = "Blend Pose Exception : " + str(e)
    # Delete pose
    bpy.context.scene.collection.objects.unlink(refPose)
    # Clean orphans
    removeOrphans()
    # Show message if exception
    if exceptionMessage:
        raise Exception(exceptionMessage)


def clearBoneSelection():
    """Unselect all bones"""
    for armature in bpy.data.armatures:
        for bone in armature.bones:
            bone.select = False


def removeOrphans():
    """Remove all orphan objects and collections"""
    doRemove = False
    for c in bpy.data.collections:
        if not c.users:
            doRemove = True

    while doRemove:
        removeOrphanCollections()
        doRemove = False
        for c in bpy.data.collections:
            if not c.users:
                doRemove = True

    for o in bpy.data.objects:
        if not o.users:
            bpy.data.objects.remove(o)


def removeOrphanCollections():
    """Remove orphan collections"""
    for c in bpy.data.collections:
        if not c.users:
            for o in c.objects:
                bpy.data.objects.remove(o)
            bpy.data.collections.remove(c)
