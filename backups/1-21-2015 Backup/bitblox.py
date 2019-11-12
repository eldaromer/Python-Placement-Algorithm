MALE = True
FEMALE = False
NW = True
NE = False

# To convert an FGU location to a grid location:
#   -  Shift down .5 on z (because anchors are always offset .5 from unit grid)
#   -  Rotate 45 (we'll pick clockwise, but it doesn't matter)
#   -  Divide positions by sqrt(2)
#   -  Round to int for index purposes
# This will convert (1, 1, .5) to (1, 0, 0) and so forth: placement grid.
def anchor2grid(anchor):
    newAnchor = list(anchor)
    newAnchor[0] = int(round((anchor[0]*.707 + anchor[1]*.707)/1.414))
    newAnchor[1] = int(round((-anchor[0]*.707 + anchor[1]*.707)/1.414))
    newAnchor[2] = int(round(anchor[2] - .5))
    return newAnchor

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

    # Transformation matrices hard coded to avoid evaluating sin/cos w/ error
    def rotate(self, ccw_turns):
        ccw_turns = ccw_turns % 4
        if ccw_turns is 1:
            self.position = [-self.y(), self.x(), self.z()]
            if self.align is not None:
                self.align = not self.align
        elif ccw_turns is 2:
            self.position = [-self.x(), -self.y(), self.z()]
        elif ccw_turns is 3:
            self.position = [self.y(), -self.x(), self.z()]
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
# Conveniently, and and all BitBlox only have 4 transformations, plus translations
# Really a collection of FGU objects. There is no FGU at the origin.

# An important note on anchors:
#   - Anchors are required to transform FGU coordinates to grid coordinates
#   - The anchor is contained within the 1/2 radius with Z = 0:
#       - [.5, .5, 0] [.5 -.5 0] [-.5 -.5 0] [-.5 .5 0]
#       - It is the origin.
#   - Fortunately, this is invariant with rotation - no need to track it.
#   - Origin is still a valid reference point for merging two BitBlox
#   - Additional caveat is 45 degree rotation between grids - can be done after SAT.

class BitBlox():

    # The user must create a list of FGU's to initialize a BitBlox.
    # This is tedious and will likely be done via a tool later.
    # Anchor is located at centroid of anchor FGU's.
    def __init__(self, name, FGU_list, anchorFGUs):
        self.FGU_list = FGU_list
        self.anchorFGUs = anchorFGUs
        self.orientation = 0
        self.name = name

    def __repr__(self):
        return (self.name +' @ ' + str(self.getAnchor()) + ', ' + str(90*self.orientation) 
                + 'd w/ ' + str(len(self.FGU_list)) + ' FGUs')

    # You can add Bitblox into meta-blox!
    # The first Bitblox in the add expression determines anchor, orientation, etc.
    def __add__(self, other):
        newFGU = list(self.FGU_list)
        newFGU.extend(other.FGU_list)
        newName = self.name + '+' + other.name
        newAnchors = self.anchorFGUs
        return BitBlox(newName, newFGU, newAnchors)

    # This returns a list of the nets available on the Bitblox.
    def listNets(self):
        nets = []
        for n in self.FGU_list:
            nets.append(n.net)
        return list(set(nets))

    # Must compensate for any existing translation
    # (Rotate all FGU, then translate back)
    def rotate(self, ccw_turns):
        ccw_turns = ccw_turns % 4
        anchor = self.getAnchor()
        for fgu in self.FGU_list:
            fgu.rotate(ccw_turns)
        newAnchor = self.getAnchor()
        trans = [anchor[i] - newAnchor[i] for i in range(3)]
        self.translate(trans)
        self.orientation = (self.orientation + ccw_turns) % 4

    def rotateTo(self, rot):
        self.rotate(rot - self.orientation)

    # The FGU passed here must one of this Bitblox's children
    def rotateAbout(self, axisFgu, ccw_turns):
        fguLoc = axisFgu.position
        for fgu in self.FGU_list:
            fgu.rotate(ccw_turns)
        newLoc = axisFgu.position
        trans = [fguLoc[i] - newLoc[i] for i in range(3)]
        self.translate(trans)
        self.orientation = (self.orientation + ccw_turns) % 4

    def translate(self, trans):
        for fgu in self.FGU_list:
            fgu.translate(trans)

    def translateTo(self, trans):
        a = self.getAnchor()
        trans = [trans[i] - a[i] for i in range(3)]
        self.translate(trans)

    # Translates the anchor back to home, and orientation 0
    # A "homed" anchor is at (0, 0, .5)
    def reHome(self):
        self.rotateTo(0)
        self.translateTo([0, 0, .5])

    def getAnchor(self):
        anchor = [0, 0, 0]
        for n in self.anchorFGUs:
            fgu = self.FGU_list[n]
            anchor[0] += fgu.position[0]
            anchor[1] += fgu.position[1]
            anchor[2] += fgu.position[2]
        out = [a / 4 for a in anchor]
        return out

    # For all these placement grid extremities, the trick is to shift FGU coordinates
    # .5 to the inside (+.5 xy for minimums, -.5 xy for maximums) before converting
    # to grid coordinates. Once converted, you can safely check for max.
    def minGridX(self):
        x = float("inf")
        for fgu in self.FGU_list:
            gridx = anchor2grid([fgu.x()+.5, fgu.y()+.5, .5])
            if gridx[0] < x:
                x = gridx[0]
        return x

    def minGridY(self):
        y = float("inf")
        for fgu in self.FGU_list:
            gridy = anchor2grid([fgu.x()-.5, fgu.y()+.5, .5])
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
            gridx = anchor2grid([fgu.x()-.5, fgu.y()-.5, .5])
            if gridx[0] > x:
                x = gridx[0]
        return x

    def maxGridY(self):
        y = float("-inf")
        for fgu in self.FGU_list:
            gridy = anchor2grid([fgu.x()+.5, fgu.y()-.5, .5])
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

