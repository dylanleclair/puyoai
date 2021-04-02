import matplotlib.pyplot as pyplot

# data is the fitness value over generation
def graph_fitness_over_generations(data):
    y = [float(x) for x in data]
    x = [z for z in range(len(y))]
    pyplot.plot(x,y)
    pyplot.savefig('output.pdf')
    pyplot.savefig('outputaspng.png')