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
    import bpy_extras.anim_utils as anim_utils
except:
    print("Blenderutils : import error bpy")


from PySide6 import QtCore, QtWidgets


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


def importAllActions(filepath):
    """Import ALL actions from given blend file"""
    actionList = [act for act in bpy.data.actions]
    # load my .blend file
    with bpy.data.libraries.load(filepath) as (data_from, data_to):
        data_to.actions = data_from.actions  # collect action
    # Return first action from the blend file
    importedActions = []
    for act in bpy.data.actions:
        if act not in actionList:
            importedActions.append(act)
    return importedActions


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
                # mainCollection.objects.link(new_obj)
                new_obj.select_set(False)
                new_obj.hide_viewport = True
                new_obj.hide_render = True

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


def selectConstraintBones(jsonPath, pairingDict):
    """Read constraint json file and select listed bones of selected object"""
    pbList = []
    clearBoneSelection()
    # read json
    itemdata = {}
    with open(jsonPath) as file:
        itemdata = json.load(file)
    if "constraintData" in itemdata.keys():
        constraintData = itemdata["constraintData"]
    else:
        ShowDialog("Found no constraint data in " + jsonPath, title="Abort action")
        return
    # get selection
    objects = getSelectedObjects()
    # deselect all objects
    toggleObjectSelection(objects, select=False)
    # select bones
    for objName in constraintData.keys():
        boneConstraints = constraintData[objName]["bone_constraints"]
        constraintToObject = None
        for selected in objects:
            if selected.name == pairingDict[objName]["object"]:
                constraintToObject = selected
                break
        if not constraintToObject:
            pbList.append(
                "Did not find "
                + pairingDict[objName]["object"]
                + " to be paired with "
                + objName
                + " amongst selected objects"
            )
            continue
        # select object
        constraintToObject.select_set(True)
        bpy.context.view_layer.objects.active = constraintToObject
        # select bones
        if not constraintToObject.pose:
            pbList.append(constraintToObject.name + " object does not have any bones.")
            continue
        for boneName in boneConstraints.keys():
            bone = constraintToObject.pose.bones.get(boneName)
            if not bone:
                pbList.append(
                    "Did not find bone " + boneName + " in " + constraintToObject.name
                )
                continue
            # select bone
            bone.select = True
    if len(pbList):
        ShowDialog(
            "Some problems occured while selecting bones : \n" + "\n".join(pbList),
            title="Select bones Warning",
        )


def selectMultiPoseBones(jsonPath, pairingDict):
    pbList = []
    itemdata = {}
    with open(jsonPath) as file:
        itemdata = json.load(file)

    itemType = itemdata["metadata"]["type"]

    if itemType not in ["MULTI POSE", "MULTI ANIMATION"]:
        print("Operation not available for " + itemType)
        return
    clearBoneSelection()
    # get bone names from json
    boneDict = {}
    for key in itemdata["metadata"].keys():
        if key == "boneNames":
            boneDict = itemdata["metadata"]["boneNames"]
    # get selected object
    objects = getSelectedObjects()
    for objName in boneDict.keys():
        # ignore objects with not pairing
        if pairingDict[objName]["object"] == "":
            continue
        sceneObj = None
        for selected in objects:
            if selected.name == pairingDict[objName]["object"]:
                sceneObj = selected
                break
        if not sceneObj:
            pbList.append(
                "Did not find "
                + pairingDict[objName]["object"]
                + " to be paired with "
                + objName
                + " amongst selected objects"
            )
            continue
        # select bones
        if not sceneObj.pose:
            pbList.append(sceneObj.name + " object does not have any bones.")
            continue
        for boneName in boneDict[objName]:
            bone = sceneObj.pose.bones.get(boneName)
            if not bone:
                pbList.append("Did not find bone " + boneName + " in " + sceneObj.name)
                continue
            # select bone
            bone.select = True
    if len(pbList):
        ShowDialog(
            "Some problems occured while selecting bones : \n" + "\n".join(pbList),
            title="Select bones Warning",
        )


def selectBones(jsonPath):
    """Read pose/animation json file and select listed bones of selected object"""
    itemdata = {}
    with open(jsonPath) as file:
        itemdata = json.load(file)

    itemType = itemdata["metadata"]["type"]
    clearBoneSelection()
    if itemType != "CONSTRAINT SET":
        # get bone names from json
        bones = []
        for key in itemdata["metadata"].keys():
            if key == "boneNames":
                bones = itemdata["metadata"]["boneNames"]
        # get selected object
        objects = getSelectedObjects()
        if len(objects) != 1:
            ShowDialog(
                "NO OR TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.",
                title="Abort action",
            )
            return
        obj = objects[0]
        if obj.type != "ARMATURE":
            ShowDialog("Please, select an ARMATURE object.", title="Abort action")
            return
        # Select bones
        for bone in bones:
            if obj.pose.bones.get(bone):
                if obj.data.bones.get(bone).hide:
                    obj.data.bones.get(bone).hide = False
                for collection in obj.data.bones.get(bone).collections:
                    collection.is_visible = True
                    break
                obj.pose.bones.get(bone).select = True
            else:
                print("Not found : " + bone)
        # check selected bones
        pbList = []
        selectedBones = getSelectedBones()
        for bone in bones:
            found = False
            for posebone in selectedBones:
                if posebone.name == bone:
                    found = True
                    break
            if not found:
                pbList.append(bone)
        if len(pbList):
            ShowDialog(
                "Some bones could not be selected (visibility turned off or non-existent):\n\n"
                + "\n".join(pbList),
                title="Warning",
            )


def keySelectedBonesForFrame(frame, selectedBones=None):
    # key first frame
    bpy.context.scene.frame_set(frame)
    if not selectedBones:
        selectedBones = [b for b in bpy.context.selected_pose_bones]
    for bone in selectedBones:
        bone.keyframe_insert(data_path="rotation_mode", frame=frame)
        for axis in range(3):
            if not bone.lock_location[axis]:
                bone.keyframe_insert(data_path="location", index=axis, frame=frame)
            if not bone.lock_rotation[axis]:
                bone.keyframe_insert(
                    data_path="rotation_euler", index=axis, frame=frame
                )
            if not bone.lock_scale[axis]:
                bone.keyframe_insert(data_path="scale", index=axis, frame=frame)
        for key in bone.keys():
            try:
                bone.keyframe_insert(data_path='["' + key + '"]', frame=frame)
            except Exception as e:
                pass


def createActionsForLib(objects, frameIn, frameOut, keyLastFrame):
    actionCopies = {}
    # get all object action and slots
    objectActions = []
    for o in objects:
        if o.animation_data and o.animation_data.action:
            action = o.animation_data.action
            slot = o.animation_data.action_slot
            objectActions.append((o, action, slot))
    # create copy of actions
    countActions = 1
    for t in objectActions:
        obj, action, slot = t[0], t[1], t[2]
        if action.name not in actionCopies.keys():
            newAction = action.copy()
            newAction.name = "GAOLIB_Animation_" + str(countActions)
            actionCopies[action.name] = newAction
            countActions += 1
        else:
            newAction = actionCopies[action.name]
        obj.animation_data.action = None
        obj.animation_data.action = newAction
    # clean copies from unused slots
    for key in actionCopies.keys():
        newAction = actionCopies[key]
        toCleanSlots = []
        for slot in newAction.slots:
            if not len(slot.users()):
                toCleanSlots.append(slot)
        for slot in toCleanSlots:
            newAction.slots.remove(slot)
    selectedBones = getSelectedBones(allowMulti=True)
    # key first frame
    keySelectedBonesForFrame(frameIn, selectedBones=selectedBones)
    if keyLastFrame:
        keySelectedBonesForFrame(frameOut, selctedBones=selectedBones)

    return actionCopies


def copyAnim(animDir):
    """Copy animation temp file to library"""
    tempDir = bpy.context.preferences.filepaths.temporary_directory + "/gaolib_temp"
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


def toggleObjectSelection(objects, select=False):
    """Unselect all objects"""
    for obj in objects:
        obj.select_set(select)


def getSelectedBones(allowMulti=False):
    """Return list of selected bones"""
    bones = []
    objects = getSelectedObjects()
    if not len(objects):
        ShowDialog("NO OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action")
        return None
    if len(objects) > 1 and not allowMulti:
        ShowDialog("TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action")
        return None
    for obj in objects:
        if obj.type != "ARMATURE":
            continue
        for posebone in obj.pose.bones:
            if posebone.select:
                if not posebone.bone.hide and (
                    (
                        len(posebone.bone.collections)
                        and posebone.bone.collections[0].is_visible_effectively
                    )
                    or not len(posebone.bone.collections)
                ):
                    bones.append(posebone)
    return bones


def getConstraintSelectedBones(objects):
    """Return dictionnary with selected object as key and list of selected bones in the object as value"""
    boneDict = {}
    for obj in objects:
        toggleObjectSelection(objects, select=False)
        if obj.pose:
            obj.select_set(True)
            bones = getSelectedBones()
            if not bones:
                toggleObjectSelection(objects, select=True)
                return
            boneDict[obj] = bones
    return boneDict


def getConstraintsForSelection():
    """Return dict with constraints datas for selected bones"""
    objects = getSelectedObjects()
    # Get bones objects from which to get constraint datas
    boneDict = getConstraintSelectedBones(objects)
    if not boneDict:
        return
    constraintDict = {}
    # get constraint datas
    for obj in boneDict.keys():
        objName = obj.name
        objConstraints = {}
        objConstraints["bone_constraints"] = {}
        for bone in boneDict[obj]:
            for cons in bone.constraints:
                # ignore constraints with target set to self
                try:
                    target = cons.target
                    if not target or target == obj:
                        continue
                except:
                    target = None
                    continue
                print("\n\nIgnore targetless constraint : " + cons.name)
                # write dict
                if bone.name not in objConstraints["bone_constraints"].keys():
                    objConstraints["bone_constraints"][bone.name] = {}
                objConstraints["bone_constraints"][bone.name][cons.name] = {}
                for prop, value in cons.bl_rna.properties.items():
                    propValue = eval("cons." + prop)
                    if value.type == "POINTER":
                        try:
                            propValue = {"type": propValue.type, "name": propValue.name}
                        except:
                            propValue = str(propValue)
                    if propValue.__class__.__name__ == "Matrix":
                        propValue = {
                            "matrix": [[elem for elem in line] for line in propValue]
                        }
                    objConstraints["bone_constraints"][bone.name][cons.name][
                        prop
                    ] = propValue
        if len([key for key in objConstraints["bone_constraints"].keys()]):
            constraintDict[objName] = objConstraints
    # reset selection
    toggleObjectSelection(objects, select=True)
    if not len([key for key in constraintDict.keys()]):
        return
    return constraintDict


def updateSelectionSet(infoWidget, add=True):
    """Modify selection set item"""
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


def pasteConstraints(constraintDir, pairingDict, itemType="CONSTRAINT SET"):
    """Read constraint json and apply constraints on selected bones"""
    # read json
    itemdata = {}
    if itemType == "MULTI POSE":
        jsonPath = os.path.join(constraintDir, "multi_pose.json")
    elif itemType == "MULTI ANIMATION":
        jsonPath = os.path.join(constraintDir, "multi_animation.json")
    else:
        jsonPath = os.path.join(constraintDir, "constraint_set.json")
    with open(jsonPath) as file:
        itemdata = json.load(file)
    if "constraintData" in itemdata.keys():
        constraintData = itemdata["constraintData"]
    else:
        ShowDialog("Found no constraint data in " + jsonPath, title="Abort action")
        return
    # Get objects from which to get constraint datas
    objects = getSelectedObjects()
    pbList = []
    # apply constraints
    for objName in constraintData.keys():
        boneConstraints = constraintData[objName]["bone_constraints"]
        constraintToObject = None
        for selected in objects:

            if selected.name == pairingDict[objName]["object"]:
                constraintToObject = selected
                break
        if not constraintToObject:
            pbList.append("Info : Constraints for " + objName + " have been ignored.")
            continue
        for boneName in boneConstraints.keys():
            bone = constraintToObject.pose.bones.get(boneName)

            for constName, constData in boneConstraints[boneName].items():
                if not constData["name"] in pairingDict[objName]["constraints"].keys():
                    print("Ignore apply " + constData["name"])
                    continue
                if not bone:
                    pbList.append(
                        "Did not find bone "
                        + boneName
                        + " in "
                        + constraintToObject.name
                        + " to apply "
                        + constData["name"]
                        + " constraint"
                    )
                    continue
                cons = bone.constraints.new(constData["type"])
                cons.name = constData["name"] + "_GAOLIB"
                try:
                    cons.target = bpy.data.objects.get(
                        pairingDict[objName]["constraints"][constData["name"]][
                            "destinationTarget"
                        ]
                    )
                except:
                    print(constName + " : This constraint has no target ")
                    pass
                for propName, propData in constData.items():
                    if propName not in [
                        "type",
                        "rna_type",
                        "name",
                        "is_override_data",
                        "is_valid",
                        "error_location",
                        "error_rotation",
                        "target",
                    ]:
                        if propData.__class__.__name__ != "dict":
                            try:
                                if (
                                    propData.__class__.__name__ == "str"
                                    and propData != "None"
                                ):
                                    exec(
                                        "cons."
                                        + propName
                                        + ' = "'
                                        + str(propData)
                                        + '"'
                                    )
                                else:
                                    exec("cons." + propName + " = " + str(propData))
                            except AttributeError as e:
                                pbList.append("Attribute error : " + str(e))
                        else:
                            if "matrix" in propData.keys():
                                for i in range(len(propData["matrix"])):
                                    for j in range(len(propData["matrix"][i])):
                                        exec(
                                            "cons."
                                            + propName
                                            + "["
                                            + str(i)
                                            + "]["
                                            + str(j)
                                            + "] = "
                                            + str(propData["matrix"][i][j])
                                        )

                            elif "type" in propData.keys():
                                elem = eval(
                                    'bpy.data.objects.get("' + propData["name"] + '")'
                                )
                                exec("cons." + propName + "= elem")
                # if constData["type"] == "CHILD_OF":
                #     # set inverse
                #     print("Set inverse not implemented yet")
                #     # bpy.context.active_object.data.bones.active = bone.bone
                #     # print(bpy.context)
                #     # bpy.ops.constraint.childof_set_inverse( constraint=cons.name, owner="BONE" )

                #     # matrix_final = (
                #     #     cons.target.matrix_world
                #     #     * cons.target.pose.bones.get(cons.subtarget).matrix
                #     # )
                #     # cons.inverse_matrix = matrix_final.inverted()

    # if len(pbList):
    #     ShowDialog(
    #         "Some problems occured : \n" + "\n".join(pbList),
    #         title="WARNING",
    #     )
    return pbList


def getActionFcurves(action, slot=None):
    # blender 5.0 new way to retrieve fcurves
    fcurves = []
    if slot:
        channelbag = anim_utils.action_get_channelbag_for_slot(action, slot)
        if channelbag:
            return [fc for fc in channelbag.fcurves]
    else:
        for slot in action.slots:
            channelbag = anim_utils.action_get_channelbag_for_slot(action, slot)
            if not channelbag:
                print("Not channel bag !!!! ")
                continue
            for fc in channelbag.fcurves:
                fcurves.append(fc)
    return fcurves


def getAnimInfos(infoWidget, sourceFrameIn, sourceFrameOut):
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
    return (quickPaste, frameIn, frameOut)


def assignActionToObject(object, action, slot=None):
    if object.animation_data is None:
        object.animation_data_create()
    # assign action
    object.animation_data.action = action
    # assign slot
    if hasattr(action, "slots"):  # manage slots or blender 4.4
        if not slot:
            suitable_slots = object.animation_data.action_suitable_slots
            if suitable_slots:
                object.animation_data.action_slot = suitable_slots[0]
            else:
                slot = action.slots.new(id_type="OBJECT", name=object.name)
                object.animation_data.action_slot = slot
        else:
            object.animation_data.action_slot = slot


def cleanFrameRangeToPasteAnim_old(
    selectedObject, selectedBones, frameIn, frameOut, actionName
):
    """
    Prepare action to paste anim on
    Args:
        selectedObject: armatuer object to paste animatoin on
        selectedBones: List of bones
        frameIn: start frame to clean
        frameOut: end frame to clean
        actionName: if no action exists on selectedObject create one named actionName
    """
    # Delete frame range anim
    for bone in selectedBones:
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
                        bone.keyframe_delete(data_path='["' + key + '"]', frame=frame)
                    except:
                        pass
            else:
                break
    if selectedObject.animation_data is None:
        selectedObject.animation_data_create()
    # If no action on selected object, create one
    if selectedObject.animation_data.action is None:
        gaolibAction = bpy.data.actions.new(actionName)
        selectedObject.animation_data.action = gaolibAction


def cleanFrameRangeToPasteAnim(
    selectedObject, selectedBones, frameIn, frameOut, actionName, slot=None
):
    animation_data = selectedObject.animation_data
    if not animation_data:
        return
    action = animation_data.action
    if not action:
        return
    fcurves = getActionFcurves(action, slot=slot)
    bone_names = {bone.name for bone in selectedBones}
    # remove anim curves
    for fcurve in fcurves:
        data_path = fcurve.data_path
        if not data_path.startswith('pose.bones["'):
            continue
        try:
            bone_name = data_path.split('"')[1]
        except Exception:
            continue
        if bone_name not in bone_names:
            continue
        keyframe_points = fcurve.keyframe_points
        # Collect once
        to_remove = [kp for kp in keyframe_points if frameIn <= kp.co.x <= frameOut]
        # Remove backwards
        for kp in reversed(to_remove):
            keyframe_points.remove(kp)
        fcurve.update()
    bpy.context.view_layer.update()
    if selectedObject.animation_data is None:
        selectedObject.animation_data_create()
    # If no action on selected object, create one
    if selectedObject.animation_data.action is None:
        gaolibAction = bpy.data.actions.new(actionName)
        selectedObject.animation_data.action = gaolibAction


def get_or_create_fcurve(action, data_path, array_index=-1, slot=None):
    # -------------------------------------------------------------------------
    # Legacy actions
    # -------------------------------------------------------------------------
    if hasattr(action, "fcurves"):
        fcurves = action.fcurves
    # -------------------------------------------------------------------------
    # Blender 5 layered/slotted actions
    # -------------------------------------------------------------------------
    else:
        if not len(action.layers):
            action.layers.new("MainLayer")
        layer = action.layers[0]
        if not len(layer.strips):
            layer.strips.new(type="KEYFRAME")
        strip = layer.strips[0]
        channelbag = strip.channelbag(slot)
        if not channelbag:
            channelbag = strip.channelbags.new(slot)
        fcurves = channelbag.fcurves
    # -------------------------------------------------------------------------
    # Find/create curve
    # -------------------------------------------------------------------------
    fc = fcurves.find(data_path, index=array_index)
    if fc is None:
        fc = fcurves.new(data_path, index=array_index)
    return fc


def copyKeyframes(
    source_action,
    target_object,
    selected_bones,
    source_frame_in,
    source_frame_out,
    frame_in,
    slot=None,
):
    animation_data = target_object.animation_data
    if not animation_data:
        target_object.animation_data_create()
        animation_data = target_object.animation_data
    if not animation_data.action:
        animation_data.action = bpy.data.actions.new(
            name=f"{target_object.name}_Action"
        )
    if not animation_data.action_slot:
        animation_data.action_slot = animation_data.action.slots.new(
            id_type="OBJECT", name=target_object.name
        )
    target_action = animation_data.action
    target_slot = animation_data.action_slot
    bone_names = {bone.name for bone in selected_bones}
    source_fcurves = getActionFcurves(source_action, slot=slot)
    for source_fc in source_fcurves:
        data_path = source_fc.data_path
        # ---------------------------------------------------------------------
        # Filter pose bone curves
        # ---------------------------------------------------------------------
        if data_path.startswith('pose.bones["'):
            try:
                bone_name = data_path.split('"')[1]
            except Exception:
                bone_name = None
                continue
            if not bone_name or bone_name not in bone_names:
                continue
        if '.constraints["' in data_path:
            # For constraints, new created constraint is renamed with _GAOLIB suffix
            # print("original data_path : " + str(data_path))
            splitted = data_path.split('.constraints["')
            constraintName = splitted[-1].split('"]')[0]
            data_path = (
                splitted[0]
                + '.constraints["'
                + constraintName
                + "_GAOLIB"
                + splitted[-1].replace(constraintName, "")
            )
            # print("new data_path : " + str(data_path))
        array_index = source_fc.array_index
        # ---------------------------------------------------------------------
        # Get/create target fcurve ONCE
        # ---------------------------------------------------------------------
        target_fc = get_or_create_fcurve(
            target_action, data_path, array_index, target_slot
        )
        source_points = source_fc.keyframe_points
        # ---------------------------------------------------------------------
        # Collect points first
        # ---------------------------------------------------------------------
        new_keys = []
        for kp in source_points:
            source_frame = kp.co.x
            if not (source_frame_in <= source_frame <= source_frame_out):
                continue
            target_frame = frame_in + source_frame - source_frame_in
            new_keys.append(
                (
                    target_frame,
                    kp.co.y,
                    kp.interpolation,
                )
            )
        if not new_keys:
            continue
        # ---------------------------------------------------------------------
        # Bulk-add keyframes
        # ---------------------------------------------------------------------
        start_index = len(target_fc.keyframe_points)
        target_fc.keyframe_points.add(len(new_keys))
        for i, (frame, value, interpolation) in enumerate(new_keys):
            kp = target_fc.keyframe_points[start_index + i]
            kp.co = (frame, value)
            kp.interpolation = interpolation
        # ---------------------------------------------------------------------
        # One update only
        # ---------------------------------------------------------------------
        target_fc.update()
    # -------------------------------------------------------------------------
    # Single scene refresh
    # -------------------------------------------------------------------------
    bpy.context.view_layer.update()
    # Group channels by bones
    groupChannelsByBones(target_object)


def copyKeyframes_old(
    sourceAction,
    targetObject,
    selectedBones,
    sourceFrameIn,
    sourceFrameOut,
    frameIn,
    slot=None,
):
    count_op = 0
    # get list of all action fcurves
    fcurves = getActionFcurves(sourceAction, slot=slot)
    # Retrieve source action keyframe points and copy them into target action
    for fc in fcurves:
        for kp in fc.keyframe_points:
            sourceFrame = kp.co.x
            if sourceFrameIn <= sourceFrame <= sourceFrameOut:
                data_path = fc.data_path
                bone = None
                try:
                    bone = eval(("targetObject." + data_path).split("]")[0] + "]")
                except Exception as e:
                    print("WARNING : " + str(e))
                if bone in selectedBones:
                    index = fc.array_index
                    value = kp.co.y
                    try:
                        data = eval("targetObject." + data_path)
                        convertedValue = eval(
                            data.__class__.__name__ + "(" + str(value) + ")"
                        )
                        value = convertedValue
                    except:
                        pass
                    frame = frameIn + sourceFrame - sourceFrameIn

                    bpy.context.scene.frame_current = int(frame)
                    try:
                        index = fc.array_index
                        cmd = (
                            "targetObject."
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
                        valueType = eval(f"targetObject.{data_path}.__class__.__name__")
                        typedValue = eval(f"{valueType}({value})")
                        cmd = f"targetObject.{data_path} = {typedValue}"
                        if not "rotation_mode" in data_path:
                            exec(cmd)
                            count_op += 1
                        else:
                            try:
                                rot = int(value)
                            except:
                                rot = int(float(value))
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
                                "targetObject."
                                + data_path
                                + " = '"
                                + rotmodeDict[rot]
                                + "'"
                            )
                            exec(cmd)
                            count_op += 1

                    except KeyError as e:
                        print("WARNING : KeyError for command : " + cmd + "\n" + str(e))
                        continue
                    except Exception as e:
                        ShowDialog(
                            "Paste anim exception : " + str(e), title="Abort action"
                        )
                        raise
                    count_op += 1
                    targetObject.keyframe_insert(
                        data_path=data_path, index=index, frame=frame
                    )
    print(
        "Copy keyframes on "
        + targetObject.name
        + " total operations : "
        + str(count_op)
    )
    # Group channels by bones
    groupChannelsByBones(targetObject)


def pasteMultiAnim(animDir, pairingDict, sourceFrameIn, sourceFrameOut, infoWidget):
    """Paste library animation on selection allowing selection on multiple armatures"""
    # read json
    itemdata = {}
    jsonPath = os.path.join(animDir, "multi_animation.json")
    with open(jsonPath) as file:
        itemdata = json.load(file)
    if "multiAnimData" in itemdata.keys():
        multiAnimData = itemdata["multiAnimData"]
    else:
        ShowDialog("Found no constraint data in " + jsonPath, title="Abort action")
        return
    # Remember selection
    selectedObjects = getSelectedObjects()
    selectedBones = getSelectedBones(allowMulti=True)
    if not len(selectedBones):
        return
    if len(selectedObjects) < 1:
        ShowDialog("NO OBJECTS SELECTED. NEED AT LEAST ONE.", title="Abort action")
        return
    # Read item infos on GAOLIB window
    quickPaste, frameIn, frameOut = getAnimInfos(
        infoWidget, sourceFrameIn, sourceFrameOut
    )
    # Append actions
    animPath = os.path.join(animDir, "animation.blend")
    importedActions = importAllActions(animPath)
    if not len(importedActions):
        ShowDialog("NO ACTION IMPORTED FROM " + animPath, title="Abort action")
        return
    itemName = os.path.basename(animDir).split(".")[0]
    for sourceObj in pairingDict.keys():
        # get target object to apply pose to
        targetObj = None
        for obj in selectedObjects:
            if obj.name == pairingDict[sourceObj]["object"]:
                targetObj = obj
                break
        if not targetObj:
            print("Did not find target obj for " + sourceObj)
            continue
        # get bone names from source selection set
        selectionSetBones = []
        for key in itemdata["metadata"].keys():
            if key == "boneNames":
                if sourceObj in itemdata["metadata"]["boneNames"].keys():
                    selectionSetBones = itemdata["metadata"]["boneNames"][sourceObj]
        # select target
        toggleObjectSelection(selectedObjects)
        bpy.context.view_layer.objects.active = targetObj
        toggleObjectSelection([targetObj], select=True)
        # get  selected bones for targetObj
        selection = getSelectedBones()
        if not len(selection):
            print("No bones selected in target " + targetObj.name)
            continue
        # get action to paste on targetObj
        if sourceObj not in multiAnimData.keys():
            continue
        slotName = multiAnimData[sourceObj]["slot"]
        actionName = multiAnimData[sourceObj]["lib_action"]
        action = None
        for act in importedActions:
            if act.name == actionName:
                action = act
        if not action:
            ShowDialog(
                "NO ACTION IMPORTED FROM " + animPath + " IS NAMED " + actionName,
                title="Abort action",
            )
            return
        slot = action.slots.get(slotName)
        if not slot:
            ShowDialog(
                slotName + " slot not found in action " + action.name,
                title="Abort action",
            )
            return
        # PASTE action
        if quickPaste:
            assignActionToObject(targetObj, action, slot=slot)
        else:
            newActionName = itemName + "_GAOLIB_NEW_ACTION"
            # Delete frame range anim
            cleanFrameRangeToPasteAnim(
                targetObj, selection, frameIn, frameOut, newActionName
            )
            # copy keyframes from library action to current action
            copyKeyframes(
                action,
                targetObj,
                selection,
                sourceFrameIn,
                sourceFrameOut,
                frameIn,
                slot=slot,
            )

    if quickPaste:
        # rename imported actions
        for act in importedActions:
            origName = ""
            for key in multiAnimData:
                if act.name == multiAnimData[key]["lib_action"]:
                    origName = multiAnimData[key]["original_action"]
                    break
            act.name = itemName + "_" + origName
        infoWidget.parent.statusBar().showMessage("Quick Paste Action(s) done !", 1500)
    else:
        # clean actions
        for act in importedActions:
            bpy.data.actions.remove(act)
        infoWidget.parent.statusBar().showMessage("Paste animation done !", 1500)


def pasteAnim(animDir, sourceFrameIn, sourceFrameOut, infoWidget):
    """Paste animation on selected bones"""
    # Remember selection
    selection = getSelectedBones()
    if not selection:
        return
    # Read item infos on GAOLIB window
    quickPaste, frameIn, frameOut = getAnimInfos(
        infoWidget, sourceFrameIn, sourceFrameOut
    )
    # Get selected object
    selectedObjects = getSelectedObjects()
    if len(selectedObjects) != 1:
        ShowDialog(
            "NO OR TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action"
        )
        return
    selectedObject = selectedObjects[0]
    slot = selectedObject.animation_data.action_slot
    # Append action
    animPath = os.path.join(animDir, "animation.blend")
    # # ensure ther is only one action in animPath blender file
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
    actionName = os.path.basename(animDir).split(".")[0]
    if "gaolibaction" not in actionName.lower():
        actionName = actionName + "GaolibAction"
    if quickPaste:
        # Paste entire action in new action
        action.name = actionName
        assignActionToObject(selectedObject, action)
        infoWidget.parent.statusBar().showMessage("Quick Paste Action done !", 1500)
    else:
        # Paste into current action the keyframes corresponding to selected range
        action.name = "TEMP_ACTION"
        # Delete frame range anim
        cleanFrameRangeToPasteAnim(
            selectedObject, selection, frameIn, frameOut, actionName, slot
        )
        # copy keyframes
        if len(action.slots) == 1:
            sl = action.slots[0]
        else:
            sl = None
        copyKeyframes(
            action,
            selectedObject,
            selection,
            sourceFrameIn,
            sourceFrameOut,
            frameIn,
            slot=sl,
        )
        # clean action
        bpy.data.actions.remove(action)
        infoWidget.parent.statusBar().showMessage("Paste animation done !", 1500)


def groupChannelsByBones(selectedObject):
    # Group channels by bone names
    bones = {}
    # selectedObjFcurves = getActionFcurves(selectedObject.animation_data.action)
    act = selectedObject.animation_data.action
    sl = selectedObject.animation_data.action_slot
    channelbag = anim_utils.action_get_channelbag_for_slot(act, sl)
    selectedObjFcurves = [fc for fc in channelbag.fcurves]
    for fc in selectedObjFcurves:
        try:
            bone = fc.data_path.split('["')[1].split('"]')[0]
            if bone not in bones.keys():
                bones[bone] = []
            bones[bone].append(fc)
        except:
            pass
    for key in bones.keys():
        group = channelbag.groups.get(key)
        if not group:
            group = channelbag.groups.new(key)
        for fc in bones[key]:
            if fc.group == None:
                fc.group = group


def copyPose(poseDir):
    """Copy pose temporary file to library"""
    tempDir = bpy.context.preferences.filepaths.temporary_directory + "/gaolib_temp"
    for f in os.listdir(tempDir):
        if f.endswith(".blend"):
            source = os.path.join(tempDir, f)
            fileName = f.replace("copybuffer_pose_original", "pose").replace(
                "copybuffer_pose_flipped", "pose_flipped"
            )
            destination = os.path.join(poseDir, fileName)
            shutil.copyfile(source, destination)


def getCurrentPose():
    """Return dict with current pose informations"""
    selection = []
    objects = getSelectedObjects()
    # if len(objects) != 1:
    #     ShowDialog(
    #         "NO OR TOO MANY OBJECTS SELECTED. NEED EXACTLY ONE.", title="Abort action"
    #     )
    #     return None
    # if objects[0].type != "ARMATURE":
    #     ShowDialog("Please, select an ARMATURE object.", title="Abort action")
    #     return None
    for obj in objects:
        if obj.type != "ARMATURE":
            continue
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


def getRefPoseFromLib(poseDir, selection, flipped=False, sourceObjName=None):
    """Retrieve pose from given poseDir directory"""
    selectionNames = [posebone.bone.name for posebone in selection]
    # Append pose object
    prefix = ""
    if sourceObjName:
        prefix = sourceObjName + "__"
    if flipped:
        posePath = os.path.join(poseDir, prefix + "pose_flipped.blend")
    else:
        posePath = os.path.join(poseDir, prefix + "pose.blend")
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
            posebone.select = True
            refBones.append(posebone)
    return refPose


def deleteRefPose(refPose, infoWidget):
    """Clean reference pose imported while pasting/blending a pose"""
    try:
        bpy.data.objects.remove(refPose)
    except ReferenceError as e:
        print(str(e))
    # Clean armature orphans
    for arm in bpy.data.armatures:
        if not arm.users:
            bpy.data.armatures.remove(arm)
    infoWidget.refPose = None


def copyBoneProperties(
    sourceBone,
    destinationBone,
    currentPose,
    blend,
    insertKeyframes,
    additiveMode=False,
    cleanOnError=True,
):
    # Manage if different rotation modes used (WARNING : axis angle not supported !)
    rotationMode = sourceBone.rotation_mode
    # AXIS_ANGLE rotation mode not supported !
    if rotationMode == "AXIS_ANGLE" or destinationBone.rotation_mode == "AXIS_ANGLE":
        # Clean orphans
        if cleanOnError:
            removeOrphans()
        raise Exception(
            "AXIS_ANGLE Rotation mode not supported, use QUATERNION or Euler.\nCheck bone named "
            + sourceBone.name
        )
    elif (
        rotationMode == "QUATERNION"
        and currentPose[destinationBone]["rotationMode"] != "QUATERNION"
    ):
        currentPoseRotation = currentPose[destinationBone]["rotation"].to_quaternion()
    elif (
        rotationMode != "QUATERNION"
        and currentPose[destinationBone]["rotationMode"] == "QUATERNION"
    ):
        currentPoseRotation = currentPose[destinationBone]["rotation"].to_euler()
    elif rotationMode == currentPose[destinationBone]["rotationMode"]:
        currentPoseRotation = currentPose[destinationBone]["rotation"]
    else:
        # Clean orphans
        if cleanOnError:
            removeOrphans()
        raise Exception(
            "Conversion between Rotation modes other than QUATERNION and Euler are not supported !\nCheck bone named "
            + sourceBone.name
        )

    destinationBone.rotation_mode = rotationMode
    # Set pose for selected bones
    for axis in range(3):
        if not destinationBone.lock_location[axis]:
            if additiveMode:
                (
                    blend * sourceBone.location[axis]
                    + currentPose[destinationBone]["location"][axis]
                )
            else:
                destinationBone.location[axis] = (
                    blend * sourceBone.location[axis]
                    + (1 - blend) * currentPose[destinationBone]["location"][axis]
                )
        if rotationMode != "QUATERNION":
            if not destinationBone.lock_rotation[axis]:
                if additiveMode:
                    destinationBone.rotation_euler[axis] = (
                        blend * sourceBone.rotation_euler[axis]
                        + currentPoseRotation[axis]
                    )
                else:
                    destinationBone.rotation_euler[axis] = (
                        blend * sourceBone.rotation_euler[axis]
                        + (1 - blend) * currentPoseRotation[axis]
                    )
        if not destinationBone.lock_scale[axis]:
            if additiveMode:
                destinationBone.scale[axis] = (
                    blend * sourceBone.scale[axis]
                    + currentPose[destinationBone]["scale"][axis]
                    - blend
                )
            else:
                destinationBone.scale[axis] = (
                    blend * sourceBone.scale[axis]
                    + (1 - blend) * currentPose[destinationBone]["scale"][axis]
                )
    if rotationMode == "QUATERNION":
        if not destinationBone.lock_rotation_w:
            if additiveMode:
                destinationBone.rotation_quaternion[0] = (
                    blend * sourceBone.rotation_quaternion[0]
                    + currentPoseRotation[0]
                    - blend
                )
            else:
                destinationBone.rotation_quaternion[0] = (
                    blend * sourceBone.rotation_quaternion[0]
                    + (1 - blend) * currentPoseRotation[0]
                )
        for axis in range(3):
            if not destinationBone.lock_rotation[axis]:
                if additiveMode:
                    destinationBone.rotation_quaternion[axis + 1] = (
                        blend * sourceBone.rotation_quaternion[axis + 1]
                        + currentPoseRotation[axis + 1]
                    )
                else:
                    destinationBone.rotation_quaternion[axis + 1] = (
                        blend * sourceBone.rotation_quaternion[axis + 1]
                        + (1 - blend) * currentPoseRotation[axis + 1]
                    )

    # handle properties
    for key in sourceBone.keys():
        try:
            propertyType = eval("destinationBone." + key).__class__.__name__
            if propertyType == "float":
                exec(
                    "destinationBone."
                    + key
                    + " = blend * sourceBone."
                    + key
                    + " + (1-blend) * currentPose[destinationBone]."
                    + key
                )
            else:
                exec("destinationBone." + key + " = sourceBone." + key)
        except:
            try:
                propertyType = eval('destinationBone["' + key + '"]').__class__.__name__
                if propertyType == "float":
                    command = (
                        'destinationBone["'
                        + key
                        + '"] = blend * sourceBone["'
                        + key
                        + '"]'
                        + '+ (1-blend) * currentPose[destinationBone]["properties"]["'
                        + key
                        + '"]'
                    )
                    exec(command)
                else:
                    exec('destinationBone["' + key + '"] = sourceBone["' + key + '"]')
            except:
                print(
                    "IMPOSSIBLE TO HANDLE PROPERTY "
                    + key
                    + " FOR "
                    + destinationBone.name
                )
    # Key the pasted pose
    if insertKeyframes:
        destinationBone.keyframe_insert(data_path="rotation_mode")
        for axis in range(3):
            if not destinationBone.lock_location[axis]:
                destinationBone.keyframe_insert(data_path="location", index=axis)
            if rotationMode != "QUATERNION":
                if not destinationBone.lock_rotation[axis]:
                    destinationBone.keyframe_insert(
                        data_path="rotation_euler", index=axis
                    )
            if not destinationBone.lock_scale[axis]:
                destinationBone.keyframe_insert(data_path="scale", index=axis)
        if rotationMode == "QUATERNION":
            for axis in range(3):
                if not destinationBone.lock_rotation[axis]:
                    destinationBone.keyframe_insert(
                        data_path="rotation_quaternion", index=axis + 1
                    )
                    destinationBone.keyframe_insert(
                        data_path="rotation_quaternion", index=0
                    )
        for key in sourceBone.keys():
            try:
                destinationBone.keyframe_insert(data_path='["' + key + '"]')
            except Exception as e:
                print(
                    "IMPOSSIBLE TO ADD KEYFRAME FOR PROP "
                    + key
                    + " FOR "
                    + destinationBone.name
                )


def pasteMultiPose(
    poseDir,
    pairingDict,
    flipped=False,
    blend=1,
    currentPose=None,
    additiveMode=False,
):
    """Paste pose from library on selected armature object for selected bones"""
    insertKeyframes = bpy.context.scene.tool_settings.use_keyframe_insert_auto
    # get pose selection set
    itemdata = {}
    jsonPath = os.path.join(poseDir, "multi_pose.json")
    with open(jsonPath) as file:
        itemdata = json.load(file)
    # Remember selection
    selectedObjects = getSelectedObjects()
    selectedBones = getSelectedBones(allowMulti=True)
    if not len(selectedBones):
        # If no bone is selected select all
        print("No selected bones, select all by default")
        selectMultiPoseBones(jsonPath, pairingDict)(jsonPath)
        selectedBones = getSelectedBones(allowMulti=True)
    # Remember current pose
    if not currentPose:
        currentPose = getCurrentPose()
    exceptionMessage = ""
    for sourceObj in pairingDict.keys():
        # get target object to apply pose to
        targetObj = None
        for obj in selectedObjects:
            if obj.name == pairingDict[sourceObj]["object"]:
                targetObj = obj
                break
        if not targetObj:
            print("Did not find target obj for " + sourceObj)
            continue
        # get bone names from source selection set
        selectionSetBones = []
        for key in itemdata["metadata"].keys():
            if key == "boneNames":
                selectionSetBones = itemdata["metadata"]["boneNames"][sourceObj]
        # select target
        toggleObjectSelection(selectedObjects)
        bpy.context.view_layer.objects.active = targetObj
        toggleObjectSelection([targetObj], select=True)
        # get  selected bones for targetObj
        selection = getSelectedBones()
        if not len(selection):
            print("No bones selected in target " + targetObj.name)
            continue
        # Append pose object
        refPose = getRefPoseFromLib(
            poseDir, selection, flipped=flipped, sourceObjName=sourceObj
        )
        pose = refPose.pose
        # Copy properties from ref bones current object
        try:
            for posebone in pose.bones:
                for selectedbone in selection:
                    if not selectedbone.name in selectionSetBones:
                        # ignore bones outside original pose selection set
                        continue
                    if posebone.name == selectedbone.name:
                        copyBoneProperties(
                            posebone,
                            selectedbone,
                            currentPose,
                            blend,
                            insertKeyframes,
                            additiveMode=additiveMode,
                        )
                        break
            # Group channels by bones
            if insertKeyframes:
                # Get selected object
                selectedObject = getSelectedObjects()[0]
                if not selectedObject.animation_data:
                    selectedObject.animation_data_create()
                if not selectedObject.animation_data.action:
                    selectedObject.animation_data.action = bpy.data.actions.new(
                        "anim_" + selectedObject.name + "Action"
                    )

        except Exception as e:
            print(
                targetObj.name
                + " Blend Pose Exception : "
                + str(e)
                + "\n"
                + str(traceback.format_exc())
            )
            exceptionMessage += (
                targetObj.name + " Blend Pose Exception : " + str(e) + "\n"
            )
        # Clean orphans
        removeOrphans()
        # Show message if exception
        if len(exceptionMessage):
            raise Exception(exceptionMessage)


def pastePose(
    poseDir,
    flipped=False,
    blend=1,
    currentPose=None,
    additiveMode=False,
):
    """Paste pose from library on selected armature object for selected bones"""
    insertKeyframes = bpy.context.scene.tool_settings.use_keyframe_insert_auto
    # get pose selection set
    itemdata = {}
    jsonPath = os.path.join(poseDir, "pose.json")
    with open(jsonPath) as file:
        itemdata = json.load(file)
    selectionSetBones = []
    for key in itemdata["metadata"].keys():
        if key == "boneNames":
            selectionSetBones = itemdata["metadata"]["boneNames"]
    # Remember selection
    selection = getSelectedBones()
    if not len(selection):
        # If no bone is selected select all
        print("No selected bones, select all by default")
        selectBones(jsonPath)
        selection = getSelectedBones()
    # Remember current pose
    if not currentPose:
        currentPose = getCurrentPose()
    # Append pose object
    refPose = getRefPoseFromLib(poseDir, selection, flipped=flipped)
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
                    copyBoneProperties(
                        posebone,
                        selectedbone,
                        currentPose,
                        blend,
                        insertKeyframes,
                        additiveMode=additiveMode,
                    )
                    break
        # Group channels by bones
        if insertKeyframes:
            # Get selected object
            selectedObjects = getSelectedObjects()
            selectedObject = selectedObjects[0]
            if not selectedObject.animation_data:
                selectedObject.animation_data_create()
            if not selectedObject.animation_data.action:
                selectedObject.animation_data.action = bpy.data.actions.new(
                    "anim_" + selectedObject.name + "Action"
                )
            # group channels by bones
            groupChannelsByBones(selectedObject)
    except Exception as e:
        print("Blend Pose Exception : " + str(e) + "\n" + str(traceback.format_exc()))
        exceptionMessage = "Blend Pose Exception : " + str(e)
    # Clean orphans
    removeOrphans()
    # Show message if exception
    if exceptionMessage:
        raise Exception(exceptionMessage)


def clearBoneSelection():
    """Unselect all bones"""
    for obj in bpy.data.objects:
        if obj.type == "ARMATURE":
            for bone in obj.pose.bones:
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

    for arm in bpy.data.armatures:
        if not arm.users:
            bpy.data.armatures.remove(arm)


def removeOrphanCollections():
    """Remove orphan collections"""
    for c in bpy.data.collections:
        if not c.users:
            for o in c.objects:
                bpy.data.objects.remove(o)
            bpy.data.collections.remove(c)
