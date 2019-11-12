# Constants used for denoting pin gender and orientation.
# "Gender" is used in the industrial sense, and is binary in this case.

MALE = True
FEMALE = False
NW = True
NE = False

# To convert an FGU coordinate to a grid coordinate:
#   -  Rotate 45 (we'll pick clockwise, but it doesn't matter)
#   -  Divide positions by sqrt(2)
#   -  Round to int for index purposes
# This will convert:    (0, 0, 0) to (0, 0, 0)
#                       (1, 1, 0) to (1, 0, 0)
#                       (1, 3, 1) to (2, 1, 1)  and so forth.

def origin2grid(origin):    # Hand test OK
    grid = list(origin)
    grid[0] = int(round((origin[0] + origin[1])/2))
    grid[1] = int(round((-origin[0] + origin[1])/2))
    grid[2] = int(round(origin[2]))
    return grid

# Inverse operation for the above.

def grid2origin(grid):      # Hand test OK
    origin = list(grid)
    origin[0] = grid[0] - grid[1]
    origin[1] = grid[0] + grid[1]
    origin[2] = grid[2]
    return origin

# Summation of Bitblox lists.

def assemble(bblist):
    out = bblist[0]
    for i in range(1, len(bblist)):
        out = out + bblist[i]
    return out

def inPlaneRot(xyz, ccw_turns):
    ccw_turns = ccw_turns % 4
    if ccw_turns is 1:
        return [-xyz[1], xyz[0], xyz[2]]
    elif ccw_turns is 2:
        return [-xyz[0], -xyz[1], xyz[2]]
    elif ccw_turns is 3:
        return [xyz[1], -xyz[0], xyz[2]]
    else:
        return xyz


# An FGU class defining a "fundamental grid unit," which is a "corner" of a Bitblox
# containing 3 pins (either the female or male halves of the pins). Every single
# Bitblox can be defined as a collection of just fundamental grid units, offset to
# various positions from the origin.

# The origin of a Bitblox is defined as the centroid of the 8 FGU's representing the
# unit Bitblox used for picking, which is equivalent to the center bottom of the 4 
# female socket FGUs used for picking. One FGU unit is one FGU wide/long/tall. An
# FGU's coordinates are considered to be the position of its centroid - therefore,
# FGU's typically have coordinates of .5, 1.5, 2.5, etc. 

class FGU():

    # Note that gender doubles as occupancy information
    # gender "none" denotes a non - collidable FGU with no net
    # Position is an [X, Y, Z] list
    # Net is a string containing net name
    # Gender is either True (pin) or False (socket)
    # Align is either True (NW, \) or False (NE, /)

    def __init__(self, position, net = None, gender = None, align = None):
        self.position = position
        self.net = net
        self.gender = gender
        self.align = align

    def __repr__(self):
        if self.net is not None:
            return 'FGU @ ' + str(self.position) + ' of net ' + self.net
        else:
            return 'FGU @ ' + str(self.position) + ', no net'

    # Rotation about the origin.
    # Transformation matrices hard coded to avoid evaluating sin/cos w/ error
    def rotate(self, ccw_turns):
        self.position = inPlaneRot(self.position, ccw_turns)
        if (ccw_turns is 1) or (ccw_turns is 3):
            if self.align is not None:
                self.align = not self.align

    # Translates by trans = [x, y, z]
    def translate(self, trans):
        self.position = [self.position[i] + trans[i] for i in range(3)]

    def x(self):
        return self.position[0]

    def y(self):
        return self.position[1]

    def z(self):
        return self.position[2]

# BitBlox class defining a BitBlox as well as all of its rotational transformations
# Conveniently, all BitBlox only have 4 transformations, plus translations.
# As mentioned in the FGU class documentation, Bitblox are really just a collection 
# of FGU objects. Bitblox objects are initialized with their origin set to [0, 0, 0];
# translation and rotations not about the origin will update the origin coordiantes.

class Bitblox():

    # The user must create a list of FGU's to initialize a BitBlox.
    # This is tedious and will likely be done via a tool later.
    def __init__(self, name, FGU_list, env = None, color = None, cmap = None):
        self.FGU_list = FGU_list
        self.origin = [0, 0, 0]
        self.orientation = 0
        self.name = name
        self.color = color
        self.cmap = cmap
        if env is None:
            self.env = self.__findEnvelope()
        else:
            self.env = env

    def __repr__(self):
        return (self.name +' @ ' + str(self.origin) + ', ' + str(90*self.orientation) 
                + 'd w/ ' + str(len(self.FGU_list)) + ' FGUs')

    # You can add Bitblox together with '+'; it combines their FGUs.
    # Bitblox are not "re-homed" before combining; positions in space are conserved.
    # The first Bitblox in the add expression determines origin, orientation, etc.
    # Note that this does not create a new Bitblox, but rather "glues" them together
    # such that they can be transformed relative to the first one! This behavior is due
    # to the fact that while a new Bitblox object is instantiated, its FGU's are still
    # children of the summed Bitblox.
    def __add__(self, other):
        if other:
            newFGU = list(self.FGU_list)
            newFGU.extend(other.FGU_list)
            newName = self.name + '+' + other.name
            out = Bitblox(newName, newFGU)
            out.origin = self.origin
        else:
            out = self
        return out

    # This returns a list of the nets available on the Bitblox.
    def listNets(self):
        nets = []
        for n in self.FGU_list:
            if n.net is not None:
                nets.append(n.net)
        return list(set(nets))

    # Relative rotation about the Bitblox origin
    # Must compensate for any existing translation
    # (Rotate all FGU, then translate back)
    def rotate(self, ccw_turns):
        ccw_turns = ccw_turns % 4
        origin = self.origin
        self.translateTo((0, 0, 0))
        for fgu in self.FGU_list:
            fgu.rotate(ccw_turns)
        self.translate(origin)
        self.orientation = (self.orientation + ccw_turns) % 4

    # Absolute rotation about the Bitblox origin
    def rotateTo(self, rot):
        self.rotate(rot - self.orientation)

    # Relative rotation about an FGU - this FGU stays in place but may rotate.
    # Useful when looking for valid connections.
    def rotateAbout(self, axisFgu, ccw_turns):
        fguLoc = axisFgu.position
        self.rotate(ccw_turns)
        trans = [fguLoc[i] - axisFgu.position[i] for i in range(3)]
        self.translate(trans)

    # A true rotation of the Bitblox around 0, 0, 0 in global FGU coordinates.
    def globalRotate(self, ccw_turns):
        for fgu in self.FGU_list:
            fgu.rotate(ccw_turns)
        self.origin = inPlaneRot(self.origin, ccw_turns)
        self.orientation = (self.orientation + ccw_turns) % 4

    # Relative translation in FGU coordinates.
    def translate(self, trans):
        for fgu in self.FGU_list:
            fgu.translate(trans)
        self.origin = [self.origin[i] + trans[i] for i in range(3)]

    # Absolute translation in FGU coordinates.
    def translateTo(self, trans):
        if not (self.origin is trans):
            a = self.origin
            trans = [trans[i] - a[i] for i in range(3)]
            self.translate(trans)

    # Translates the origin back to home, and sets orientation to 0
    def reHome(self):
        self.rotateTo(0)
        self.translateTo((0, 0, 0))

    # For all these placement grid extremities, the trick is to shift FGU coordinates
    # .5 to the inside (+.5 xy for minimums, -.5 xy for maximums) before converting
    # to grid coordinates. Once converted, you can safely check for max.
    def minGridX(self):
        x = float("inf")
        for fgu in self.FGU_list:
            gridx = origin2grid([fgu.x()+.5, fgu.y()+.5, 0])
            if gridx[0] < x:
                x = gridx[0]
        return x

    def minGridY(self):
        y = float("inf")
        for fgu in self.FGU_list:
            gridy = origin2grid([fgu.x()-.5, fgu.y()+.5, 0])
            if gridy[1] < y:
                y = gridy[1]
        return y

    def minGridZ(self):
        z = float("inf")
        for fgu in self.FGU_list:
            if fgu.z()+.5 < z:
                z = fgu.z() + .5
        return int(round(z))

    def maxGridX(self):
        x = float("-inf")
        for fgu in self.FGU_list:
            gridx = origin2grid([fgu.x()-.5, fgu.y()-.5, 0])
            if gridx[0] > x:
                x = gridx[0]
        return x

    def maxGridY(self):
        y = float("-inf")
        for fgu in self.FGU_list:
            gridy = origin2grid([fgu.x()+.5, fgu.y()-.5, 0])
            if gridy[1] > y:
                y = gridy[1]
        return y

    def maxGridZ(self):
        z = float("-inf")
        for fgu in self.FGU_list:
            if fgu.z() - .5 > z:
                z = fgu.z() - .5
        return int(round(z))

    def minGridCorner(self):
        return (self.minGridX(), self.minGridY(), self.minGridZ())

    def maxGridCorner(self):
        return (self.maxGridX(), self.maxGridY(), self.maxGridZ())

    # This runs upon initialization to find the home-state grid envelope.
    def __findEnvelope(self):
        minc = self.minGridCorner()
        maxc = self.maxGridCorner()
        return [minc, maxc]

    # This can be called anytime to find the current transformed grid envelope.
    # The rotation messes min/max up a bit, so "matrix" is hard-coded here again.
    def gridEnvelope(self):
        origin = origin2grid(self.origin)
        rot = self.orientation

        if rot is 1:
            # -MaxY -> MinX, MinX -> MinY, -MinY -> MaxX, MaxX -> MaxY 
            out = [[-self.env[1][1], self.env[0][0], self.env[0][2]], 
                   [-self.env[0][1], self.env[1][0], self.env[1][2]]]
        elif rot is 2:
            # -MaxX -> MinX, -MaxY -> MinY, -MinX -> MaxX, -MinY -> MaxY 
            out = [[-self.env[1][0], -self.env[1][1], self.env[0][2]], 
                   [-self.env[0][0], -self.env[0][1], self.env[1][2]]]
        elif rot is 3:
            # MinY -> MinX, -MaxX -> MinY, MaxY -> MaxX, -MinX -> MaxY 
            out = [[self.env[0][1], -self.env[1][0], self.env[0][2]], 
                   [self.env[1][1], -self.env[0][0], self.env[1][2]]]
        else:
            out = self.env

        out = [ [out[0][i] + origin[i] for i in range(3)],
                [out[1][i] + origin[i] for i in range(3)] ]
        return out

    # Returns merged, transformed grid envelope between this and another BB.
    def mergedEnvelope(self, other):
        selfEnv = self.gridEnvelope()
        otherEnv = other.gridEnvelope()
        return ([min(selfEnv[0][i], otherEnv[0][i]) for i in range(3)],
                [max(selfEnv[1][i], otherEnv[1][i]) for i in range(3)] )

    # Finds centroid in FGU units, mostly for drawing.
    def findCenterFGU(self):
        env = self.gridEnvelope()
        gridc = [(env[0][0] - .5*(env[1][0] - env[0][0])),
                 (env[0][1] - .5*(env[1][1] - env[0][1])),
                 (env[0][2] - .5*(env[1][2] - env[0][2]))]
        return grid2origin(gridc)