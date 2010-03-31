# Back-Propagation Neural Network
# 
# Written in Python.  See http://www.python.org/
# Placed in the public domain.
# Original code by Neil Schemenauer <nas@arctrix.com>
# extended by Heather Dewey-Hagborg 
#
#
# This code id for 3 layer feedforward neural nets
# there is one bas node on the input layer
# the backpropogation learning method is illustrated
# visualizations depend on Python Imaging Library
# and Matplotlib


import math
import random
import string

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import Image, ImageDraw, sys




# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x):
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

class NN:
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.numberInputs = ni + 1 # +1 for bias node
        self.numberHiddens = nh
        self.numberOutputs = no

        # activations for nodes
        self.inputActivations = [1.0]*self.numberInputs
        self.hiddenActivations = [1.0]*self.numberHiddens
        self.outputActivations = [1.0]*self.numberOutputs
        
        # create weights
        self.inputWeights = makeMatrix(self.numberInputs, self.numberHiddens)
        self.outputWeights = makeMatrix(self.numberHiddens, self.numberOutputs)

        #error list
        self.errorHistory = []
        
        # set them to random values
        for i in range(self.numberInputs):
            for j in range(self.numberHiddens):
                self.inputWeights[i][j] = random.uniform(-0.2, 0.2)
        for j in range(self.numberHiddens):
            for k in range(self.numberOutputs):
                self.outputWeights[j][k] = random.uniform(-2.0, 2.0)


    def update(self, inputs):
        if len(inputs) != self.numberInputs-1:
            raise ValueError, 'wrong number of inputs'

        # input activations
        for i in range(self.numberInputs-1):
            self.inputActivations[i] = inputs[i]

        # hidden activations
        for j in range(self.numberHiddens):
            sum = 0.0
            for i in range(self.numberInputs):
                sum = sum + self.inputActivations[i] * self.inputWeights[i][j]
            self.hiddenActivations[j] = sigmoid(sum)

        # output activations
        for k in range(self.numberOutputs):
            sum = 0.0
            for j in range(self.numberHiddens):
                sum = sum + self.hiddenActivations[j] * self.outputWeights[j][k]
            self.outputActivations[k] = sigmoid(sum)

        return self.outputActivations[:]


    def backPropagate(self, reference, learningRate):
        if len(reference) != self.numberOutputs:
            raise ValueError, 'wrong number of reference values'

        # calculate error terms for output
        output_deltas = [0.0] * self.numberOutputs
        for k in range(self.numberOutputs):
            error = reference[k]-self.outputActivations[k]
            output_deltas[k] = dsigmoid(self.outputActivations[k]) * error

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.numberHiddens
        for j in range(self.numberHiddens):
            error = 0.0
            for k in range(self.numberOutputs):
                error = error + output_deltas[k]*self.outputWeights[j][k]
            hidden_deltas[j] = dsigmoid(self.hiddenActivations[j]) * error

        # update output weights
        for j in range(self.numberHiddens):
            for k in range(self.numberOutputs):
                change = output_deltas[k]*self.hiddenActivations[j]
                self.outputWeights[j][k] = self.outputWeights[j][k] + learningRate*change 

        # update input weights
        for i in range(self.numberInputs):
            for j in range(self.numberHiddens):
                change = hidden_deltas[j]*self.inputActivations[i]
                self.inputWeights[i][j] = self.inputWeights[i][j] + learningRate*change

        # calculate error
        error = 0.0
        for k in range(len(reference)):
            error = error + 0.5*(reference[k]-self.outputActivations[k])**2
        return error


    def test(self, patterns, _print=False):
        output = []
        for p in patterns:
            o = self.update(p[0])
            if _print: print p[0], '->', o
            output+= o
        return output

    def weights(self):
        print 'Input weights:'
        for i in range(self.numberInputs):
            print self.inputWeights[i]
        print
        print 'Output weights:'
        for j in range(self.numberHiddens):
            print self.outputWeights[j]

    def train(self, patterns, iterations=1000, learningRate=0.5, errorFloor=.001):
        #there are many ways to train
        #you can use a static # of iterations
        #you can use that in combination with an error floor (which we do here)
        #such that when error gets small enough you stop training
        #you can also analyze how much you error is decreasing over the past X iterations
        #and if the rate of decrease is less than a certain threshold break
        #anoher commonly used trick is to decrease the learning rate constant over time
        #to fine tune the learning
        # See Alpaydin, "Introduction to Machine Learning" Ch. 11.8 for more info
        
        for i in xrange(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                reference = p[1]
                self.update(inputs)
                error = error + self.backPropagate(reference, learningRate)
            self.errorHistory.append(error)
            if i % 50 == 0:
                print "Iteration ", i
                print 'error %-14f' % error
                self.test(patterns, _print=True)
                print
                print
            if error <= errorFloor:
                print "Good enough solution found"
                print "Iteration ", i
                print "Final Error: ", error
                self.test(patterns, _print=True)
                break

















    ################################################
            # visual interface
            #comment out the next 3 functions if
            #no visual  interface desired
    ################################################
            
    def drawTopology(self):
        #this function depends on Python Imaging Library
        #Comment this function out if you dont have the library
        width = 800
        height = 600
        im = Image.new('RGB', (width,height))

        draw = ImageDraw.Draw(im)

        layers = [self.numberInputs,self.numberHiddens,self.numberOutputs]
        layers.sort()
        max = layers[-1]

        #spacing = width /  #nodes + 2 for buffer +30 offset for size of ellipse
        distance = (width / (max +1)) 

        start = distance*((max - float(self.numberInputs))/2.0)

        layer1 = []
        for i in range(1,self.numberInputs+1):
           layer1.append(((start+distance*i)-30, 70, (start+distance*i)+30, 130))

        start = distance*((max - float(self.numberHiddens))/2.0)

        layer2 = []
        for i in range(1,self.numberHiddens+1):
            layer2.append(((start+distance*i)-30,270, (start+distance*i)+30,330))
            
        start = distance*((max - float(self.numberOutputs))/2.0)


        layer3 = []
        for i in range(1,self.numberOutputs+1):
            layer3.append(((start+distance*i)-30,470, (start+distance*i)+30,530))

        #draw connecting lines
        for i in range(len(layer1)):
            for j in range(len(layer2)):
                fromNode = layer1[i]
                toNode = layer2[j]
                fromCenter = ((fromNode[0] + fromNode[2])/2, (fromNode[1] + fromNode[3])/2)
                toCenter = ((toNode[0] + toNode[2])/2, (toNode[1] + toNode[3])/2)
                
                if self.inputWeights[i][j] < 1:
                    color = "blue"
                else:
                    color = "red"
                    
                draw.line((fromCenter, toCenter), fill=color, width = int(round(abs(self.inputWeights[i][j]))))

        #draw connecting lines
        for i in range(len(layer2)):
            for j in range(len(layer3)):
                fromNode = layer2[i]
                toNode = layer3[j]
                fromCenter = ((fromNode[0] + fromNode[2])/2, (fromNode[1] + fromNode[3])/2)
                toCenter = ((toNode[0] + toNode[2])/2, (toNode[1] + toNode[3])/2)

                if self.inputWeights[i][j] < 1:
                    color = "blue"
                else:
                    color = "red"
                    
                draw.line((fromCenter, toCenter), fill=color, width = int(round(abs(self.inputWeights[i][j]))))

        #draw nodes on top
        for i in range(len(layer1)):
           draw.ellipse(layer1[i], fill='white')
        for i in range(len(layer2)):
           draw.ellipse(layer2[i], fill='white')
        for i in range(len(layer3)):
           draw.ellipse(layer3[i], fill='white')
            
        del draw 

        # write to stdout
        im.save("test.png")

        im.show()

    def plotError(self):
        #this function depends on matplotlib
        #Comment this function out if you dont have the library
        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.errorHistory)
        plt.ylabel('Root Mean Squared error')
        plt.title('XOR error rate')

        
    def plotTestResults(self, testPats, results):
        #this function depends on matplotlib
        #Comment this function out if you dont have the library
        plt.subplot(212)
        #1 = black, 0 = white
        for i in range(len(testPats)):
                      
            #print "x: ", testPats[i][0][0], "y: ", testPats[i][0][1], "results: ", results[i]
            if results[i] <0: _color = "0" #black
            elif results[i] > 1: _color = "1" #white
            else: _color = str(results[i])
            plt.plot(testPats[i][0][0], testPats[i][0][1], color=_color, marker='.')
        
        
        a = [0,1,0,1]
        plt.axis(a)
        
        plt.xlabel('X input')
        plt.ylabel('Y input')
     

def demo():
    # Teach network XOR function
    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input + 1 bias, two hidden, and one output nodes
    n = NN(2, 2, 1)
    # train it with some patterns
    n.train(pat)
    #visualize
    n.drawTopology()
    n.plotError()
    
    
    
    #generate 50 test patterns
    testPats = []
    for i in range(1000):
        testPats.append([[random.uniform(0, 1),random.uniform(0,1)]])
    # test it
    z = n.test(testPats)
    
    n.plotTestResults(testPats, z)
    
    plt.show()
    print "plots generated"
    
    
    



if __name__ == '__main__':
    demo()