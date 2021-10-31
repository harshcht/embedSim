#include <stdio.h>
#include "controller.hpp"

void
updateDuty(double Vref, double Vmeasure){
    duty += gain * (Vref - Vmeasure) * sampling_time;
    if(duty > 1) duty = 1;
    if(duty < 0) duty = 0;

}