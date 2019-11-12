from bblist import *
from bbviz import drawBB, newWindow
from formulate import findMatches, findCollisions, anchor2grid

# led = Led()
# drawBB(led)
# mybut = But()
# mybut.translate([1,1,1])
# interest = mybut.FGU_list[3]
# mybut.rotateAbout(interest, 1)
# print mybut.orientation
# drawBB(mybut)

led = Led()
but = But()
bat = Bat()
led.translateTo((-1,3,1.5)) # 1, 2, 1, 3
led.rotateTo(3)
but.translateTo((0,4,.5)) # 2, 2, 0, 0; 2, 2, 0, 3
but.rotateTo(3)
bat.translateTo((1,3,1.5)) # 2, 1, 1, 0
w = newWindow()
drawBB(led)
drawBB(but)
drawBB(bat)


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