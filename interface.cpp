#include "src/controller.hpp"
#include "src/mppt_controller.hpp"
#include <stdio.h>
double sampling_time = 0;
double * nodes;
int node_num = 0, vref, vout;
double duty = 0;
double gain = 1;
extern "C" 
{
    double * createNodes(int n){
        nodes = (double *)calloc(n , sizeof(double));
        node_num = n;
        return nodes;
    }
    void updateNode(int num, double value){
        *(nodes + num) = value;
    }
    double getNodeVal(int num){
        return *(nodes + num);
    }
    void assignNodeNum(int _vref, int _vout){
        vref = _vref;
        vout = _vout;
    }
    void  create_controller(double _gain, double _sampling_time){
        gain = _gain;
        sampling_time = _sampling_time;
    }
    void Exec(double time){
        updateDuty(nodes[vref], nodes[vout]);
    }
    double getDuty(){
        return duty;
    }
    mppt_controller * create_mppt_controller(double vstep){
        return new mppt_controller(vstep);
    }
    void execMPPT(double time, double vin, double iin, mppt_controller * _this){
        _this->exec(time, vin, iin);
    }
    double getVref(mppt_controller * _this){
        return _this->getVref();
    }
}
