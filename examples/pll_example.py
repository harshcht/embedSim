import math

import sys
sys.path.insert(0, '../')

import Models_lib as models
from matplotlib import pyplot as plt

nodes = models.createNodes(4)
src1 = models.sine_source(50, 0, 1, 0)
src2 = models.sine_source(50, 1, 1, 0)

class multiplier :
    nd1 = 0
    nd2 = 0
    nd_out = 0
    def __init__(self, nd1, nd2, nd_out) :
        self.nd1 = nd1
        self.nd2 = nd2
        self.nd_out = nd_out
        models.parts.append(self)
    def Exec(self, time):
        v1 = models.getNodeValue(self.nd1)
        v2 = models.getNodeValue(self.nd2)
        vout = v1 * v2
        models.putNodeVal(self.nd_out, 2*vout)


class filter :
    nd_in = 0
    nd_out = 0
    buff_size = 0
    time_div = 0
    t_pre = 0
    v_buff = []
    sum =0 
    def __init__(self, nd_in, nd_out, time_div, n_samples):
        self.nd_in = nd_in
        self.nd_out = nd_out
        self.time_div = time_div
        self.buff_size = n_samples
        models.parts.append(self)
        pass

    def Exec(self, time):
        dt = time - self.t_pre
        #print(self.t_pre)
        if(dt > self.time_div):
            vin  = models.getNodeValue(self.nd_in)
            vo = models.getNodeValue(self.nd_out)
            self.v_buff.append(vin)
            v_rm = 0
            if(len(self.v_buff) > self.buff_size):
                v_rm  = self.v_buff.pop(0)

            self.sum += vin - v_rm
            #print(self.sum)
            vo = self.sum / self.buff_size
            self.t_pre = time
            models.putNodeVal(self.nd_out, vo)
            

mul = multiplier(0, 1, 2)
avg = filter(2, 3, 0.0001, 50)
models.execAll(0.0001, 0.5)

plt.plot(models.simulation_time, models.recorded_nodes[0])
plt.plot(models.simulation_time, models.recorded_nodes[1])
plt.plot(models.simulation_time, models.recorded_nodes[2])
plt.plot(models.simulation_time, models.recorded_nodes[3])

plt.show()
