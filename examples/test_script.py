import math
from matplotlib import pyplot as plt

Vt = 0.026
n = 100
Voc = 50
def linear(V):
    return (1 + (V / (n * Vt)))

def exponent(V):
    return math.exp((Voc - V)/(n*Vt))


expo = []
lin  = []
v = []

for i in range(10000):
    vin = 25 + 0.01 * i
    v.append(vin)
    expo.append(exponent(vin))
    lin.append(linear(vin))


plt.plot(v, expo)
plt.plot(v, lin)
plt.show()
    