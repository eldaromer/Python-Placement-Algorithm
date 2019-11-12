from bblist import *
from schematic import schematic
from formulate import solve, autosolve

import pdb, traceback

if __name__ == '__main__':

    try:

        # A simple case study for the solver: two buttons sharing a net.
        ws = (2, 2, 2)  
        problem = schematic(ws, name = "Bridged Buttons")

        butA = But('Button 1')
        butB = But('Button 2')
        p = Pass('Pass')

        problem.addConnection(butA, 'B1', butB, 'B1', 1)
        # problem.addConnection(butA, 'B1', p, 'P')
        # problem.addConnection(p, 'P', butB, 'B1')

        # Fixed Button 1 at the origin with default orientation, as example.
        problem.fix((butA, 0, 0, 0, 0))

        # To test bridging, also fix Button 2 in a position which requires it.
        problem.fix((butB, 1, 1, 0, 2))

        # Call the solver, which positions the Bitblox correctly.
        expanded = autosolve(problem)

        # Draw the assembly resulting from the solution.
        expanded.showSolution()

    except Exception, e:

        traceback.print_exc()
        pdb.post_mortem()