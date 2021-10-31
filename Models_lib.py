from matplotlib import pyplot as plt

import ctypes
from ctypes import c_char_p, c_double, c_void_p, cdll
import enum
import math


global_time_passed = 0
recorded_nodes = []
simulation_time = []

interface = cdll.LoadLibrary('/home/harsh/embedSim/build/libcontroller.so')
interface.createNodes.argtypes = [ctypes.c_int]
interface.createNodes.restype = ctypes.c_void_p
interface.updateNode.argtypes = [ctypes.c_int, ctypes.c_double]
interface.assignNodeNum.argtypes = [ctypes.c_int, ctypes.c_int]
interface.create_controller.argtypes = [ctypes.c_double, ctypes.c_double]
interface.Exec.argtypes = [ctypes.c_double]
interface.getDuty.restype = ctypes.c_double
interface.getNodeVal.argtypes = [ctypes.c_int]
interface.getNodeVal.restype = ctypes.c_double
interface.create_mppt_controller.argtypes = [ctypes.c_double]
interface.create_mppt_controller.restype = ctypes.c_void_p
interface.execMPPT.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_void_p]
interface.getVref.restype = ctypes.c_double
interface.getVref.argtypes = [ctypes.c_void_p]



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

        interface.assignNodeNum(vref , vout)

q_by_k = 11594
class PV_Source:
    nd_p = 0
    nd_n = 0
    nd_i = 0
    Isc = 0
    Voc = 0
    n = 1
    temp = 300
    def __init__(self, pos, neg, i, isc, voc, n):
        self.nd_p = pos
        self.nd_n = neg
        self.nd_i = i
        self.Isc = isc
        self.Voc = voc
        self.n = n
        parts.append(self)
    def Exec(self, time):
        vpv = getNodeValue(self.nd_p) - getNodeValue(self.nd_n)
        #print(vpv)
        ipv = self.Isc * (1 - math.exp(q_by_k * (vpv - self.Voc) / (self.n * self.temp)))
        #ipv = vpv * 0
        putNodeVal(self.nd_i, ipv)



class boost_converter :
    L = 0
    C1 = 0
    C2 = 0
    r = 1
    R = 100
    nd_out = 0
    nd_pwm = 0
    nd_vpv = 0
    nd_ipv = 0
    t_pre = 0
    iL = 0
    vo = 0
    def __init__(self, l, c1, c2, r, R, out, pwm, nd_v, nd_i):
        self.L = l
        self.C1 = c1
        self.C2 = c2
        self.r = self.r
        self.R = R
        self.nd_out = out
        self.nd_pwm = pwm
        self.nd_vpv = nd_v
        self.nd_ipv = nd_i
        parts.append(self)

    def Exec(self, time):
        dt = time - self.t_pre
        switch_state = getNodeValue(self.nd_pwm)
        vpv = getNodeValue(self.nd_vpv)
        ipv = getNodeValue(self.nd_ipv)
        #print("dt : ", dt, "vpv : ", vpv, "vo : ", self.vo, "nd_pv", self.nd_vpv, "iL_cache : ", self.iL, "ipv : ", ipv, "time : ", time)
        iL_cache = self.iL
        if(switch_state):
            self.iL += (dt / self.L) * (vpv - self.iL * self.r - self.vo)
            vpv += (dt / self.C1) * (ipv - iL_cache)
            self.vo += (dt / self.C2) * (iL_cache - self.vo / self.R)

        else:
            self.iL += (dt / self.L) * (vpv - self.iL * self.r)
            vpv += (dt / self.C1) * (ipv - iL_cache)
            self.vo += (dt / self.C2) * (- self.vo / self.R)
        putNodeVal(self.nd_out, self.vo)
        if(vpv < 0) :
            vpv = 0
        if(vpv > 50) :
            vpv = 50
        self.t_pre = time
        putNodeVal(self.nd_vpv, vpv)



class mppt_controller :
    mppt_obj = 0
    time_interval = 0
    t_pre = 0
    node_v = 0
    node_i = 0
    node_out = 0
    def __init__(self, vstep, interval, nd_v, nd_i, nd_out) :
        self.mppt_obj = interface.create_mppt_controller(vstep)
        self.time_interval = interval
        self.node_v = nd_v
        self.node_i = nd_i
        self.node_out = nd_out
        parts.append(self)
        
    def Exec(self, time):
        dt = time - self.t_pre
        vin = getNodeValue(self.node_v)
        iin = getNodeValue(self.node_i)
        if(dt  > self.time_interval):
            interface.execMPPT(time, vin, iin, self.mppt_obj)
            self.t_pre = time

        putNodeVal(self.node_out, interface.getVref(self.mppt_obj))




        