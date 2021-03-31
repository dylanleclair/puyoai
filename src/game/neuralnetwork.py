
import random
import numpy as np

class neural_network:
    layers = []

    fitness = 0.0

    def init_neurons(self):
        self.neurons = []
        for i in self.layers:
            self.neurons.append([0 for i in range(i)]) 

    def init_biases(self):
        self.biases = []
        for i in self.layers:
            self.biases.append([random.uniform(-0.5,0.5) for j in range(i)])

    def init_weights(self):
        self.weights = []
        for i in range(1,len(self.layers)):
            layers_weights_list = []
            neurons_previous_layer = self.layers[i-1]
            for j in range(len(self.neurons[i])):
                neuron_weights = []
                for k in range(neurons_previous_layer):
                    neuron_weights.append(random.uniform(-0.5,0.5))
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
        
        for i in range(len(inputs)):
            self.neurons[0][i] = inputs[i]

        for i in range(1,len(self.layers)):
            layer = i - 1 # need to calculate sum of all values in previous layer according to bias
            for j in range(len(self.neurons[i])):
                val = 0.0 # the sum of the activations of all nodes in the previous layer
                for k in range(len(self.neurons[i-1])):
                    val += self.weights[i-1][j][k] * self.neurons[i-1][k]; # the sum of an indivual node in previous layer

            if layer == len(self.layers)-2:
                self.neurons[i][j] = sigmoid(val + self.biases[i][j]) # feed it forward!
            else:
                self.neurons[i][j] = rectified(val + self.biases[i][j]) # feed it forward!


        return self.neurons[len(self.neurons) -1] # return the last layer in the network as the outputs

    # allows the fitness of the neural network to be set
    def set_fitness(self,fitness):
        self.fitness = fitness

# sigmoid
def rectified(x):
	return max(0.0, x)


# modified, from 
# https://medium.com/@omkar.nallagoni/activation-functions-with-derivative-and-python-code-sigmoid-vs-tanh-vs-relu-44d23915c1f4
def sigmoid(x):
    s=1/(1+np.exp(-x))
    return s