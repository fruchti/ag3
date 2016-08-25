#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy
import math

def getrand(p):
    return numpy.random.choice(numpy.arange(0, len(p)), p = p)

p = [0.3, 0.7]
p_1 = [0.4, 0.6]
p_2 = [0.5, 0.5]

avg = 0
for i in range(len(p)):
    avg += p[i] * math.log(p_1[i] / p_2[i])

randplot = []
avgplot = []
logsum = 0
for i in range(10000):
    randplot.append(logsum)
    x_i = getrand(p)
    logsum += math.log(p_1[x_i] / p_2[x_i])

    avgplot.append(i * avg)

plt.plot(randplot)
plt.plot(avgplot)
plt.show()
