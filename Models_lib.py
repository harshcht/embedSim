from matplotlib import pyplot as plt

import ctypes
from ctypes import c_char_p, c_double, c_void_p, cdll
import enum
import math


global_time_passed = 0
recorded_nodes = []
simulation_time = []

interface = cdll.LoadLibrary('build/libcontroller.so')
interface.createNodes.argtypes = [ctypes.c_int]
interface.createNodes.restype = ctypes.c_void_p
interface.updateNode.argtypes = [ctypes.c_int, ctypes.c_double]
interface.assignNodeNum.argtypes = [ctypes.c_int, ctypes.c_int]
interface.create_controller.argtypes = [ctypes.c_double, ctypes.c_double]
interface.Exec.argtypes = [ctypes.c_double]
interface.getDuty.restype = ctypes.c_double
interface.getNodeVal.argtypes = [ctypes.c_int]
interface.getNodeVal.restype = ctypes.c_double



parts = []

def getNodeValue(num):
    return interface.getNodeVal(num)

def putNodeVal(num, val):
    interface.updateNode(num, val)

def createNodes(num):
    global recorded_nodes
    recorded_nodes.extend([] for i in range(num))
    return interface.createNodes(num)


def recordNodes() :
    global recorded_nodes
    records = []
    #with open(record,'w') as csvfile :
     #   csvwriter = csv.writer(csvfile) 
      #  for i in range(len(recorded_nodes)) :
       #     records.append(getNodeValue(i))
        
        #csvwriter.writerow(records)
    for i in range(len(recorded_nodes)):
        
        recorded_nodes[i].append(getNodeValue(i))
        #if recorded_nodes
    return


def execAll(time_div, time) :
    #print(len(parts))
    global global_time_passed
    global simulation_time
    t = global_time_passed
    num_record = 0
    while(t < time + global_time_passed) : 
        if(num_record % time == 0):
            recordNodes()
            simulation_time.append(t)
        for p in parts : 
            p.Exec(t)
            #print(mt.getSpeed())
        t  = t + time_div
        num_record += 1
    
    global_time_passed = time + global_time_passed

class Clock :
    state = False
    t_pre = 0
    period = 0
    duty = 0
    time_frac = 0
    node = 0
    v_on = 0
    v_off = 0
    def __init__(self, period, duty, node_num, v_on, v_off):
        self.period = period
        self.duty = duty
        self.node  = node_num
        self.v_on = v_on
        self.v_off = v_off
        parts.append(self)
    def Exec(self, time):
        self.time_frac += (time - self.t_pre)/self.period
        duty = getNodeValue(self.duty)
        if(self.time_frac >= duty) :
            if(self.state) :
                self.state = False

        if(self.time_frac > 1) :
            self.state = True
            self.time_frac = 0
        self.t_pre = time
        if(self.state):
            putNodeVal(self.node, self.v_on)
        else:
            putNodeVal(self.node, self.v_off)


class rLC : 
    L = 0
    C = 0
    r = 0
    Vin = 0
    Vo = 0
    i=0
    t_pre = 0
    duty = 0
    v_on = 0
    v_off = 0
    pwm_src = 0
    node_in = 0
    node_out = 0
    def __init__(self,l,c,r, in_node, out_node):
        self.L = l
        self.C = c
        self.r = r
        self.node_in = in_node
        self.node_out = out_node
        parts.append(self)

    def Exec(self, time) :
        self.Vin = getNodeValue(self.node_in)
        dt = time - self.t_pre
        i_cache = self.i
        self.i = self.i + (self.Vin - self.Vo - self.r * self.i) * dt / self.L 
        self.Vo = self.Vo + i_cache * dt / self.C
        #print("output :", self.Vo, " Vin :", self.Vin)
        self.t_pre = time
        putNodeVal(self.node_out, self.Vo)

#device  = rLC(0.001, 0.0005, 1, 10, 0)


class controller :
    gain = 0
    sampling_time = 0
    t_pre = 0
    vref_node = 0
    vout_node = 0
    duty_node = 0
    def __init__(self, gain, _sampling_time, duty_node):
        interface.create_controller(gain, _sampling_time)
        self.gain = gain
        self.sampling_time = _sampling_time
        parts.append(self)
        self.duty_node = duty_node
        
    def Exec(self, time):
        if(time - self.t_pre > self.sampling_time):
            interface.Exec(time)
            self.t_pre = time

        putNodeVal(self.duty_node, interface.getDuty())

    def assignNodes(self, vref, vout):
        print("assign out :", vout)
        interface.assignNodeNum(vref , vout)

#create ndoes 
#for this example we need 3 nodes
#the nodes are identified by integers from 0 to num-1
#syntax : createNodes(num)
#   num = number of nodes needed

nodes = createNodes(4)

#create pwm source
#syntax Clock(time_period, duty_node, output_node, von, voff)
#   time_period : time period of the pulse
#   duty_node : node which defines the duty cycle
#   output_node : node which defines the output
#   von : output when the state of the clock is high
#   voff : output when the state of the clock is low
clk = Clock(0.0001, 2, 0, 10, 0)

#rLC filter of the converter
#syntax : rLC(l, c, r, in_node, out_node)
#   l : inductance
#   c : capacitance
#   r : switch resistance
#   in_node : input node number
#   out_node : output node number
converter= rLC(0.001, 0.00005, 1, 0, 1)


ctrl = controller(1, 0.0001, 2)
ctrl.assignNodes(3, 1)
#put value on a given node defined by it's node number
#syntax : putNodeVal(node_num, val)
#   node_num : number of the node
#   val : float value to be assigned
putNodeVal(3, 4)

#execute the simulation
#this will automatically execute all the aprts 
#in this example we have 2 parts, rLC and clock
#syntax : execAll(time_div, duration)
#   time_div : time division for simulation
#   duration : duration for which the simulation is supposed to last
execAll(0.0000001, 2)

plt.plot(simulation_time, recorded_nodes[0])
plt.plot(simulation_time, recorded_nodes[1])
plt.ylabel("voltage (V)")
plt.xlabel("time (s)")
plt.show()
