import cv2
import sys
from matplotlib import pyplot as plt 
  
# Opening image 
img = cv2.imread(sys.argv[1])
edged = cv2.Canny(img, 10, 30)
cv2.imshow("Image", edged)
cv2.waitKey(0)
  
# OpenCV opens images as BRG  
# but we want it as RGB We'll  
# also need a grayscale version 
# img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
# _, thresh_img = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
# contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# found = sorted(contours, key=cv2.contourArea, reverse=True)
# found = [found[0]]

# found_r = [cv2.boundingRect(contour) for contour in found]
  
# # Don't do anything if there's  
# # no sign 
# amount_found = len(found_r) 
  
# if amount_found != 0: 
      
#     # There may be more than one 
#     # sign in the image 
#     for (x, y, width, height) in found_r: 
          
#         # We draw a green rectangle around 
#         # every recognized sign 
#         cv2.rectangle(img_rgb, (180, 256),
#                       (1070,930),
#                       (0, 255, 0), 5)
        
#         # cv2.circle(img_rgb, (x + int(height / 2), y + int(width / 2)), 5, (255, 0, 0), 5) 
          
# # Creates the environment of  
# # the picture and shows it 
# plt.subplot(1, 1, 1) 
# plt.imshow(img_rgb) 
# plt.show() 