#implementation of a Hopfield autoassociative network using simulateous updating technique

import numpy, math, random
import Image, ImageDraw #graphics

def createNetwork(n):
    matrix=numpy.array([0.0] * n * n)
    matrix.shape = (n,n)
    return matrix


def addPattern(p,m):
    #create a new matrix based on input pattern
    new=numpy.array([0.0]*len(p)*len(p))
    new.shape = (len(m),len(m))
    for i in range((len(m))):
        for j in range((len(m))):
            new[i][j] = p[i]*p[j]
    #add new matrix to old
    for i in range((len(m))):
        for j in range((len(m))):
            m[i][j]= m[i][j]+new[i][j]

def getActivation(input, net):
    activation = numpy.array([0.0] * len(input))
    activationMatrix = input * net #instantaeous update
    for i in range(len(input)):
        activation[i] = sum(activationMatrix[i])

    #threshold the activation
    activation = threshold(activation)
    return activation

def getOutput(input, net, maxIterations):
    print "input: ", input
    #print "shape of input: ", numpy.shape(input) #for debugging
    newActivation = getActivation(input, net)
    
    #now feed back thru and see if activation changes
    oldActivation = newActivation
    newActivation = getActivation(oldActivation, net)

    if numpy.array_equal(oldActivation, newActivation):
        print "network stabilized after 1 iteration"
        output = newActivation
    else:
        print "network not stable yet"
        count = 1
        while count < maxIterations and not numpy.array_equal(oldActivation, newActivation):
            count=count+1
            print "iteration: ", count
            oldActivation = newActivation
            newActivation = getActivation(oldActivation, net)
            output = newActivation
        if numpy.array_equal(oldActivation, newActivation):
            print "network stabilized after ", count, "iterations"
        else:
            print "needs more than ", maxIterations, " to stabilize or minimum is a temporal pattern"
        
    print "final output:", output
    return output


def threshold(array):
    for i in range((len(array))):
        if array[i] >0:
            array[i] = 1
        else:
            array[i] = -1
    return array

def drawPatterns(patterns, x, y):
    
    height = (len(patterns) * y *10 ) + (len(patterns) * 20)
    width = x *10 + 20

    im = Image.new('L', (width, height),127)
    draw = ImageDraw.Draw(im)

    x = 0
    y = 0
    
    for i in range(len(patterns)):
        y+=10
        for j in range(len(patterns[i])):
            #draw a rectangle
            if patterns[i][j] <0: c = 255
            else: c = 0
            draw.rectangle([x,y,x+10,y+10], fill=c)
            x+=10
            if (j+1)%6==0:
                x = 0
                y+=10
    # write to stdout
    im.save("test.png")

    im.show()

'''
#example from Luger p. 501
patterns = [[1,-1,1,-1,1],
            [-1,1,1,-1,-1],
            [1,1,-1,1,1]]
'''

#patterns 6 x 8 grid
'''
# letters A, B, C
patterns = [[-1,-1,1,1,-1,-1,
             -1,1,-1,-1,1,-1,
             1,-1,-1,-1,-1,1,
             1,-1,-1,-1,-1,1,
             1,1,1,1,1,1,
              1,-1,-1,-1,-1,1,
              1,-1,-1,-1,-1,1,
              1,-1,-1,-1,-1,1],
            [1,1,1,1,1,-1,
             1,-1,-1,-1,-1,1,
             1,-1,-1,-1,-1,1,
             1,1,1,1,1,-1,
             1,-1,-1,-1,-1,1,
             1,-1,-1,-1,-1,1,
             1,-1,-1,-1,-1,1,
             1,1,1,1,1,-1],
            [-1,-1,1,1,1,1,
             -1,1,-1,-1,-1,-1,
             1,-1,-1,-1,-1,-1,
             1,-1,-1,-1,-1,-1,
             1,-1,-1,-1,-1,-1,
             1,-1,-1,-1,-1,-1,
             -1,1,-1,-1,-1,-1,
             -1,-1,1,1,1,1]]
             '''

#block patterns
patterns = [[-1,-1,-1,1,1,1,
             -1,-1,-1,1,1,1,
             -1,-1,-1,1,1,1,
             -1,-1,-1,1,1,1,
             1,1,1,-1,-1,-1,
             1,1,1,-1,-1,-1,
             1,1,1,-1,-1,-1,
             1,1,1,-1,-1,-1],
            [-1,-1,1,1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,1,1,-1,-1],
            [-1,-1,-1,-1,-1,-1,
             -1,-1,-1,-1,-1,-1,
             1,1,1,1,1,1,
             1,1,1,1,1,1,
             -1,-1,-1,-1,-1,-1,
             -1,-1,-1,-1,-1,-1,
             1,1,1,1,1,1,
             1,1,1,1,1,1]]

#noisy versions of blck patterns
noisy = [[-1,-1,-1,1,1,1,
             -1,-1,1,1,1,1,
             -1,-1,-1,-1,1,1,
             -1,-1,-1,1,1,1,
             1,1,1,-1,-1,-1,
             1,1,1,-1,-1,-1,
             1,1,1,1,-1,-1,
             1,1,1,-1,1,-1],
            [-1,-1,1,1,-1,-1,
             -1,-1,1,-1,-1,-1,
             -1,-1,1,-1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,-1,1,-1,-1,
             -1,-1,1,1,-1,-1,
             -1,-1,1,1,1,-1,
             -1,-1,1,1,-1,-1],
            [1,1,-1,-1,-1,-1,
             1,1,-1,-1,-1,-1,
             1,1,1,1,1,1,
             1,1,1,1,1,1,
             -1,-1,-1,-1,-1,-1,
             -1,-1,1,-1,-1,-1,
             1,1,1,-1,-1,-1,
             1,1,1,1,-1,-1]]

drawPatterns(patterns, 6, 8) #pattern set and shape



NETWORK_SIZE = 48
hop = createNetwork(NETWORK_SIZE) #hopfield network with this many neurons
#instill patterns in network
for i in patterns:
    addPattern(i,hop)
print "weights: "
print hop

getOutput(patterns[2], hop, 10)

#test 
ins = []
outs = []

#noisy inputs
drawPatterns(noisy, 6, 8)
for i in noisy:
    out = getOutput(i, hop, 10)
    outs.append(out)

'''
#random inputs
for i in range(10):
    r = bin(random.getrandbits(48))[2:] #generate a random binary sequence
    #pad left to make size of pattern
    padding = NETWORK_SIZE - len(r)
    new = padding * [-1]
    for i in r:
        if i == '0':
            new.append(-1)
        else:
            new.append(1)
    ins.append(new)
    new = numpy.array(new)
    out = getOutput(new, hop, 10)
    outs.append(out)
drawPatterns(ins, 6, 8)
'''

drawPatterns(outs, 6, 8)
