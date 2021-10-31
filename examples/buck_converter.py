import sys
sys.path.insert(0, '../')

import Models_lib as models
from matplotlib import pyplot as plt

#create ndoes 
#for this example we need 3 nodes
#the nodes are identified by integers from 0 to num-1
#syntax : createNodes(num)
#   num = number of nodes needed

nodes = models.createNodes(4)

#create pwm source
#syntax Clock(time_period, duty_node, output_node, von, voff)
#   time_period : time period of the pulse
#   duty_node : node which defines the duty cycle
#   output_node : node which defines the output
#   von : output when the state of the clock is high
#   voff : output when the state of the clock is low
clk = models.Clock(0.0001, 2, 0, 10, 0)

#rLC filter of the converter
#syntax : rLC(l, c, r, in_node, out_node)
#   l : inductance
#   c : capacitance
#   r : switch resistance
#   in_node : input node number
#   out_node : output node number
converter= models.rLC(0.001, 0.00005, 1, 0, 1)


ctrl = models.controller(1, 0.0001, 2)
ctrl.assignNodes(3, 1)
#put value on a given node defined by it's node number
#syntax : putNodeVal(node_num, val)
#   node_num : number of the node
#   val : float value to be assigned
models.putNodeVal(3, 4)

#execute the simulation
#this will automatically execute all the aprts 
#in this example we have 2 parts, rLC and clock
#syntax : execAll(time_div, duration)
#   time_div : time division for simulation
#   duration : duration for which the simulation is supposed to last
models.execAll(0.0000001, 2)

plt.plot(models.simulation_time, models.recorded_nodes[0])
plt.plot(models.simulation_time, models.recorded_nodes[1])
plt.ylabel("voltage (V)")
plt.xlabel("time (s)")
plt.show()