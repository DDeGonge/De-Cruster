/* GCODE PARSER STUFF */

gcode_command_floats::gcode_command_floats(vector<string> inputs)
{
  if (inputs.size() == 1)
    return;

  for(uint16_t arg_i = 1; arg_i < inputs.size(); arg_i++)
  {
    char char_value = '\0';
    float float_value = NOVALUE;
    parse_float(inputs[arg_i], char_value, float_value);

    commands.push_back(tolower(char_value));
    values.push_back(float_value);
  }
}

float gcode_command_floats::fetch(char com_key)
{
  vector<char>::iterator itr = find(commands.begin(), commands.end(), com_key);
  if (itr != commands.cend())
  {
    return values[distance(commands.begin(), itr)];
  }

  return NOVALUE;
}

bool gcode_command_floats::com_exists(char com_key)
{
  vector<char>::iterator itr = find(commands.begin(), commands.end(), com_key);
  if (itr != commands.cend())
  {
    return true;
  }

  return false;
}

void gcode_command_floats::parse_float(string inpt, char &cmd, float &value)
{
  if (inpt.length() > 0)
  {
    cmd = inpt[0];
    if (inpt.length() == 1)
      return;

    string temp_arg_char = "";
    for (uint32_t i = 1; i < inpt.length(); i++)
    {
      temp_arg_char += inpt[i];
    }
  
    value = stof(temp_arg_char);
  }
}

/* Gcode reply stuff */

void execute_linear_move(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.plan_move(gcode.fetch('x'), gcode.fetch('f'));
  if(gcode.com_exists('y'))
    step_turntable.plan_move(gcode.fetch('y'), gcode.fetch('f'));
  if(gcode.com_exists('z'))
  {
    step_z0.plan_move(gcode.fetch('z'), gcode.fetch('f'));
    step_z1.plan_move(gcode.fetch('z'), gcode.fetch('f'));
  }

  step_x.execute_move_async();
  step_turntable.execute_move_async();
  step_z0.execute_move_async();
  step_z1.execute_move_async();

  // Loop until all are done stepping
  while(true)
  {
    uint32_t tnow = micros();
    bool r0 = step_x.async_move_step_check(tnow);
    bool r1 = step_turntable.async_move_step_check(tnow);
    bool r2 = step_z0.async_move_step_check(tnow);
    bool r3 = step_z1.async_move_step_check(tnow);
    if(r0 && r1 && r2 && r3)
      break;
  }
}

void execute_pos_overwrite(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.set_current_pos_mm(gcode.fetch('x'));
  if(gcode.com_exists('y'))
    step_turntable.set_current_pos_mm(gcode.fetch('y'));
  if(gcode.com_exists('z'))
  {
    step_z0.set_current_pos_mm(gcode.fetch('z'));
    step_z1.set_current_pos_mm(gcode.fetch('z'));
  }
  if(!gcode.com_exists('x') && !gcode.com_exists('y') && !gcode.com_exists('z'))
  {
    step_x.set_current_pos_mm(gcode.fetch('x'));
    step_turntable.set_current_pos_mm(gcode.fetch('y'));
    step_z0.set_current_pos_mm(gcode.fetch('z'));
    step_z1.set_current_pos_mm(gcode.fetch('z'));
  }
}

void execute_motor_homing(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.home();
  if(gcode.com_exists('y'))
    step_turntable.home();
  if(gcode.com_exists('z'))
    home_z_axis(step_z0, step_z1);
  if(!gcode.com_exists('x') && !gcode.com_exists('y') && !gcode.com_exists('z'))
  {
    step_x.home();
    step_turntable.home();
    home_z_axis(step_z0, step_z1);
  }
}

void home_z_axis(motorDrive &step_z0, motorDrive &step_z1)
{
  // This little ball of fun is because I didn't create a dual stepper object. So behold, a janky custom homing routine for Z

  // First home
  step_z0.plan_move(-300, 1800, true);
  step_z1.plan_move(-300, 1800, true);
  step_z0.execute_move_async();
  step_z1.execute_move_async();
  while(true)
  {
    uint32_t tnow = micros();
    bool r2 = step_z0.async_move_step_check(tnow, true);
    bool r3 = step_z1.async_move_step_check(tnow, true);
    if(r2 && r3)
      break;
  }
  step_z0.zero();
  step_z1.zero();

  // Bounce a lil
  step_z0.plan_move(5, 6000);
  step_z1.plan_move(5, 6000);
  step_z0.execute_move_async();
  step_z1.execute_move_async();
  while(true)
  {
    uint32_t tnow = micros();
    bool r2 = step_z0.async_move_step_check(tnow);
    bool r3 = step_z1.async_move_step_check(tnow);
    if(r2 && r3)
      break;
  }

  // Final home
  step_z0.plan_move(-10, 1800, true);
  step_z1.plan_move(-10, 1800, true);
  step_z0.execute_move_async();
  step_z1.execute_move_async();
  while(true)
  {
    uint32_t tnow = micros();
    bool r2 = step_z0.async_move_step_check(tnow, true);
    bool r3 = step_z1.async_move_step_check(tnow, true);
    if(r2 && r3)
      break;
  }
  step_z0.zero();
  step_z1.zero();
}

void execute_motor_enable(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.enable();
  if(gcode.com_exists('y'))
    step_turntable.enable();
  if(gcode.com_exists('z'))
  {
    step_z0.enable();
    step_z1.enable();
  }
  if(!gcode.com_exists('x') && !gcode.com_exists('y') && !gcode.com_exists('z'))
  {
    step_x.enable();
    step_turntable.enable();
    step_z0.enable();
    step_z1.enable();
  }
}

void execute_motor_disable(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.disable();
  if(gcode.com_exists('y'))
    step_turntable.disable();
  if(gcode.com_exists('z'))
  {
    step_z0.disable();
    step_z1.disable();
  }
  if(!gcode.com_exists('x') && !gcode.com_exists('y') && !gcode.com_exists('z'))
  {
    step_x.disable();
    step_turntable.disable();
    step_z0.disable();
    step_z1.disable();
  }
}

void execute_motor_setaccel(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.set_default_acc_mmps2(gcode.fetch('x'));
  if(gcode.com_exists('y'))
    step_turntable.set_default_acc_mmps2(gcode.fetch('y'));
  if(gcode.com_exists('z'))
  {
    step_z0.set_default_acc_mmps2(gcode.fetch('z'));
    step_z1.set_default_acc_mmps2(gcode.fetch('z'));
  }
}

void execute_motor_setvels(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.set_default_vel_mmps(gcode.fetch('x'));
  if(gcode.com_exists('y'))
    step_turntable.set_default_vel_mmps(gcode.fetch('y'));
  if(gcode.com_exists('z'))
  {
    step_z0.set_default_vel_mmps(gcode.fetch('z'));
    step_z1.set_default_vel_mmps(gcode.fetch('z'));
  }
}

void execute_motor_stepspermm(gcode_command_floats gcode, motorDrive &step_x, motorDrive &step_turntable, motorDrive &step_z0, motorDrive &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.set_steps_per_mm(gcode.fetch('x'));
  if(gcode.com_exists('y'))
    step_turntable.set_steps_per_mm(gcode.fetch('y'));
  if(gcode.com_exists('z'))
  {
    step_z0.set_steps_per_mm(gcode.fetch('z'));
    step_z1.set_steps_per_mm(gcode.fetch('z'));
  }
}

void execute_motor_setrunpower(gcode_command_floats gcode, TMCstep &step_x, TMCstep &step_turntable, TMCstep &step_z0, TMCstep &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.set_run_current((int)gcode.fetch('x'));
  if(gcode.com_exists('y'))
    step_turntable.set_run_current((int)gcode.fetch('y'));
  if(gcode.com_exists('z'))
  {
    step_z0.set_run_current((int)gcode.fetch('z'));
    step_z1.set_run_current((int)gcode.fetch('z'));
  }
}

void execute_motor_setholdpower(gcode_command_floats gcode, TMCstep &step_x, TMCstep &step_turntable, TMCstep &step_z0, TMCstep &step_z1)
{
  if(gcode.com_exists('x'))
    step_x.set_hold_current((int)gcode.fetch('x'));
  if(gcode.com_exists('y'))
    step_turntable.set_hold_current((int)gcode.fetch('y'));
  if(gcode.com_exists('z'))
  {
    step_z0.set_hold_current((int)gcode.fetch('z'));
    step_z1.set_hold_current((int)gcode.fetch('z'));
  }
}


/* Normie functions */

// Read serial messages if exist
bool respondToSerial(char (&serial_data) [MAX_MSG_LEN])
{
  uint8_t index = 0;
  if (Serial.available() > 0) {
    while (Serial.available() > 0) {
      char newchar = Serial.read();
      if ((newchar != '\n') and (index < MAX_MSG_LEN)) {
        serial_data[index] = newchar;
        index++;
      }
      else {
        break;
      }
    }
    return true;
  }
  return false;
}

void clear_data(char (&serial_data) [MAX_MSG_LEN])
{
  for (uint16_t i = 0; i < MAX_MSG_LEN; i++) {
    serial_data[i] = '\0';
  }
}

void parse_inputs(char serial_data[MAX_MSG_LEN], vector<string> &args)
{
  char delim = ' ';
  uint32_t index = 0;
  string temp_arg_str = "";

  while (serial_data[index] != '\0') {
    temp_arg_str += serial_data[index];
    index++;
    if (serial_data[index] == delim) {
      args.push_back(temp_arg_str);
      temp_arg_str = "";
      index++;
    }

    // timeout
    if (index > MAX_MSG_LEN) return;
  }
  args.push_back(temp_arg_str);
}

void parse_int(string inpt, char &cmd, int32_t &value)
{
  cmd = '\0';
  value = NOVALUE;
  cmd = inpt[0];
  string temp_arg_char = "";
  for (uint32_t i = 1; i < inpt.length(); i++)
  {
    temp_arg_char += inpt[i];
  }

  value = stoi(temp_arg_char);
}
