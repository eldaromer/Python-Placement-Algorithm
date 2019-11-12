from bblist import *
from bbviz import drawBB
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

    ws = (3, 3, 2)

    # For now, we define corresponding Bitblox of interest explicitly, though this
    # could easily be done automatically later. It is simply a list of Bitblox object
    # pairs directly corresponding to the netlist format.

    bb = [
        bat,
        but1,
        but2,
        led1,
        led2,
    ]

    cbb = [
        (bat, but1),
        (but1, led1),
        (bat, but2),
        (but2, led2)
    ]

    cn = [
        ('PWR', 'B2'),
        ('B1', 'LED'),
        ('PWR', 'B1'),
        ('B2', 'LED')
    ]

    # Call the solver, which positions the Bitblox correctly.

    solve(ws, bb, cbb, cn)

    # Draw the assembly resulting from the solution.

    drawBB(assemble(bb), grid = False, gridRadius = 3)