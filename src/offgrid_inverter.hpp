#include <stdio.h>
#include <vector>
#include <math.h>
using namespace std;


class sine_pwm_controller {
    private :
        double freq, amplitude, phase, duty_cycle;
        double gain, sample_time, rms, rms_ref, rms_in, delay = 0.005;
        vector<double> buff = {}, buff_ref = {}, buff_in = {}, v_buff = {};
    public :
        sine_pwm_controller(double freq, double sample_time);
        void updateOutput(double time);
        void updateDutyCycle(double Vin, double Vref, double time);
        void updateDutyCycleGridTied(double vin, double Vref, double time_div);
        double getDutyCycle();
        bool updatePWM(double duty, double time);
};

void updateAverage(vector<double> * buffer, double Vin, double num, double & avg);