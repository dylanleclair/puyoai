import matplotlib.pyplot as pyplot

file = open('results.txt', 'r')

y = [float(x) for x in file.readlines()]
x = [z for z in range(len(y))]

pyplot.plot(x,y)

pyplot.show()