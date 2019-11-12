from bblist import *
from bitblox import *
from bbviz import drawBB, newWindow
from itertools import combinations, product
from math import floor, ceil
from msvcrt import getch
import pycosat

# This returns a list of anchor positions and orientations off bb2
# which causes net1 and net2 to be connected when bb1 is at the home
# position and orientation.

# This does not worry about collisions. It does worry about pin gender
# and orientation.

# Note that finding shorts consists of finding all matches for
# non-desireable net connections (all of them!)
# bb1 is the "fixed" (homed) block around which bb2 permutes.

# Align automatically makes sure only valid grid placements (props) are returned.
def findMatches(bb1, net1, bb2, net2):

    # Start by finding where net1 is
    # Directly build a list of where net2 can go
    female1 = []
    male1 = []
    for fgu in bb1.FGU_list:
        if fgu.net is net1:
            if fgu.gender is MALE:
                male1.append(fgu)
            elif fgu.gender is FEMALE:
                female1.append(fgu)

    # Likewise, find where net2 is, building same lists
    male2 = []
    female2 = []
    for fgu in bb2.FGU_list:
        if fgu.net is net2:
            if fgu.gender is MALE:
                male2.append(fgu)
            elif fgu.gender is FEMALE:
                female2.append(fgu)

    gc = lambda x,y: x.align is y.align

    # For each male/female pairing, check if orientations match,
    # then build connection list from all matching orientations
    matches = []
    bb1.reHome()
    for f1 in female1:
        for m2 in male2:
            matches.extend(permute(f1, bb2, m2, gc))

    for m1 in male1:
        for f2 in female2:
            matches.extend(permute(m1, bb2, f2, gc))

    # Finally, remove redundancy and return.
    return set(matches)

# Returns all the arrangements of 2 Bitblox which cause a physical collision.
# This means any overlap except male-female or female-male overlaps.
def findCollisions(bb1, bb2):

    collisions = []
    bb1.reHome()
    for fgu1 in bb1.FGU_list:
        if fgu1.gender is MALE:
            ok = FEMALE
        elif fgu1.gender is FEMALE:
            ok = MALE
        else:
            ok = 0
        gc = lambda x,y: (x.align is not y.align) or (y.gender is not ok)
        for fgu2 in bb2.FGU_list:
            collisions.extend(permute(fgu1, bb2, fgu2, gc))
    return set(collisions)

# Find all the different ways bb's anchor can be placed in order for fgu to land
# on top of the targ FGU. 
# Condition is a function of two FGUs and only adds to list if it returns True.
# Also trims results to only include actually placeable combinations.
def permute(targ, bb, fgu, condition):
    permute = []
    trans = [targ.position[i] - fgu.position[i] for i in range(3)]
    bb.translate(trans)
    for rot in range(4):
        bb.rotateAbout(fgu, 1)
        a = bb.getAnchor()
        if condition(targ, fgu) and (a[0] % 2 == a[1] % 2):
            permute.append((tuple(bb.getAnchor()), bb.orientation))
    return permute

# To convert an FGU anchor to a grid location:
#   -  Shift down .5 on z
#   -  Rotate 45 (we'll pick clockwise, but it doesn't matter)
#   -  Divide positions by sqrt(2)
#   -  Round to int for index purposes
# This will convert (1, 1, .5) to (1, 0, 0) and so forth: placement grid.
def fgu2grid(anchor):
    newAnchor = list(anchor)
    newAnchor[0] = int(round((anchor[0]*.707 + anchor[1]*.707)/1.414))
    newAnchor[1] = int(round((-anchor[0]*.707 + anchor[1]*.707)/1.414))
    newAnchor[2] = int(round(anchor[2] - .5))
    return newAnchor

# This will convert matches (encoded as FGU positions of bb2 about bb1 at home)
# to prop pairs (by b2p, which maps bb/position/rotation to proposition)
# Creating clauses from proposition pairs is done externally
# This function mostly translates pairs to every available spot in the workspace.
def match2props(bb1, bb2, matches, b2p, ws):
    bb1.reHome()
    proplist = []
    for m in matches:
        bb2.translateTo(m[0])
        bb2.rotateTo(m[1])
        offsets = [None, None, None]
        metablox = (bb1 + bb2)
        minc = metablox.minGridCorner()
        maxc = metablox.maxGridCorner()
        for i in range(3):
            freedom = int(round(ws[i] - (maxc[i] - minc[i])))
            offsets[i] = [j - minc[i] for j in range(freedom)]
        for c in product(offsets[0], offsets[1], offsets[2]):
            bb2g = fgu2grid(bb2.getAnchor())
            if c[1] < 0:
                import pdb; pdb.set_trace()
            prop = (b2p[(bb1, c[0], c[1], c[2], 0)], 
                    b2p[(bb2, bb2g[0] + c[0], bb2g[1] + c[1], bb2g[2] + c[2], m[1])])
            proplist.append(prop)
    return proplist

def solve():
    # A workspace is defined by a (x, y, z) tuple of available positions
    # in positional grid units.

    ws = (3, 3, 2)

    # For now, we define corresponding Bitblox of interest explicitly, though this
    # could easily be done automatically later. It is simply a list of Bitblox object
    # pairs directly corresponding to the netlist format.

    bb = [
        Bat(),
        But(),
        Led()
    ]

    cbb = [
        (bb[0], bb[1]),
        (bb[1], bb[2])
    ]

    cn = [
        ('PWR', 'B1'),
        ('B2', 'LED')
    ]

    # bb = [
    #     But(),
    #     But()
    # ]

    # cbb = [
    #     (bb[0], bb[1])
    # ]

    # cn = [
    #     ('B1', 'B1')
    # ]

    # OK, PUT THE PROBLEM TOGETHER!

    # First, compile the list of propositions. DIMACS CNF demands numbers, so we need
    # a mapping from numbers to Bitblox orientation/position. We will want to be able to
    # go from a type-anchor-rotation to number and back easily. Minisat has the added 
    # inconvenience that they must be sequential.

    # We accomplish this with two dictionaries. One takes a (bb x y z r) tuple as a
    # key to get proposition, while the other gets proposition and returns the
    # (bb x y z r) tuple.

    b2p = {}
    p2b = {}
    counter = 0
    for p in product(bb, range(ws[0]), range(ws[1]), range(ws[2]), range(4)):
        counter += 1
        b2p[(p[0], p[1], p[2], p[3], p[4])] = counter
        p2b[counter] = (p[0], p[1], p[2], p[3], p[4])
    trueProps = counter

    # OK, that's done. Now, we generate clauses preventing collision. This is done by
    # finding all colliding "matches" between every combination of 2 Bitblox, and 
    # finding every place that combo could happen in the workspace, then adding a 
    # (-A | -B) clause to the proposition list.

    # In parallel, we seek "electrical collisions" (shorts) by evaluating
    # undesireable net connections.

    exclusivePairs = []
    for combo in combinations(bb, 2):

        # Physical collision part
        collisions = findCollisions(combo[0], combo[1])
        exclusivePairs.extend(match2props(combo[0], combo[1], collisions, b2p, ws))

        # Electrical collision part
        for netCombo in product(combo[0].listNets(), combo[1].listNets()):
            # Do not mark as bad if the nets on these blox are meant to be connected
            # Check all entries of netlist, searching for this combo
            good = False;
            for i in range(len(cbb)):
                good = good or ((cbb[i] == (combo[0], combo[1])) and 
                                (cn[i] == (netCombo[0], netCombo[1])))
            print str(good) + ':   ' + str(netCombo)
            if not good:
                shorts = findMatches(combo[0], netCombo[0], combo[1], netCombo[1])
                shorts = match2props(combo[0], combo[1], shorts, b2p, ws)

    # Since these are exclusive, negate all propositions in the clauses.
    exclusivePairs.extend(shorts)
    for i in range(len(exclusivePairs)):
        exclusivePairs[i] = [-exclusivePairs[i][0], -exclusivePairs[i][1]]

    # Great, we got this far. Now, we generate clauses enforcing the connectability
    # requirement. This is done by finding clauses in DNF (uh-oh).
    # We convert to CNF linearly by introducing virtual propositions.
    # CNF = AND of ORS

    connectClauses = []
    for i in range(len(cbb)):
        connections = findMatches(cbb[i][0], cn[i][0], cbb[i][1], cn[i][1])
        orPairs = match2props(cbb[i][0], cbb[i][1], connections, b2p, ws)
        aux = []
        for op in orPairs:
            counter += 1
            aux.append(counter) 
            connectClauses.append([-counter, op[0]])
            connectClauses.append([-counter, op[1]])
        connectClauses.append(aux)

    # One more thing: unique blox requirement, or alternatively, total
    # interconnectedness requirement. This reads as "if there is a blox here, then
    # there cannot be that blox anywhere else." In logic, this translates to collision
    # on the blox space: for every blox, there must be clauses that read 
    # "it's not here or it's not there" for ever grid combination. The SAT is
    # falsified if the blox is both here and there for any two grid points.

    cnf = exclusivePairs + connectClauses

    import pdb; pdb.set_trace()



# def clauseViz(clauseList, p2b, lastTrue):
def clauseViz(clauseList, p2b, lastTrue):
    for clause in clauseList:
        if clause[0] <= lastTrue:
            prop1 = p2b[-clause[0]]
        if clause[1] <= lastTrue:
            prop2 = p2b[-clause[1]]
        print '=============================='
        print prop1
        print prop2
        getch()

def reduce(answer):
    out = []
    for a in answer:
        if a > 0:
            out.append(a)
    return out

#solve()