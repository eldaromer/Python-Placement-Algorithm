from bitblox import *

# To programmatically define a Bitblox of particular type,
# extend the Bitblox class and overload the initialization method
# to directly write the FGU list.

# A small battery, with occupied space on half of the bottom.

class Bat(Bitblox):

    def __init__(self, name = 'Battery', color = None):
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

        cmap = { 'PWR': [1, 0, 0],}

        Bitblox.__init__(self, name, FGU_list, color = color, cmap = cmap)

# A button. Current visualization gives B1 = brown, B2 = greenish blue.
# Two terminal device, opposing corners.

class But(Bitblox):

    def __init__(self, name = 'Button', color = None):
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

        cmap = { 'B1': [60.0/255, 225.0/255, 225.0/255],
                 'B2': [255.0/255, 30.0/255, 220.0/255],}

        Bitblox.__init__(self, name, FGU_list, color = color, cmap = cmap)

# A capacitor.
# Two terminal device, opposing corners.

class Cap(Bitblox):

    def __init__(self, name = 'Capacitor', color = None):
        FGU_list = [
            FGU([.5, .5, .5], net = 'C1', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'C1', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5], net = 'C2', gender = FEMALE, align = NW),
            FGU([.5, -.5, .5], net = 'C2', gender = FEMALE, align = NE),
            FGU([.5, .5, -.5], net = 'C1', gender = MALE, align = NW),
            FGU([-.5, .5, -.5], net = 'C1', gender = MALE, align = NE),
            FGU([-.5, -.5, -.5], net = 'C2', gender = MALE, align = NW),
            FGU([.5, -.5, -.5], net = 'C2', gender = MALE, align = NE)
        ]

        Bitblox.__init__(self, name, FGU_list, color = color)

# An inductor.
# Two terminal device, opposing corners.

class Inductor(Bitblox):

    def __init__(self, name = 'Inductor', color = None):
        FGU_list = [
            FGU([.5, .5, .5], net = 'I1', gender = FEMALE, align = NW),
            FGU([-.5, .5, .5], net = 'I1', gender = FEMALE, align = NE),
            FGU([-.5, -.5, .5], net = 'I2', gender = FEMALE, align = NW),
            FGU([.5, -.5, .5], net = 'I2', gender = FEMALE, align = NE),
            FGU([.5, .5, -.5], net = 'I1', gender = MALE, align = NW),
            FGU([-.5, .5, -.5], net = 'I1', gender = MALE, align = NE),
            FGU([-.5, -.5, -.5], net = 'I2', gender = MALE, align = NW),
            FGU([.5, -.5, -.5], net = 'I2', gender = MALE, align = NE)
        ]
        Bitblox.__init__(self, name, FGU_list, color = color)

# A microcontroller, which is powered from one corner, and can output
# to three others. 4 terminals, 4 corners.

class Micro(Bitblox):

    def __init__(self, name = 'uC', color = None):
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
        Bitblox.__init__(self, name, FGU_list, color = color)

# A pass block, which connects all nets.

class Pass(Bitblox):

    def __init__(self, name = 'Pass', color = None):
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
        Bitblox.__init__(self, name, FGU_list, color = color)

# An LED, lit by powering any corner.

class Led(Bitblox):

    def __init__(self, name = 'LED', color = None):
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

        cmap = { 'LED': [245.0/255, 255.0/255, 65.0/255],}

        Bitblox.__init__(self, name, FGU_list, color = color, cmap = cmap)

# A huge battery. 3 x 3 x 2 grid envelope. All pins powered.

class Lipo(Bitblox):

    def __init__(self, name = 'Lipo', color = None):

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

        cmap = { 'PWR': [1, 0, 0],}

        Bitblox.__init__(self, name, FGU_list, color = color, cmap = cmap)