from bitblox import *

# To programmatically define a Bitblox of particular type,
# extend the Bitblox class and overload the initialization method
# to directly write the FGU list.

class Bat(BitBlox):

    def __init__(self):
        self.FGU_list = [
            FGU([.5, .5, .5], net = 'PWR', gender = False, align = True),
            FGU([-.5, .5, .5], net = 'PWR', gender = False, align = False),
            FGU([-.5, -.5, .5]),
            FGU([.5, -.5, .5]),
            FGU([.5, .5, -.5], net = 'PWR', gender = True, align = True),
            FGU([-.5, .5, -.5], net = 'PWR', gender = True, align = False),
            FGU([-.5, -.5, -.5]),
            FGU([.5, -.5, -.5])
        ]
        self.anchorFGUs = [0, 1, 2, 3]
        self.orientation = 0
        self.name = 'Battery'

class But(BitBlox):
    # B1 = brown
    # B2 = blue

    def __init__(self):
        self.FGU_list = [
            FGU([.5, .5, .5], net = 'B1', gender = False, align = True),
            FGU([-.5, .5, .5], net = 'B1', gender = False, align = False),
            FGU([-.5, -.5, .5], net = 'B2', gender = False, align = True),
            FGU([.5, -.5, .5], net = 'B2', gender = False, align = False),
            FGU([.5, .5, -.5], net = 'B1', gender = True, align = True),
            FGU([-.5, .5, -.5], net = 'B1', gender = True, align = False),
            FGU([-.5, -.5, -.5], net = 'B2', gender = True, align = True),
            FGU([.5, -.5, -.5], net = 'B2', gender = True, align = False)
        ]
        self.anchorFGUs = [0, 1, 2, 3]
        self.orientation = 0
        self.name = 'Button'

class Led(BitBlox):

    def __init__(self):
        self.FGU_list = [
            FGU([.5, .5, .5], net = 'LED', gender = False, align = True),
            FGU([-.5, .5, .5], net = 'LED', gender = False, align = False),
            FGU([-.5, -.5, .5], net = 'LED', gender = False, align = True),
            FGU([.5, -.5, .5], net = 'LED', gender = False, align = False),
            FGU([.5, .5, -.5], net = 'LED', gender = True, align = True),
            FGU([-.5, .5, -.5], net = 'LED', gender = True, align = False),
            FGU([-.5, -.5, -.5], net = 'LED', gender = True, align = True),
            FGU([.5, -.5, -.5], net = 'LED', gender = True, align = False)
        ]
        self.anchorFGUs = [0, 1, 2, 3]
        self.orientation = 0
        self.name = 'LED'