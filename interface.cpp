#include "src/controller.hpp"
#include <stdio.h>
double sampling_time = 0;
double * nodes;
int node_num = 0, vref, vout;
double duty = 0;
double gain = 1;
extern "C" 
{
    double * createNodes(int n){
        nodes = (double *)malloc(n * sizeof(double));
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
        printf("\nout : %d", _vout);
    }
    void  create_controller(double _gain, double _sampling_time){
        gain = _gain;
        sampling_time = _sampling_time;
    }
    void Exec(double time){
        printf("\ntime : %f, refnum : %d, outnum : %d", time, vref, vout);
        updateDuty(nodes[vref], nodes[vout]);
    }
    double getDuty(){
        return duty;
    }
}
