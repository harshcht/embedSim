import sys
sys.path.insert(0, '../')

import Models_lib as models
from matplotlib import pyplot as plt

nodes = models.createNodes(7)
pv = models.PV_Source(1,0,2,8,40, 100)
pwm_src = models.Clock(0.0001, 4, 3, 1, 0)
boost = models.boost_converter(0.001, 0.00005, 0.00005, 1, 100, 5, 3, 1, 2)
ctrl = models.controller(1, 0.0001, 4)
ctrl.assignNodes(6, 1)
mppt = models.mppt_controller(-1, 0.2, 1,2,6)
models.putNodeVal(0,0)
models.putNodeVal(6, 40)

models.execAll(0.0000001, 5)
plt.plot(models.simulation_time, models.recorded_nodes[1])
#plt.plot(models.simulation_time, models.recorded_nodes[3])
plt.plot(models.simulation_time, models.recorded_nodes[5])
plt.show()