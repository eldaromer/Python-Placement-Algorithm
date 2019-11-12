from bblist import *
from bbviz import drawBB
from formulate import solve

import pdb, traceback

if __name__ == '__main__':

    try:

        # A simple case study for the solver: two buttons sharing a net.

        butA = But()
        butB = But()

        # A workspace is defined by a (x, y, z) tuple of available positions
        # in positional grid units. These are ranges - ie, "3" means 
        # grid spots 0, 1, and 2 are made available for placement.

        ws = (2, 2, 2)  

        # For now, we define corresponding Bitblox of interest explicitly, though this
        # could easily be done automatically later. It is simply a list of Bitblox object
        # pairs directly corresponding to the netlist format.

        bb = [
            butA,
            butB
        ]

        cbb = [
            (butA, butB)
        ]

        cn = [
            ('B1', 'B1')
        ]

        # Call the solver, which positions the Bitblox correctly.

        solve(ws, bb, cbb, cn)

        # Draw the assembly resulting from the solution.

        drawBB(butA + butB)

    except Exception, e:

        traceback.print_exc()
        pdb.post_mortem()