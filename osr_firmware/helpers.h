#define MAX_MSG_LEN 100

#include <string>
#include <vector>
#include <algorithm>
#include "pins.h"

using namespace std;

struct gcode_command_floats
{
  gcode_command_floats(vector<string> inputs);

  public:
  float fetch(char com_key);
  bool com_exists(char com_key);
  

  private:
  void parse_float(string inpt, char &cmd, float &value);

  vector<char> commands;
  vector<float> values;
};

/* SERIAL FUNCS */
void clear_data(char (&serial_data) [MAX_MSG_LEN]);
bool respondToSerial(char (&serial_data) [MAX_MSG_LEN]);

/* PARSING FUNCS */
void parse_inputs(char serial_data[MAX_MSG_LEN], vector<string> &args);
void parse_int(string inpt, char &cmd, int32_t &value);

/* GCode commands */
void execute_linear_move(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1);
void execute_pos_overwrite(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1);
void execute_motor_homing(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1);
void execute_motor_enable(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1);
void execute_motor_disable(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1);
void execute_motor_setaccel(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1);
void execute_motor_setrunpower(gcode_command_floats gcode, TMCstep &step_x, TMCstep &step_turntable, TMCstep &step_z0, TMCstep &step_z1);
void execute_motor_setholdpower(gcode_command_floats gcode, TMCstep &step_x, TMCstep &step_turntable, TMCstep &step_z0, TMCstep &step_z1);
