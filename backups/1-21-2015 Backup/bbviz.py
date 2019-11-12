# Bitblox visualization module. Uses VPython.
# Can visualize either a single Bitblox or a collection of them.

from visual import *
from bitblox import *
import hashlib

# Real dimensions are 3.4125 XY by 3.53 Z, so this is 2x high
# Boards are 1.6 high, so .25 high here

def drawBB(bb):
    for fgu in bb.FGU_list:
        # Draw a green board, except for pins.
        if fgu.gender is not MALE:
            s = box(pos = fgu.position, length = 1, height = 1, width = .25)
            s.color = (0, .8, 0)

        # If there is no pin or socket, go to next FGU.
        if fgu.gender is None:
            continue

        # Generate coloring based on net string, or grey if no net.
        if fgu.net is None:
            col = [.5, .5, .5]
        else:
            colhash = hashlib.sha224(fgu.net)
            coluw = [ord(colhash.digest()[i]) for i in range(3)]
            col = [1.0 * c / sum(coluw) for c in coluw]

        # Adjust position to draw cone/cylinder with VPython
        position = list(fgu.position)
        position[2] = position[2] + .5

        # Draw the 3 distinct pins/sockets in the proper orientation
        for offset in (-.25, 0, .25):
            offpos = list(position)
            offpos[0] = offpos[0] + offset
            if fgu.align is NW:
                offpos[1] = offpos[1] - offset
            else:
                offpos[1] = offpos[1] + offset
            if fgu.gender is MALE:
                s = cone(pos = offpos, axis = (0, 0, -1), radius = .15)
            elif fgu.gender is FEMALE:
                s = cylinder(pos = offpos, axis = (0, 0, -1), radius = .15)
            s.color = col
            s = None

    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            for z in (-1, 0, 1):
                #sphere(pos = (x, y, z), radius = .1)
                pass

def newWindow():
    scene = display()
    return scene