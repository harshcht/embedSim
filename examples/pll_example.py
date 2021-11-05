import math

import sys
sys.path.insert(0, '../')

import Models_lib as models
from matplotlib import pyplot as plt



class multiplier :
    nd1 = 0
    nd2 = 0
    nd_out = 0
    gain = 1
    def __init__(self, nd1, nd2, nd_out, gain) :
        self.nd1 = nd1
        self.nd2 = nd2
        self.nd_out = nd_out
        self.gain = gain
        models.parts.append(self)
    def Exec(self, time):
        v1 = models.getNodeValue(self.nd1)
        v2 = models.getNodeValue(self.nd2)
        vout = v1 * v2
        models.putNodeVal(self.nd_out, self.gain*vout)


class filter :
    nd_in = 0
    nd_out = 0
    buff_size = 0
    time_div = 0
    t_pre = 0
    v_buff = []
    sum =0 
    gain = 1
    def __init__(self, nd_in, nd_out, time_div, n_samples, gain):
        self.nd_in = nd_in
        self.nd_out = nd_out
        self.time_div = time_div
        self.buff_size = n_samples
        self.gain = gain
        self.v_buff = []
        models.parts.append(self)

    def Exec(self, time):
        dt = time - self.t_pre
        #print("t_pre : ", self.t_pre, "dt : ", dt)
        if(dt > self.time_div):
            vin  = models.getNodeValue(self.nd_in)
            vo = models.getNodeValue(self.nd_out)/self.gain
            self.v_buff.append(vin)
            v_rm = 0
            if(len(self.v_buff) > self.buff_size):
                v_rm  = self.v_buff.pop(0)

                self.sum += vin - v_rm
            #print("out node : ", self.nd_out, "in_node : ", self.nd_in, "vin : ", vin, "vout : ", vo, "gain : ", self.gain, "V-rmb : ", v_rm, "buffer_size : " , self.buff_size , "time : ", time, "buffer_size : ", len(self.v_buff))
            vo = self.sum / self.buff_size
            self.t_pre = time
            models.putNodeVal(self.nd_out, self.gain * vo)
            
nodes = models.createNodes(10)
#src1 = models.sine_source(50, 0, 1, 0, 0)
#src2 = models.sine_source(55, 1, 1, 0, 0)
#mul = multiplier(0, 1, 2)
#avg = filter(2, 3, 0.0001, 600)
#avg2 = filter(0, 4, 0.0001, 500)

#src1.assignFreqNode(3)
#models.putNodeVal(1, 50)

clk = models.Clock(0.0001, 2, 0, 50, -50)
converter= models.rLC(0.001, 0.00005, 1, 0, 1)
ctrl = models.controller(2, 0.0001, 2)
ctrl.assignNodes(3, 1)
src1 = models.sine_source(50, 3, 50, 0, 0)
#test_src = models.sine_source(10, 1, 1, 0, 0)
#test_src = models.sine_source(10, 8, 1, 0, 0)
avg = filter(1,4, 0.0001, 4000, 100)
mul = multiplier(3, 1, 5, 1)
phase_flter = filter(5, 6, 0.0001, 10, 1)
models.execAll(0.000001, 10)
#out = [100 * i for i in models.recorded_nodes[4]]
#pllout = [100 * j for j in models.recorded_nodes[5]]
#plt.plot(models.simulation_time, models.recorded_nodes[0])
#plt.plot(models.simulation_time, models.recorded_nodes[1])
#plt.plot(models.simulation_time, models.recorded_nodes[2])
plt.plot(models.simulation_time[1:], models.recorded_nodes[3][1:])
plt.plot(models.simulation_time[1:], models.recorded_nodes[1][1:])
#plt.plot(models.simulation_time, models.recorded_nodes[4])
plt.plot(models.simulation_time[1:], models.recorded_nodes[5][1:])
#plt.plot(models.simulation_time, out)
#plt.plot(models.simulation_time, pllout)
plt.plot(models.simulation_time[1:], models.recorded_nodes[6][1:])
#plt.plot(models.simulation_time, models.recorded_nodes[8])
#plt.plot(models.simulation_time, models.recorded_nodes[9])
plt.show()
