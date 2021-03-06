
import random
import numpy as np
import collections
from statistics import mean
from sklearn import preprocessing as pp
import copy

class neural_network:
    layers = []

    previous_fitness = collections.deque([ 0 for x in range(40)])

    fitness = 0.0

    MUTATION_RATE = 0.05

    MUTATION_STRENGTH = 0.5

    def init_neurons(self):
        self.neurons = []
        for i in self.layers:
            self.neurons.append([0 for i in range(i)]) 

    def init_biases(self):
        self.biases = []
        for i in self.layers:
            self.biases.append([random.uniform(-0.1,0.1) for j in range(i)])

    def init_weights(self):
        self.weights = []
        for i in range(1,len(self.layers)):
            layers_weights_list = []
            neurons_previous_layer = self.layers[i-1]
            for j in range(len(self.neurons[i])):
                neuron_weights = []
                for k in range(neurons_previous_layer):
                    neuron_weights.append(random.uniform(-1.0,1.0))
                layers_weights_list.append(neuron_weights)
            self.weights.append(layers_weights_list)

    # creates topology of network as specified by layers
    def __init__(self, layers):
        self.layers = layers
        
        self.init_neurons()
        self.init_biases()
        self.init_weights()
    
    # alters the network by feeding inputs through it, with a relu activation function
    def feed_forward(self, inputs):
        inputs = pp.normalize([inputs])
        inputs = inputs[0]
        for i in range(len(inputs)):
            self.neurons[0][i] = inputs[i]

        for i in range(1,len(self.layers)):
            layer = i - 1 # need to calculate sum of all values in previous layer according to bias
            for j in range(len(self.neurons[i])):
                val = 0.0 # the sum of the activations of all nodes in the previous layer
                for k in range(len(self.neurons[i-1])):
                    val += self.weights[i-1][j][k] * self.neurons[i-1][k]; # the sum of an indivual node in previous layer

                #if layer == len(self.layers)-2:
                    #self.neurons[i][j] = rectified(val + self.biases[i][j]) # feed it forward!
                #else:
                    self.neurons[i][j] = rectified(val + self.biases[i][j]) # feed it forward!

        return self.neurons[1] # return the last layer in the network as the outputs

    # allows the fitness of the neural network to be set
    def set_fitness(self,fitness):
        self.previous_fitness.popleft()
        self.previous_fitness.append(fitness)
        self.fitness = mean(self.previous_fitness)


    def mutate(self):
        # randomly mutate the biases
        # recall that the biases are a number associated with each node
        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                if (random.random() < self.MUTATION_RATE):
                    self.biases[i][j] +=  random.uniform(-self.MUTATION_STRENGTH, self.MUTATION_STRENGTH)


        # randomly mutate the weights
        # recall that the weights are the "edges" between the nodes of two layers in a network. 

        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    if (random.random() < self.MUTATION_RATE):
                        self.weights[i][j][k] += random.uniform(-self.MUTATION_RATE, self.MUTATION_STRENGTH)

    def crossover(self, other):
        net = copy.deepcopy(self)
        # randomly mutate the biases
        # recall that the biases are a number associated with each node
        for i in range(len(self.biases)):
            for j in range(len(self.biases[i])):
                coin = random.randint(0,1)
                if coin:
                    net.biases[i][j] = other.biases[i][j]


        # randomly mutate the weights
        # recall that the weights are the "edges" between the nodes of two layers in a network. 

        for i in range(len(self.weights)):
            for j in range(len(self.weights[i])):
                for k in range(len(self.weights[i][j])):
                    coin = random.randint(0,1)
                    if coin:
                        net.weights[i][j][k] = other.weights[i][j][k]
        return net


    def save(self):
        file = open('optimal_model.txt', 'w')
        
        try:
            data = []
            for i in range(len(self.biases)):
                for j in range(len(self.biases[i])):
                    data.append( str(self.biases[i][j]) + '\n')

            for i in range(len(self.weights)):
                for j in range(len(self.weights[i])):
                    for k in range(len(self.weights[i][j])):
                        data.append( str(self.weights[i][j][k]) + '\n' )

            file.writelines(data)
        finally:
            file.close()

    def load(self):
        file = open('optimal_model.txt', 'r')
        try:
            index = 0
            lines = file.readlines()
            for i in range(len(self.biases)):
                for j in range(len(self.biases[i])):
                    self.biases[i][j] = float(lines[index])
                    index+=1
            
            for i in range(len(self.weights)):
                for j in range(len(self.weights[i])):
                    for k in range(len(self.weights[i][j])):
                        self.weights[i][j][k] = float(lines[index])
                        index+=1
        finally:
            file.close()

# sigmoid
def rectified(x):
	return max(0.0, x)


# modified, from 
# https://medium.com/@omkar.nallagoni/activation-functions-with-derivative-and-python-code-sigmoid-vs-tanh-vs-relu-44d23915c1f4
def sigmoid(x):
    s=1/(1+np.exp(-x))
    return s