from bblist import *
from bbviz import drawBB
from formulate import solve

if __name__ == '__main__':

    # Another case study for the solver: button-battery-light serial circuit.

    bat = Bat(name = 'Bat')
    but1 = But(name = 'But1')
    but2 = But(name = 'But2')

    # A workspace is defined by a (x, y, z) tuple of available positions
    # in positional grid units.

    ws = (3, 3, 2)

    # For now, we define corresponding Bitblox of interest explicitly, though this
    # could easily be done automatically later. It is simply a list of Bitblox object
    # pairs directly corresponding to the netlist format.

    bb = [
        bat,
        but1,
        but2,
    ]

    cbb = [
        (bat, but1),
        (bat, but2),
    ]

    cn = [
        ('PWR', 'B2'),
        ('PWR', 'B1'),
    ]

    # Call the solver, which positions the Bitblox correctly.

    solve(ws, bb, cbb, cn)

    # Draw the assembly resulting from the solution.

    drawBB(assemble(bb), grid = False, gridRadius = 3)