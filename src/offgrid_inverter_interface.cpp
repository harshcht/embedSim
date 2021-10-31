#include "offgrid_inverter.hpp"

extern "C"
{
    sine_pwm_controller * createController(double freq, double sample_time){
        return new sine_pwm_controller(freq, sample_time);
    }

    bool updatePWM(double time, sine_pwm_controller * pwm){
        return pwm->updatePWM(pwm->getDutyCycle(), time);
    }

    void updateDuty(double Vin, double Vref, sine_pwm_controller * pwm, double time){
        pwm->updateDutyCycle(Vin, Vref, time);
    }
    void updateGridTiedDuty(double vin, double Vref, sine_pwm_controller * pwm, double time_div){
        pwm->updateDutyCycleGridTied(vin, Vref, time_div);
    }

    void updateOutput(double time, sine_pwm_controller * controller){
        controller->updateOutput(time);
    }
}