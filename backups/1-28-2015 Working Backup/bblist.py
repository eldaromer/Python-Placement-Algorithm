from bitblox import *

# To programmatically define a Bitblox of particular type,
# extend the Bitblox class and overload the initialization method
# to directly write the FGU list.

# A small battery, with occupied space on half of the bottom.

class Bat(Bitblox):

    def __init__(self, name = 'Battery'):
        FGU_list = [
            FGU([.5, .5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5]),
            FGU([.5, -.5, .5]),
            FGU([.5, .5, -.5], net = 'PWR', gender = MALE, align = NW),
            FGU([-.5, .5, -.5], net = 'PWR', gender = MALE, align = NE),
            FGU([-.5, -.5, -.5]),
            FGU([.5, -.5, -.5])
        ]
        Bitblox.__init__(self, name, FGU_list)

# A button. Current visualization gives B1 = brown, B2 = greenish blue.

class But(Bitblox):

    def __init__(self, name = 'Button'):
        FGU_list = [
            FGU([.5, .5, .5], net = 'B1', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'B1', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5], net = 'B2', gender = FEMALE, align = NW),
            FGU([.5, -.5, .5], net = 'B2', gender = FEMALE, align = NE),
            FGU([.5, .5, -.5], net = 'B1', gender = MALE, align = NW),
            FGU([-.5, .5, -.5], net = 'B1', gender = MALE, align = NE),
            FGU([-.5, -.5, -.5], net = 'B2', gender = MALE, align = NW),
            FGU([.5, -.5, -.5], net = 'B2', gender = MALE, align = NE)
        ]
        Bitblox.__init__(self, name, FGU_list)

# A microcontroller, which is powered from one corner, and can output
# to three others.

class Micro(Bitblox):

    def __init__(self, name = 'uC'):
        FGU_list = [
            FGU([.5, .5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'OUT1', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5], net = 'OUT2', gender = FEMALE, align = NW),
            FGU([.5, -.5, .5], net = 'OUT3', gender = FEMALE, align = NE),
            FGU([.5, .5, -.5], net = 'PWR', gender = MALE, align = NW),
            FGU([-.5, .5, -.5], net = 'OUT1', gender = MALE, align = NE),
            FGU([-.5, -.5, -.5], net = 'OUT2', gender = MALE, align = NW),
            FGU([.5, -.5, -.5], net = 'OUT3', gender = MALE, align = NE)
        ]
        Bitblox.__init__(self, name, FGU_list)

# A pass block, which connects all nets.

class Pass(Bitblox):

    def __init__(self, name = 'Pass'):
        FGU_list = [
            FGU([.5, .5, .5], net = 'P', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'P', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5], net = 'P', gender = FEMALE, align = NW),
            FGU([.5, -.5, .5], net = 'P', gender = FEMALE, align = NE),
            FGU([.5, .5, -.5], net = 'P', gender = MALE, align = NW),
            FGU([-.5, .5, -.5], net = 'P', gender = MALE, align = NE),
            FGU([-.5, -.5, -.5], net = 'P', gender = MALE, align = NW),
            FGU([.5, -.5, -.5], net = 'P', gender = MALE, align = NE)
        ]
        Bitblox.__init__(self, name, FGU_list)

# An LED, lit by powering any FGU.

class Led(Bitblox):

    def __init__(self, name = 'LED'):
        FGU_list = [
            FGU([.5, .5, .5], net = 'LED', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'LED', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5], net = 'LED', gender = FEMALE, align = NW),
            FGU([.5, -.5, .5], net = 'LED', gender = FEMALE, align = NE),
            FGU([.5, .5, -.5], net = 'LED', gender = MALE, align = NW),
            FGU([-.5, .5, -.5], net = 'LED', gender = MALE, align = NE),
            FGU([-.5, -.5, -.5], net = 'LED', gender = MALE, align = NW),
            FGU([.5, -.5, -.5], net = 'LED', gender = MALE, align = NE)
        ]
        Bitblox.__init__(self, name, FGU_list)

# A huge battery.

class Lipo(Bitblox):

    def __init__(self, name = 'Lipo'):

        # Organized by row, top to bottom

        FGU_list = [

            # Top layer

            FGU([-1.5, 1.5, .5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([-.5, 1.5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([.5, 1.5, .5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([1.5, 1.5, .5], net = 'PWR', gender = FEMALE, align = NW),

            FGU([-1.5, .5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([.5, .5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([1.5, .5, .5], net = 'PWR', gender = FEMALE, align = NE),

            FGU([-1.5, -.5, .5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([.5, -.5, .5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([1.5, -.5, .5], net = 'PWR', gender = FEMALE, align = NW),

            FGU([-1.5, -1.5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([-.5, -1.5, .5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([.5, -1.5, .5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([1.5, -1.5, .5], net = 'PWR', gender = FEMALE, align = NE),

            # Middle layer

            FGU([-.5, 2.5, -.5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([.5, 2.5, -.5], net = 'PWR', gender = FEMALE, align = NW),

            FGU([-1.5, 1.5, -.5], net = 'PWR', gender = MALE, align = NE),
            FGU([-.5, 1.5, -.5]),
            FGU([.5, 1.5, -.5]),
            FGU([1.5, 1.5, -.5], net = 'PWR', gender = MALE, align = NW),

            FGU([-2.5, .5, -.5], net = 'PWR', gender = FEMALE, align = NE),
            FGU([-1.5, .5, -.5]),
            FGU([-.5, .5, -.5]),
            FGU([.5, .5, -.5]),
            FGU([1.5, .5, -.5]),
            FGU([2.5, .5, -.5], net = 'PWR', gender = FEMALE, align = NW),

            FGU([-2.5, -.5, -.5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([-1.5, -.5, -.5]),
            FGU([-.5, -.5, -.5]),
            FGU([.5, -.5, -.5]),
            FGU([1.5, -.5, -.5]),
            FGU([2.5, -.5, -.5], net = 'PWR', gender = FEMALE, align = NE),

            FGU([-1.5, -1.5, -.5], net = 'PWR', gender = MALE, align = NW),
            FGU([-.5, -1.5, -.5]),
            FGU([.5, -1.5, -.5]),
            FGU([1.5, -1.5, -.5], net = 'PWR', gender = MALE, align = NE),

            FGU([-.5, -2.5, -.5], net = 'PWR', gender = FEMALE, align = NW),
            FGU([.5, -2.5, -.5], net = 'PWR', gender = FEMALE, align = NE),

            # Bottom layer

            FGU([-.5, 2.5, -1.5], net = 'PWR', gender = MALE, align = NE),
            FGU([.5, 2.5, -1.5], net = 'PWR', gender = MALE, align = NW),

            FGU([-2.5, .5, -1.5], net = 'PWR', gender = MALE, align = NE),
            FGU([2.5, .5, -1.5], net = 'PWR', gender = MALE, align = NW),

            FGU([-2.5, -.5, -1.5], net = 'PWR', gender = MALE, align = NW),
            FGU([2.5, -.5, -1.5], net = 'PWR', gender = MALE, align = NE),

            FGU([-.5, -2.5, -1.5], net = 'PWR', gender = MALE, align = NW),
            FGU([.5, -2.5, -1.5], net = 'PWR', gender = MALE, align = NE),

        ]
        Bitblox.__init__(self, name, FGU_list)