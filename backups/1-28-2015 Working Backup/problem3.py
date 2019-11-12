from bblist import *
from bbviz import drawBB
from bitblox import assemble
from formulate import solve

if __name__ == '__main__':

    # Another case study for the solver: button-battery-light serial circuit.

    bat = Bat()
    but1 = But()
    but2 = But()
    led1 = Led()
    led2 = Led()

    # A workspace is defined by a (x, y, z) tuple of available positions
    # in positional grid units.

    ws = (1, 5, 2)

    # For now, we define corresponding Bitblox of interest explicitly, though this
    # could easily be done automatically later. It is simply a list of Bitblox object
    # pairs directly corresponding to the netlist format.

    bb = [
        bat,
        but1,
        led1,
    ]

    cbb = [
        (but1, led1),
        (bat, but1),
    ]

    cn = [
        ('B1', 'LED'),
        ('PWR', 'B2'),
    ]

    # Call the solver, which positions the Bitblox correctly.

    solve(ws, bb, cbb, cn)

    # Draw the assembly resulting from the solution.
    drawBB(assemble(bb), grid = True, gridRadius = 3)