from bblist import *
from bbviz import drawBB
from formulate import findMatches, findCollisions

# A simple case study for the solver: two buttons sharing a net.


# matches = findMatches(but, 'B1', but2, 'B1')
# matches = findCollisions(but, but2)
# print matches
# print len(matches)
# but.reHome()
# for result in matches:
#      w = newWindow()
# #     but2.translateTo(result[0])
# #     but2.rotateTo(result[1])
#      drawBB(led)
#      drawBB(but)
#      drawBB(bat)
#     print anchor2grid(result[0])
#     print but2
#     w.waitfor('keyup')
#     w.delete()

#61, 137, 140, 192

if __name__ == '__main__':
    bat = Bat()
    but = But()
    led = Led()
    but.translateTo((1,1,1))
    led.translateTo((2,2,0))
    print origin2grid(bat.origin)
    print origin2grid(but.origin)
    print origin2grid(led.origin)
    print bat
    drawBB(bat+but+led, grid = True, gridRadius = 2)
    import pdb; pdb.set_trace()