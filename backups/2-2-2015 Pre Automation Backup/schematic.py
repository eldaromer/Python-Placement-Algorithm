from bitblox import *
from bblist import Pass
from bbviz import drawBB

# This is an object representing a schematic, which is
#   - A 3-tuple representing the workspace
#   - A list of tuples representing paired Bitblox, cbb ('connection bitblox')
#   - A list of tuples representing corresponding net connections, cn ('connection nets')
#   - A list of ints representing the maximum range of 
#     allowed intermediate connectors pb ('pass blocks') [OPTIONAL]
#   - A list of known solutions, where a solution is a list of (bitblox, x, y, z, r)
#     tuples of the form use in formulate.py
#   - A list of fixed bitblox

# This class mostly serves as a data structure for easy passing between functions.

class schematic():

    def __init__(self, ws, cbb = [], cn = [], pb = None, fixed = [], name = "Schematic"):
        self.ws = ws
        self.cbb = cbb
        self.cn = cn
        self.fixed = fixed
        self.name = name
        if pb is None:
            self.pb = []
            for i in self.cn:
                self.pb.append(0)
        else:
            self.pb = pb
        self.soln = []

    # Makes sure the proposition is enforced in future solutions.
    # Prop is of form (Bitblox, x, y, z, r) as in formulate.
    def fix(self, prop):
        self.fixed.append(prop)

    def listBitblox(self):
        bb = []
        for pair in self.cbb:
            bb = bb + list(pair)
        return list(set(bb))

    def applySolution(self, n = 0):
        if self.soln:
            print "Applying solution " + str(n)
            for pos in self.soln[n]:
                pos[0].translateTo(grid2origin(pos[1:4]))
                pos[0].rotateTo(pos[4])
        else:
            print "No solutions are stored!"

    def showSolution(self, n = 0):
        if self.soln:
            self.applySolution(n)
            print "Rendering solution..."
            drawBB(assemble(self.listBitblox()), grid = False, center = self.ws)
        else:
            print "No solutions are stored!"

    def listConnections(self):
        for i in range(len(self.cbb)):
            print (self.cn[i][0] + ' on ' + self.cbb[i][0].name + " to " + 
                   self.cn[i][1] + ' on ' + self.cbb[i][1].name)

    def addConnection(self, bb1, net1, bb2, net2, pmax = 0):
        self.cbb.append((bb1, bb2))
        self.cn.append((net1, net2))
        self.pb.append(pmax)

    def relaxAll(self, pmaxGlobal):
        for i, pbn in enumerate(self.pb):
            self.pb[i] = (self.pb[i][0], pmaxGlobal)

    # Expands netlist entry n to include an additional connector block.
    def expand(self, n):
        oldCbb = self.cbb[n]
        oldCn = self.cn[n]
        oldMax = self.pb[n]
        del self.pb[n]
        del self.cbb[n]
        del self.cn[n]
        newPass = Pass()
        self.addConnection(oldCbb[0], oldCn[0], newPass, 'P', oldMax - 1)
        self.addConnection(newPass, 'P', oldCbb[1], oldCn[1])

