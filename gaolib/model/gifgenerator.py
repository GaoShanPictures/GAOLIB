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

# import imageio
import subprocess


def generateGif(sequence, fps=25):
    """Generate a gif file from the given image sequence"""
    gifFile = os.path.join(os.path.dirname(sequence), "thumbnail.gif")
    paletteFile = os.path.join(os.path.dirname(sequence), "palette.png")
    inputF = os.path.join(sequence, "thumbnail.mp4")

    # Q:/tools/ffmpeg/bin/ffmpeg.exe -i "C:\Users\arnaudc\blenderTemp\gaolib_temp\sequence\thumbnail.mp4" -vf "fps=25,scale=200:-1:flags=lanczos,palettegen=stats_mode=single" -frames:v 1 "C:\Users\arnaudc\blenderTemp\gaolib_temp\sequence\palette.png"
    ffmpegCmd = f'{os.environ["FFMPEG_PATH"]} -i {inputF} -vf "fps=25,scale=200:-1:flags=lanczos,palettegen=stats_mode=single" -frames:v 1 -y {paletteFile}'
    p = subprocess.Popen(ffmpegCmd)
    p.communicate()
    ffmpegCmd2 = f'{os.environ["FFMPEG_PATH"]} -i {inputF} -i {paletteFile} -filter_complex "fps=25,scale=200:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3" {gifFile} -y'
    p2 = subprocess.Popen(ffmpegCmd2)
    p2.communicate()
    # images = []
    # filenames = sorted(os.listdir(sequence))
    # nbFrames = 0
    # for filename in filenames:
    #     images.append(imageio.imread(os.path.join(sequence, filename)))
    #     nbFrames += 1
    # print("Generate GIF from path : " + str(sequence) + " fps : " + str(fps))
    # # imageio.mimsave(gifFile, images, duration=1.0 / fps, loop=0)
    # imageio.mimsave(gifFile, images, fps=fps, loop=0)
    return gifFile
