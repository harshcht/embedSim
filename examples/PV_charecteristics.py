import sys
sys.path.insert(0, '../')

import Models_lib as models
from matplotlib import pyplot as plt

nodes = models.createNodes(3)
pv = models.PV_Source(1,0,2,8,40, 100)

Vpv = []
Ipv= []

n = 1000
vmax = 40
power = []
for i in range(n):
    v = i * vmax / n
    models.putNodeVal(1, v)
    models.execAll(1, 10)
    Vpv.append(v)
    Ipv.append(models.getNodeValue(pv.nd_i))
    power.append(v * models.getNodeValue(pv.nd_i))

#plt.plot(Vpv, Ipv)
plt.plot(Vpv, power)
plt.xlabel("voltage (V)")
plt.ylabel("power (W)")
plt.show() 