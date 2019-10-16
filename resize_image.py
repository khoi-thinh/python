# Resize all JPEG images to 100x100 size in current directory
import cv2
import os
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if not name.endswith('.jpg'):
            continue
        else:
            if name.startswith('resized'):
                continue
            else:           
                img = cv2.imread(name)
                resize_img = cv2.resize(img,(100,100))
                print(os.path.join("resized-"+ name))
                cv2.imwrite(os.path.join("resized-" + name), resize_img)
