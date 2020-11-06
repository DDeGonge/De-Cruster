""" MECHANICAL PARAMETERS """
x_step_per_mm = 27106
y_step_per_mm = 27106  # Actually rads but units psh whatever
z_step_per_mm = 27106

x_default_vel_radps = 400
x_default_accel_radps2 = 5000
y_default_vel_radps = 3
y_default_accel_radps2 = 200
z_default_vel_radps = 300
z_default_accel_radps2 = 3000


""" OPERATION PARAMETERS """
saveimg_path = '/home/pi/imgs'


""" CAMERA PARAMETERS """
video_resolution = (640,480)


""" MOTION DETECT PARAMETERS """
check_video_fps = 10
motion_start_min_percent = 0.10
motion_stop_max_percent = 0.01
motion_stop_time = 0.5          # Consecutive frames must change by less than motion_stop_max_percent for this much time


""" FEATHER COMM PARAMETERS """
# Chars used for setting parameters on feather. All vars here must be int
Feather_Parameter_Chars = {
    'a': s0_step_per_rev,
    'b': s1_step_per_rev,
    'c': default_vel_radps,
    'd': default_accel_radps2
}


""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_FRAMES = True
