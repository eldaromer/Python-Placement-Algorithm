# Tested working with testman, 2/2

from bblist import *
from schematic import schematic
from formulate import solve, autosolve

import random

if __name__ == '__main__':

    # Another case study for the solver: a random circuit!
    # It works by building a bank, then pick a random pair of
    # Bitblox and their nets to add to the schematic. A random
    # connection is added in this manner N times.

    # The bank is of some20 fixed Bitblox in order to keep frequencies
    # somewhat realistic.

    n = random.randint(3,12)
    ws = (n, n, 3)
    relax = 1

    bank = []
    bank.append(Lipo("LiPo 1"))
    bank.append(Lipo("LiPo 2"))
    bank.append(But("Button 1"))
    bank.append(But("Button 2"))
    bank.append(But("Button 3"))
    bank.append(But("Button 4"))
    bank.append(But("Button 5"))
    bank.append(But("Button 6"))
    bank.append(Micro("uC 1"))
    bank.append(Micro("uC 2"))
    bank.append(Micro("uC 3"))
    bank.append(Micro("uC 4"))
    bank.append(Led("LED 1"))
    bank.append(Led("LED 2"))
    bank.append(Led("LED 3"))
    bank.append(Led("LED 4"))
    bank.append(Led("LED 5")) 
    bank.append(Led("LED 6")) 
    bank.append(Bat("Small Bat 1"))
    bank.append(Bat("Small Bat 2"))

    problem = schematic(ws, name = ("Random-" + str(n)))

    for i in range(n):
        firstPick = random.randint(0, len(bank) - 1)
        secondPick = firstPick
        while secondPick == firstPick:
            secondPick = random.randint(0, len(bank) - 1)
        bb1 = bank[firstPick]
        bb2 = bank[secondPick]
        nets1 = bb1.listNets()
        nets2 = bb2.listNets()
        bb1Net = nets1[random.randint(0, len(nets1) - 1)]
        bb2Net = nets2[random.randint(0, len(nets2) - 1)]
        problem.addConnection(bb1, bb1Net, bb2, bb2Net, relax)
        print ("Added " + bb1.name + ', ' + bb1Net + ' to ' +
                bb2.name + ', ' + bb2Net)

    # Call the solver, which positions the Bitblox correctly.

    fixed = autosolve(problem)

    # Draw the assembly resulting from the solution.
    #fixed.showSolution() 