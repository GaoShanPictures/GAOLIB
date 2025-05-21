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

import imageio


def generateGif(sequence, fps=25):
    """Generate a gif file from the given image sequence"""
    images = []
    filenames = sorted(os.listdir(sequence))
    nbFrames = 0
    for filename in filenames:
        images.append(imageio.imread(os.path.join(sequence, filename)))
        nbFrames += 1
    gifFile = os.path.join(os.path.dirname(sequence), "thumbnail.gif")
    print("Generate GIF from path : " + str(sequence) + " fps : " + str(fps))
    # imageio.mimsave(gifFile, images, duration=1.0 / fps, loop=0)
    imageio.mimsave(gifFile, images, fps=fps, loop=0)
    return gifFile
