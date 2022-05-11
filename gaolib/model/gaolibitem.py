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

import os
import json


class GaoLibItem(object):
    """Description of one item of the list view"""
    def __init__(self, name="", thumbpath=None, path=None):
        self.name = name
        self.thumbpath = thumbpath
        stamped = thumbpath.replace('thumbnail.png', 'thumbnail_stamped.png')
        if self.thumbpath is None or not os.path.isfile(self.thumbpath):
            self.thumbpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../icons/nopreview2.png')
        self.stamped = self.thumbpath
        if os.path.isfile(stamped):
            self.stamped = stamped
        self.path = path
        self.bonesSelection = False

        self.getItemInfos()

    def getItemInfos(self):
        """Read json infos from json"""
        if self.name.endswith('.pose'):
            jsonPath = os.path.join(self.path,  'pose.json')
            self.itemType = 'POSE'
        elif self.name.endswith('.anim'):
            jsonPath = os.path.join(self.path,  'animation.json')
            self.itemType = 'ANIMATION'
        elif self.name.endswith('.selection'):
            jsonPath = os.path.join(self.path,  'selection_set.json')
            self.itemType = 'SELECTION SET'
        else:
            jsonPath = None
            self.itemType = 'FOLDER'

        self.owner = ''
        self.date = ''
        self.content = ''
        self.frameRange = ''

        if jsonPath:
            if os.path.exists(jsonPath):
                with open(jsonPath) as file:
                    itemdata = json.load(file)

                self.owner = 'Unknown'
                self.date = 'Unknown'
                self.content = 'Unknown'
                self.frameRange = 'Unknown'

                if 'metadata' in itemdata.keys():
                    if 'user' in itemdata['metadata'].keys():
                        self.owner = itemdata['metadata']['user']
                    if 'date' in itemdata['metadata'].keys():
                        self.date =  itemdata['metadata']['date']
                    if 'content' in itemdata['metadata'].keys():
                        self.content = itemdata['metadata']['content']
                    if 'frameRange' in itemdata['metadata'].keys():
                        self.frameRange = itemdata['metadata']['frameRange']
                    if 'boneNames' in itemdata['metadata'].keys():
                        self.bonesSelection = True