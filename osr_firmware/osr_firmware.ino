#include <OSR.h>
#include "helpers.h"

void setup() {
  // put your setup code here, to run once:
  Serial.begin(250000);
  while (!Serial) { delay(1); }
}

void loop() {
  // Initialize motors
  TMC2041 Driver0(D0EN, D0CS);
  TMC2041 Driver1(D1EN, D1CS);
  TMCstep motdrive0 = TMCstep(D0S0S, D0S0D, Driver0, 0); // turntable
  TMCstep motdrive1 = TMCstep(D0S1S, D0S1D, Driver0, 1); // z motor 1
  TMCstep motdrive2 = TMCstep(D1S1S, D1S1D, Driver1, 1); // z motor 2
  TMCstep motdrive3 = TMCstep(D1S0S, D1S0D, Driver1, 0); // x motor
  motorDrive step_turntable = motorDrive(motdrive0, 320);
  motorDrive step_z0 = motorDrive(motdrive1, 320);
  motorDrive step_z1 = motorDrive(motdrive2, 320);
  motorDrive step_x = motorDrive(motdrive3, 320);

  unsigned long startTime_us = micros();
  unsigned long t_elapsed_us;
  char serial_data[MAX_MSG_LEN];

  // Set x motor current
  motdrive3.set_run_current(20);
  motdrive3.set_hold_current(6);

  // Set turntable motor current
  motdrive0.set_run_current(15);
  motdrive0.set_hold_current(6);

  // Set turntable motor currents
  motdrive1.set_run_current(20);
  motdrive1.set_hold_current(6);
  motdrive2.set_run_current(20);
  motdrive2.set_hold_current(6);

  // Init vars
  char base_cmd, char_value;
  int32_t base_value, int_value;
  float float_value;

  // Start main response loop
  while (true)
  {
    t_elapsed_us = micros() - startTime_us;
    clear_data(serial_data);
    if (respondToSerial(serial_data)) 
    {
      // Parse input into data chunks
      std::vector<std::string> args;
      parse_inputs(serial_data, args);
      parse_int(args[0], base_cmd, base_value);

      switch (tolower(base_cmd)) 
      {
        case 'g': {
          switch (base_value) 
          {
            case 0:
            case 1: {
              // LINEAR MOVE DO NOT WAIT
              gcode_command_floats gcode(args);
              execute_linear_move(gcode, step_x, step_turntable, step_z0, step_z1);
              break;
            }
            case 28: {
              gcode_command_floats gcode(args);
              execute_motor_homing(gcode, step_x, step_turntable, step_z0, step_z1);
              break;
            }
            case 92: {
              // Overwrite current pos
              gcode_command_floats gcode(args);
              execute_pos_overwrite(gcode, step_x, step_turntable, step_z0, step_z1);
              break;
            }
          }
          break;
        }
      case 'm': {
          switch (base_value) 
          {
            case 17: {
              // Enable Steppers
              gcode_command_floats gcode(args);
              execute_motor_enable(gcode, step_x, step_turntable, step_z0, step_z1);
              break;
            }
            case 84: {
              // Disable Steppers
              gcode_command_floats gcode(args);
              execute_motor_disable(gcode, step_x, step_turntable, step_z0, step_z1);
              break;
            }
            case 114: {
              // Get current position
              float xpos = step_x.get_current_pos_mm();
              float ypos = step_turntable.get_current_pos_mm();
              float zpos = step_z0.get_current_pos_mm();
              Serial.print(xpos, 4);
              Serial.print(",");
              Serial.print(ypos, 4);
              Serial.print(",");
              Serial.print(zpos, 4);
              Serial.print("\n");
              break;
            }
            case 201: {
              // Set acceleration
              gcode_command_floats gcode(args);
              execute_motor_setaccel(gcode, step_x, step_turntable, step_z0, step_z1);
              break;
            }
            case 906: {
              // Set motor run current, values 0 to 31 acceptable
              gcode_command_floats gcode(args);
              execute_motor_setrunpower(gcode, motdrive3, motdrive0, motdrive1, motdrive2);
              break;
            }
            case 907: {
              // Set motor hold current, values 0 to 31 acceptable
              gcode_command_floats gcode(args);
              execute_motor_setholdpower(gcode, motdrive3, motdrive0, motdrive1, motdrive2);
              break;
            }
          }
          break;
        }
      case 'c': {
          switch (base_value) 
          {
            case 0: {
              // configure hardware stuff
              break;
            }
            case 1: {
              // set trigger angle
              break;
            }
            case 2: {
              // Get current velocities
              float xvel = step_x.get_current_vel_mmps();
              float yvel = step_turntable.get_current_vel_mmps();
              float zvel = step_z0.get_current_vel_mmps();
              Serial.print(xvel, 4);
              Serial.print(",");
              Serial.print(yvel, 4);
              Serial.print(",");
              Serial.print(zvel, 4);
              Serial.print("\n");
              break;
            }
          }
          break;
        }
        break;
      }
      Serial.println("ok");
    }
  }
}
