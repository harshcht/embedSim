#include "offgrid_inverter.hpp"

#define PI 3.14159265
#define BUFF_SIZE 2000
#define T_PHASE_CHANGE 0.1

sine_pwm_controller :: sine_pwm_controller(double f, double _st){
    this->freq = f;
    this->sample_time = _st;
    phase = PI;

};


void
sine_pwm_controller :: updateOutput(double time){
    this->duty_cycle = 0.5 + 0.5 * sin(2 * PI * this->freq * time + phase);
    //printf("\nduty : %f", this->duty_cycle);
    //this->duty_cycle = 0.5;
}

void
sine_pwm_controller :: updateDutyCycle(double Vin, double Vref, double time){
    static double t_pre = 0, ph_t_pre, vrms_pre, phase_shift = 0.025, pll_gain  = 0.005, ref_a = 40;
    static double dt = 0, ph_dt = 0;
    static double vref = 0, delayed_vref = 0;
    double errar_A;
    vref = ref_a * sin(2 * PI *time * this->freq + phase);
    //printf("\ntime : %f, t_pre : %f, dt : %f", time, t_pre, dt);
    dt = time - t_pre;
    if(dt > this->sample_time){
           this->duty_cycle += 4.1*dt * (vref - Vin);
        if(duty_cycle > 1) duty_cycle = 1;
        if(duty_cycle < 0) duty_cycle=0;
        t_pre = time;
        

        /*
        this->v_buff.push_back(Vref);
        if(time < this->delay){
            return;
        }
        else{
            delayed_vref = this->v_buff[0];
            this->v_buff.erase(this->v_buff.begin());
        }*/
        delayed_vref = Vref;
        updateAverage(&buff, pow(delayed_vref - Vin, 2), BUFF_SIZE, rms);
        updateAverage(&buff_in, pow(Vin,2), BUFF_SIZE, rms_in);
        updateAverage(&buff_ref, pow(delayed_vref, 2), BUFF_SIZE, rms_ref);
        if(buff.size() >= BUFF_SIZE){
            errar_A = rms_ref - rms_in;
            ref_a += 0.1 * errar_A * this->sample_time;
            //printf("\ntime : %f, ref_rms : %f, ref _in : %f, v_in : %f", time, rms_ref, rms_in, Vin);
            if(fabs(errar_A) < 20){
                ph_dt = time - ph_t_pre;
                if(ph_dt > BUFF_SIZE * this->sample_time){
                    
                    if(vrms_pre < rms){
                        pll_gain = -pll_gain;
                        phase_shift = -phase_shift;
                    }
                    phase += pll_gain * rms;
                    vrms_pre = rms;
                    ph_dt = 0;
                    ph_t_pre = time;
                    printf("\nrms : %f, time : %f, Vref - Vin: %f, phase : %f", rms, time, delayed_vref - Vin, phase);
                }
            } 
 
        }
        else{
            printf("\nsize : %ld", buff.size());
        }
        //printf("\ntime : %f, duty_cycle : %f, Vin : %f, Vref : %f", time, duty_cycle, Vin, Vref);
    }
    //duty_cycle = 0.7;
    //this->updateOutput(time);
}

bool
sine_pwm_controller :: updatePWM(double duty, double time){
    static double last_sim_time, time_frac = 0;
    static double period = 0.00001;
    static bool state_cache = 0, state = 0;
    time_frac = (time - last_sim_time)/period + time_frac;
    state_cache = state;
    if(time_frac >= duty){
        if(state == 1){            
            state = 0;
        }
    }
    if(time_frac >= 1){
        state = 1;
        time_frac = 0;
    }
    
    //printf("\ntime : %f, t_pre : %f, time_frac : %f, duty : %f, state : %d", time, last_sim_time, time_frac, duty, state);
    last_sim_time = time;
    //printf("\nstate : %d", state);
    return state;
}


void
sine_pwm_controller :: updateDutyCycleGridTied(double Vin, double Vref, double time){
    static double dt, t_pre;
    dt = time - t_pre;
    if(dt >= this->sample_time){
        this->duty_cycle += 4.1 * this->sample_time * (Vref - Vin);
        if(duty_cycle > 1) duty_cycle = 1;
        if(duty_cycle < 0) duty_cycle=0;
        t_pre = time;
    }

}

double
sine_pwm_controller :: getDutyCycle(){
    return this->duty_cycle;
}

void updateAverage(vector<double> * buffer, double Vin, double num, double & avg){
    //double first = 0;
    double sum = buffer->size() * avg;
    //if(buffer->size() != 0)
    //printf(" Vin : %f, size : %ld, first : %f", Vin, buffer->size(), (*buffer)[0]);
    if(buffer->size() < num){
        buffer->push_back(Vin);
        sum = sum + Vin ;
    }
    else{
        buffer->push_back(Vin);
        sum = sum + (Vin - (*buffer)[0]);
        buffer->erase(buffer->begin());
    }
    avg = sum / buffer->size();
}