""" MECHANICAL PARAMETERS """
x_step_per_mm = 320
y_step_per_mm = 28500  # Actually rads but units psh whatever
z_step_per_mm = 320

x_default_vel_radps = 400
x_default_accel_radps2 = 10000
y_default_vel_radps = 3
y_default_accel_radps2 = 5
z_default_vel_radps = 300
z_default_accel_radps2 = 4000

z_table_offset_mm = 115
z_clear_food_mm = 30
knife_zero_offset_mm = 70


""" OPERATION PARAMETERS """
saveimg_path = '/home/pi/imgs'
reddit_path = 'reddit.png'


""" CAMERA PARAMETERS """
video_resolution = (1920, 1080)


""" MOTION DETECT PARAMETERS """
check_video_fps = 3
motion_start_min_percent = 4
motion_stop_max_percent = 1
motion_stop_time = 1          # Consecutive frames must change by less than motion_stop_max_percent for this much time


""" OBJECT DETECT PARAMETERS """
turntable_center = (594, 620)  # Center of rotation of turntable after crop, (0,0) coordinate
pixel_threshold = 20
pix_per_mm = 6.80
crop_w_lower = 400
crop_w_upper = 1600


""" CHOPPING PARAMETERS """
crust_thickness_mm = 8
fine_slice_mm = 1
coarse_slice_mm = 3
dice_spacing_mm = 5


""" AUDIO STUFF """
audio_path = 'media'
audio_catagories = {
    'tea': 'tea',
    'chop': 'chop',
    'thud': 'thud',
    'safen': 'safen',
    'safes': 'safes',
    'score': 'score',
    'oops': 'oops',
    'thank': 'thank'
}  # I know this dict is useless now but eh it's fine, 'futureproofing' ya?
freq = 44100
bitsize = -16
channels = 2
buffer = 2048
volume = 0.95


""" DEBUG PARAMS """
DEBUG_MODE = True
SAVE_FRAMES = True
