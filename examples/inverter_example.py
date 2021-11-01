import sys
sys.path.insert(0, '../')

import Models_lib as models
from matplotlib import pyplot as plt
nodes = models.createNodes(4)
clk = models.Clock(0.0001, 2, 0, 50, -50)

#rLC filter of the converter
#syntax : rLC(l, c, r, in_node, out_node)
#   l : inductance
#   c : capacitance
#   r : switch resistance
#   in_node : input node number
#   out_node : output node number
converter= models.rLC(0.001, 0.00005, 1, 0, 1)

controller = models.inverter_controller(0.00001, 1, -1, 3, 2)

ref = models.sine_source(50, 3, 40, 0)

models.execAll(0.000001, 10)


plt.plot(models.simulation_time, models.recorded_nodes[1])
plt.plot(models.simulation_time, models.recorded_nodes[3])
error = [models.recorded_nodes[3][i] - models.recorded_nodes[1][i] for i in range(len(models.simulation_time))]
plt.plot(models.simulation_time, error)
plt.show()