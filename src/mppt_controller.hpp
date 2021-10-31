class mppt_controller
{
private:
    /* data */
    double vstep = 0.005;
    double power = 0;
    double v_ref;
public:
    mppt_controller(double _vstep);
    void exec(double time, double v_in, double i_in);
    double getVref();
};
