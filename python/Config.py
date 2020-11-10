""" MECHANICAL PARAMETERS """
x_step_per_mm = 320
y_step_per_mm = 27106  # Actually rads but units psh whatever
z_step_per_mm = 320

x_default_vel_radps = 400
x_default_accel_radps2 = 5000
y_default_vel_radps = 3
y_default_accel_radps2 = 2
z_default_vel_radps = 300
z_default_accel_radps2 = 3000


""" OPERATION PARAMETERS """
saveimg_path = '/home/pi/imgs'


""" CAMERA PARAMETERS """
video_resolution = (1920, 1080)


""" MOTION DETECT PARAMETERS """
check_video_fps = 3
motion_start_min_percent = 5
motion_stop_max_percent = 1
motion_stop_time = 1          # Consecutive frames must change by less than motion_stop_max_percent for this much time


""" OBJECT DETECT PARAMETERS """
turntable_center = (990, 565)  # Center of rotation of turntable, (0,0) for the math
pixel_threshold = 40
pix_per_mm = 6.41
knife_zero_offset_mm = 80  # Distance from knife home to center of turntable


""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_FRAMES = True
