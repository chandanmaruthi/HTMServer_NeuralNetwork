__author__ = 'chandanmaruthi'
from nupic.research.TP10X2 import TP
import numpy
import os
import cPickle as pickle
# Step 1: create Temporal Pooler instance with appropriate parameters
tp = TP(numberOfCols=50, cellsPerColumn=5,
        initialPerm=0.5, connectedPerm=0.5,
        minThreshold=10, newSynapseCount=10,
        permanenceInc=0.1, permanenceDec=0.0,
        activationThreshold=8,
        globalDecay=0, burnIn=1,
        checkSynapseConsistency=False,
        pamLength=10)

path = os.path.abspath("/home/chandanmaruthi/chandan/code/brainscience/tptest.p")

# Step 2: create input vectors to feed to the temporal pooler. Each input vector
# must be numberOfCols wide. Here we create a simple sequence of 5 vectors
# representing the sequence A -> B -> C -> D -> E
x = numpy.zeros((5, tp.numberOfCols), dtype="uint32")
x[0,0:10]  = 1   # Input SDR representing "A", corresponding to columns 0-9
x[1,10:20] = 1   # Input SDR representing "B", corresponding to columns 10-19
x[2,20:30] = 1   # Input SDR representing "C", corresponding to columns 20-29
x[3,30:40] = 1   # Input SDR representing "D", corresponding to columns 30-39
x[4,40:50] = 1   # Input SDR representing "E", corresponding to columns 40-49


# Step 3: send this simple sequence to the temporal pooler for learning
# We repeat the sequence 10 times
test=1

if test == 0:

    for i in range(10):

        # Send each letter in the sequence in order
        for j in range(5):

            # The compute method performs one step of learning and/or inference. Note:
            # here we just perform learning but you can perform prediction/inference and
            # learning in the same step if you want (online learning).
            tp.compute(x[j], enableLearn = True, computeInfOutput = False)


            # This function prints the segments associated with every cell.$$$$
            # If you really want to understand the TP, uncomment this line. By following
            # every step you can get an excellent understanding for exactly how the TP
            # learns.
            #tp.printCells()

        # The reset command tells the TP that a sequence just ended and essentially
        # zeros out all the states. It is not strictly necessary but it's a bit
        # messier without resets, and the TP learns quicker with resets.
        #tp.reset()
    objNetworkDump = open(path, "wb")
    pickle.dump(tp,objNetworkDump)

else:
        tp=None

        objNetworkDump = open(path, "rb")
        tp = pickle.load(objNetworkDump)

        tp._initEphemerals()

        print "oopla oopla"

# Step 4: send the same sequence of vectors and look at predictions made by
# temporal pooler

# Utility routine for printing the input vector
def formatRow(x):
    s = ''
    for c in range(len(x)):
        if c > 0 and c % 10 == 0:
            s += ' '
        s += str(x[c])
    s += ' '
    return s


for j in range(5):
    print "\n\n--------","ABCDE"[j],"-----------"
    print "Raw input vector\n",formatRow(x[j])

    # Send each vector to the TP, with learning turned off
    tp.compute(x[j], enableLearn=False, computeInfOutput=True)

    # This method prints out the active state of each cell followed by the
    # predicted state of each cell. For convenience the cells are grouped
    # 10 at a time. When there are multiple cells per column the printout
    # is arranged so the cells in a column are stacked together
    #
    # What you should notice is that the columns where active state is 1
    # represent the SDR for the current input pattern and the columns where
    # predicted state is 1 represent the SDR for the next expected pattern
    print "\nAll the active and predicted cells:"
    tp.printStates(printPrevious=False, printLearnState=False)

    # tp.getPredictedState() gets the predicted cells.
    # predictedCells[c][i] represents the state of the i'th cell in the c'th
    # column. To see if a column is predicted, we can simply take the OR
    # across all the cells in that column. In numpy we can do this by taking
    # the max along axis 1.
    print "\n\nThe following columns are predicted by the temporal pooler. This"
    print "should correspond to columns in the *next* item in the sequence."
    predictedCells = tp.getPredictedState()
    #print predictedCells.max(axis=1).nonzero()
    print formatRow(predictedCells.max(axis=1).nonzero())