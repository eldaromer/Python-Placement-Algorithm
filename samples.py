from bblist import *
from schematic import schematic
from formulate import solve, autosolve
from bbviz import *

import pdb, traceback

if __name__ == '__main__':

    try:

        # A simple case study for the solver: two buttons sharing a net.
        ws = (2, 2, 2)  
        problem = schematic(ws, name = "Two Buttons")

        butA = But('Button 1', color = (1, 0, 0))
        butB = But('Button 2', color = (0, 0, 1))
        butA.translate((1,1,1))
        butA.rotate(2)
        butB.rotate(3)

        drawBB([butB])

        # The bridged circuit fixed blox

        butA = But('Button 1')
        butB = But('Button 2')
        butA.translate((0,0,0))
        butB.translate((0,4,2))
        butB.rotate(2)

        drawBB([butA, butB])

    except Exception, e:

        traceback.print_exc()
        pdb.post_mortem()