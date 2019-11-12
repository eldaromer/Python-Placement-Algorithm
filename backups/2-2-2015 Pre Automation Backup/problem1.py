from bblist import *
from schematic import schematic
from formulate import solve, autosolve

import pdb, traceback

if __name__ == '__main__':

    try:

        # A simple case study for the solver: two buttons sharing a net.
        ws = (2, 2, 2)  
        problem = schematic(ws, name = "Two Buttons")

        butA = But('Button 1')
        butB = But('Button 2')

        problem.addConnection(butA, 'B1', butB, 'B1')

        # Fixed Button 1 at the origin with default orientation, as example.
        problem.fix((butA, 0, 0, 0, 0))

        # Call the solver, which positions the Bitblox correctly.

        solve(problem)

        # Draw the assembly resulting from the solution.

        problem.showSolution()

    except Exception, e:

        traceback.print_exc()
        pdb.post_mortem()