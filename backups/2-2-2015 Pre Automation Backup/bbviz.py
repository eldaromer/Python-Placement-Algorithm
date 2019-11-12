# Bitblox visualization module. Uses VPython.
# Can visualize either a single Bitblox or a collection of them.

from visual import *
from bitblox import *
from itertools import product
from multiprocessing import Process
import hashlib

# This function draws a Bitblox. It can be used to visualize assemblies by using
# the '+' operator to combine Bitblox objects, since it takes only one.
# If grid is True, small dots will be placed at FGU grid vertices.

# Runs in a different process because of how annoying VPython is. You'll be able to 
# close the window whenever you need to, and the behavior is non-blocking.

def drawBB(bb, grid = False, gridRadius = 1, center = (0,0,0)):
    p = Process(target = drawThread, args = (bb, grid, gridRadius, center))
    p.start()
    

def drawThread(bb, grid, gridRadius, center):
    scene = display(center=center)

    for fgu in bb.FGU_list:
        
        # Draw a green board, except for male pins.
        if fgu.gender is not MALE:
            s = box(pos = fgu.position, length = 1, height = 1, width = .25)
            s.color = (0, .8, 0)

        # If there is no pin or socket, go to next FGU.
        if fgu.gender is None:
            continue

        # Generate pin coloring based on net string, or grey if no net.
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

    if grid:
        bound = range(-gridRadius, gridRadius + 1)
        for p in product(bound, repeat = 3):
            sphere(pos = p, radius = .1)

    while True:
        rate(30)