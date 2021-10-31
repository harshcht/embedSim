#include "mppt_controller.hpp"
#include <stdio.h>
mppt_controller :: mppt_controller(double _vstep){
    this->vstep = _vstep;
    this->v_ref = 37;
}


void
mppt_controller :: exec(double time, double v_in, double i_in){
    if(v_in * i_in < power){
        this->vstep = -this->vstep;
    }
    this->v_ref += this->vstep;
    printf("\npower : %f, new_power : %f, v_ref : %f, v_in : %f, i_in : %f", this->power, v_in * i_in, this->v_ref, v_in, i_in);
    power = v_in * i_in;
    
}

double
mppt_controller :: getVref(){
    return this->v_ref;
}