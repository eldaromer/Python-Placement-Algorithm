from bitblox import *
from bbviz import drawBB
from itertools import combinations, product
from time import time
from copy import deepcopy
from random import randint
import pycosat

# This returns a list of Bitblox origins and orientations of bb2
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

# Find all the different ways bb can be placed in order for fgu to land
# on top of the targ FGU. 
# Condition is a function of two FGUs and only adds to list if it returns True.
def permute(targ, bb, fgu, condition):
    permute = []
    trans = [targ.position[i] - fgu.position[i] for i in range(3)]
    bb.translate(trans)
    for rot in range(4):
        bb.rotateAbout(fgu, 1)
        a = bb.origin
        if condition(targ, fgu) and (a[0] % 2 == a[1] % 2):
            permute.append((tuple(bb.origin), bb.orientation))
    return permute

# Returns all the arrangements of 2 Bitblox which cause a physical collision.
# This means any overlap except male-female or female-male overlaps.
# TODO: Operate on grid space to save computation. As it stands, a single arrangement
# is discovered and recorded many times.
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

# This will convert matches (encoded as FGU positions of bb2 about bb1 at home)
# to prop pairs (by b2p, which maps bb/position/rotation to proposition)
# Creating clauses from proposition pairs is done externally
# This function mostly transforms pairs to every available spot in the workspace.
def match2props(bb1, bb2, matches, b2p, ws):
    proplist = []
    offsets = [0, 0, 0]
    bb1.reHome()
    for m in matches:
        bb2.translateTo(m[0])
        bb2.rotateTo(m[1])              
        for rot in [1, 2, 3, 0]:
            bb1.globalRotate(1)
            bb2.globalRotate(1)
            metablox = (bb1 + bb2)
            minc = metablox.minGridCorner()
            maxc = metablox.maxGridCorner()
            for i in range(3):
                freedom = int(round(ws[i] - (maxc[i] - minc[i])))
                offsets[i] = [j - minc[i] for j in range(freedom)]
            bb2g = origin2grid(bb2.origin)
            for k in product(offsets[0], offsets[1], offsets[2]):
                prop = (b2p[(bb1, k[0], k[1], k[2], rot)], 
                        b2p[(bb2, bb2g[0] + k[0], bb2g[1] + k[1], bb2g[2] + k[2], bb2.orientation)])
                proplist.append(prop)
    return proplist

# Same as solve, but uses the extra connector allowance to iteratively solve a 
# potentially overconstrained schematic. Default max. tries is 10.
# Right now, the relaxation method is a fairly naive random mutation.
# It returns an edited schematic which does satisfy the problem.
def autosolve(schematic, tries = 10):
    counter = 0; done = False
    iSchematic = deepcopy(schematic)
    while (counter < tries) and not done:
        counter = counter + 1
        print "Trial " + str(counter)
        print "--------------------------"
        done = solve(iSchematic)
        print "--------------------------"

        # If failed, pick a random extensible connection, and extend it.
        if not done:
            if sum(iSchematic.pb) < 1:
                print "Failed to autosolve. Problem maximally expanded."
                return False
            goodPick = False
            while not goodPick:
                pick = randint(0, len(iSchematic.cn) - 1)
                if iSchematic.pb[pick] > 0:
                    goodPick = True
            iSchematic.expand(pick)
    return iSchematic


# This function will take the Bitblox pairs in cbb and connect their corresponding nets
# in cn, if possible. It operates directly on the Bitblox found in cbb. It will return
# True if it found a solution, and False otherwise. It will only search for solutions
# that fit in workspace (placement grid) area ws.
def solve(schematic):

    # First, compile the list of propositions. DIMACS CNF demands numbers, so we need
    # a mapping from numbers to Bitblox orientation/position. We will want to be able to
    # go from a type-origin-rotation to number and back easily. Minisat has the added 
    # inconvenience that they must be sequential.

    # We accomplish this with two dictionaries. One takes a (bb x y z r) tuple as a
    # key to get proposition, while the other gets proposition and returns the
    # (bb x y z r) tuple.

    # While we're doing this, we also make uniqueness clases - in other words,
    # "it's not here or it's not there" for every grid combination per BB. The SAT is
    # falsified if the blox is both here and there for any two grid points.
    # This is every combination. Not so bad - another "n choose 2" type of deal.

    # Extract useful variables from schematic structure
    bb = schematic.listBitblox()
    ws = schematic.ws
    cbb = schematic.cbb
    cn = schematic.cn

    # Build all propositions. The proposition space is bb x grid slots x 4.
    # In parallel, build uniqueness clauses that enforce only one instance of
    # each Bitblox in the final solution. There are many, but they are cheap to make.
    print "Building proposition set"
    b2p = {}
    p2b = {}
    counter = 0
    uniquenessClauses = []
    for bbx in bb:
        firstBBX = counter + 1
        for p in product(range(ws[0]), range(ws[1]), range(ws[2]), range(4)):
            counter += 1
            b2p[(bbx, p[0], p[1], p[2], p[3])] = counter
            p2b[counter] = (bbx, p[0], p[1], p[2], p[3], )
        for i in combinations(range(firstBBX, counter + 1), 2):
            uniquenessClauses.append([-i[0], -i[1]])
    trueProps = counter
    print str(trueProps) + " propositions generated."
    print str(len(uniquenessClauses)) + " uniqueness clauses generated."

    # OK, that's done. Now, we generate clauses preventing collision. This is done by
    # finding all colliding "matches" between every combination of 2 Bitblox, and 
    # finding every place that combo could happen in the workspace, then adding a 
    # (-A | -B) clause to the proposition list.

    # In parallel, we seek "electrical collisions" (shorts) by evaluating
    # undesireable net connections.

    collisions = []
    shorts = []
    for combo in combinations(bb, 2):

        # Physical collision part
        col = findCollisions(combo[0], combo[1])
        collisions.extend(match2props(combo[0], combo[1], col, b2p, ws))

        # Electrical collision part
        for netCombo in product(combo[0].listNets(), combo[1].listNets()):

            # Do not mark as bad if the nets on these blox are meant to be connected
            # Check all entries of netlist, searching for this combo
            good = False;
            for i in range(len(cbb)):
                oneWay = ((cbb[i] == (combo[0], combo[1])) and 
                                (cn[i] == (netCombo[0], netCombo[1])))
                otherWay = ((cbb[i] == (combo[1], combo[0])) and 
                                (cn[i] == (netCombo[1], netCombo[0])))
                good = good or oneWay or otherWay
            if not good:
                sh = findMatches(combo[0], netCombo[0], combo[1], netCombo[1])
                shorts.extend(match2props(combo[0], combo[1], sh, b2p, ws)) 

    print str(len(collisions)) + " collision clauses generated."
    print str(len(shorts)) + " short clauses generated."
    
    # Since these are exclusive, negate all propositions in the clauses.
    exclusivePairs = collisions + shorts
    for i in range(len(exclusivePairs)):
        exclusivePairs[i] = [-exclusivePairs[i][0], -exclusivePairs[i][1]]

    # Great, we got this far. Now, we generate clauses enforcing the connectability
    # requirement. This is done by finding clauses in DNF (uh-oh).
    # We convert to CNF linearly by introducing virtual propositions.
    # Remember, CNF = AND of ORS, DNF = OR of ANDS

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
    print str(len(connectClauses)) + " connection clauses generated."

    # Finally, the user may have specified that certain blox be fixed in the problem
    # structure. This is easy - just AND that particular proposition with the whole
    # problem.
    fixed = []
    for f in schematic.fixed:
        fixed.append([b2p[f]])

    # Great, that's all the requirements. Concatenate them here, and call PicoSAT.
    cnf = exclusivePairs + connectClauses + uniquenessClauses + fixed
    
    print "Calling PicoSAT..."
    t = time()
    soln = pycosat.solve(cnf)
    t = time() - t
    print "Solution took " + str(t) + " seconds."
    if str(soln) == 'UNSAT':
        print "No solution found. Returning conflict metric."
        return False
    else:
        true = trueOnly(soln, trueProps)
        print 'Solution: ' + str(true)
        print 'Recording solution...'
        if not true:
            print 'Something went wrong - solution is empty.'
            print 'Entering debugger.'
            import pdb; pdb.set_trace()
        else:
            out = []
            for lit in true:
                pos = p2b[lit]
                out.append(pos)
                print str(lit) + ' -> ' + str(pos)
            schematic.soln.append(out)
            return True

# Utility function that trims a solution from pycosat such that it only contains the
# positive (true) literals, and ignores virtual literals (literals above trueProps).
# You can choose to keep virtual literals by setting includeExtra to True.
def trueOnly(answer, trueProps, includeExtra = False):
    out = []
    for a in answer:
        if a > 0 and ((a < trueProps) or (includeExtra)):
            out.append(a)
    return out

# For debugging: Given a lit of propositions and the proposition -> Bitblox dictionary,
# draw all the propositions for the sake of visualization.
def drawPropositions(props, p2b):
    out = []
    for bb in props:
        pos = p2b[bb]
        cop = deepcopy(pos[0])
        cop.translateTo(grid2origin(pos[1:4]))
        cop.rotateTo(pos[4])
        out = cop + out
    drawBB(out, grid = True, gridRadius = 2)

# For debugging: Given a list of propositions (of the PicoSAT CNF form), find a
# clause in cnf which causes falsification.
def falsify(props, cnf):
    props = set(props)
    for i, clause in enumerate(cnf):
        falsified = True
        for lit in clause:
            if lit in props:
                falsified = False
                break
            elif ((lit < 0) and (not -lit in props)):
                falsified = False
                break
        if falsified:
            print "Input " + str(props) + " falsified by:"
            print str(clause) + " @ index " + str(i)
    print "Done searching."

# For debugging: Find clauses and indices which contain the given literal
def lookup(lit, cnf):
    for i, clause in enumerate(cnf):
        for litB in clause:
            if (lit == litB):
                print str(clause) + " @ index " + str(i)

# For debugging: Cycle through drawing every permutation of bb2 around bb1.
# Meant to operate on the output of the permute function.
def showMe(bb1, bb2, perm):
    print "Drawing " + str(len(perm)) + " arrangements..." 
    bb1.reHome()
    for p in perm:
        bb2.translateTo(p[0])
        bb2.rotateTo(p[1])
        drawBB(bb1 + bb2)
        raw_input("Press enter to draw next...")