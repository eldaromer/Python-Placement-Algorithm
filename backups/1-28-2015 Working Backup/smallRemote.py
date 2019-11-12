from bblist import *
from bbviz import drawBB
from bitblox import assemble
from formulate import solve

if __name__ == '__main__':

    # Another case study for the solver: button-battery-light serial circuit.

    lip = Lipo(name = "LiPo")
    but1 = But(name = "Button 1")
    but2 = But(name = "Button 2")
    led1 = Led(name = "LED 1")
    led2 = Led(name = "LED 2")
    uc1 = Micro(name = "uC 1")
    uc2 = Micro(name = "uC 2")

    # A workspace is defined by a (x, y, z) tuple of available positions
    # in positional grid units.

    ws = (6, 3, 2)

    # For now, we define corresponding Bitblox of interest explicitly, though this
    # could easily be done automatically later. It is simply a list of Bitblox object
    # pairs directly corresponding to the netlist format.

    bb = [
        lip,
        but1,
        but2,
        led1,
        led2,
        uc1,
        uc2,
    ]

    cbb = [
        (lip, but1),
        (but1, uc1),
        (uc1, led1),
        (lip, but2),
        (but2, uc2),
        (uc2, led2),
    ]

    cn = [
        ('PWR', 'B1'),
        ('B2', 'PWR'),
        ('OUT2', 'LED'),
        ('PWR', 'B1'),
        ('B2', 'PWR'),
        ('OUT2', 'LED'),
    ]

    # Call the solver, which positions the Bitblox correctly.

    solve(ws, bb, cbb, cn)

    # Draw the assembly resulting from the solution.
    drawBB(assemble(bb), grid = True, gridRadius = 3)