from bblist import *
from schematic import schematic
from formulate import solve, autosolve

if __name__ == '__main__':

    # Another case study for the solver: button-battery-light serial circuit.

    ws = (3, 3, 2)
    problem = schematic(ws, name = "Double LED")

    bat = Bat('Battery')
    but1 = But('Button 1')
    but2 = But('Button 2')
    led1 = Led('LED 1')
    led2 = Led('LED 2')

    problem.addConnection(bat, 'PWR', but1, 'B2')
    problem.addConnection(but1, 'B1', led1, 'LED')
    problem.addConnection(bat, 'PWR', but2, 'B2')
    problem.addConnection(but2, 'B1', led2, 'LED')

    # Call the simple solver, which positions the Bitblox correctly.

    solve(problem)

    # Draw the assembly resulting from the solution.

    problem.showSolution()