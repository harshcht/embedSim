
#pragma once

#ifndef CONTROLLER_H_
#define CONTROLLER_H_
#include <math.h>

extern double duty;
extern double gain;
extern double sampling_time;

void updateDuty(double Vref, double Vmeasure);
#endif