import os

WEBCAM_TOP = 20
WEBCAM_BOT = 130
WEBCAM_LEFT_2 = 460 # for people = 2
WEBCAM_LEFT_3 = 370  # for people = 3
WEBCAM_PADDING = 2
WEBCAM_WIDTH = 180

SOUND_BAR_WIDTH = 7
SOUND_BAR_HEIGHT = 2
SOUND_BAR_PADDING = 2
XMAX = 472 - WEBCAM_LEFT_2
YMAX = 112 - WEBCAM_TOP
PADDING_MAX = 1


WEBCAM_HEIGHT = 110

WIDTH_OLD = 1280
HEIGHT_OLD = 720

name = 'Gia_Bao_label'
dir_list = os.listdir(name)
print(dir_list)
for file in dir_list:
    file_name = file[:-4]
    f = open(name + '/' + file, 'r')
    s = f.read()
    
    label, x_center, y_center, width, height = s.split()
    # print(type(s))
    xcenter = (float(x_center) * WIDTH_OLD - WEBCAM_LEFT_2) / WEBCAM_WIDTH
    if xcenter > 1:
        xcenter = (float(x_center) * WIDTH_OLD - WEBCAM_WIDTH - WEBCAM_PADDING - WEBCAM_LEFT_2)/WEBCAM_WIDTH
    ycenter = (float(y_center) * HEIGHT_OLD - WEBCAM_TOP) / WEBCAM_HEIGHT
    new_width = float(width) * WIDTH_OLD / WEBCAM_WIDTH
    new_height = float(height) * HEIGHT_OLD / WEBCAM_HEIGHT
    fi = open('lb' + '/' + file, 'w')
    fi.write(label + ' ' + str(xcenter) + ' ' + str(ycenter) + ' ' + str(new_width) + ' ' + str(new_height))
