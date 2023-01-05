import cv2
import numpy as np
import time
from tensorflow import keras
from setting import *
import os  


WEBCAM_TOP = 20
WEBCAM_BOT = 130
WEBCAM_LEFT_2 = 460 # for people = 2
WEBCAM_LEFT_3 = 370  # for people = 3
WEBCAM_PADDING = 2
WEBCAM_WIDTH = 180

# SOUND_BAR_WIDTH = 7
# SOUND_BAR_HEIGHT = 2
# SOUND_BAR_PADDING = 2
# XMAX = 472 - WEBCAM_LEFT_2
# YMAX = 112 - WEBCAM_TOP
# PADDING_MAX = 1

# TODO 1080
# WEBCAM_TOP = 30
# WEBCAM_BOT = 195
# WEBCAM_LEFT_2 = 690 # for people = 2
# WEBCAM_LEFT_3 = 534  # for people = 3
# WEBCAM_PADDING = 2
# WEBCAM_WIDTH = 270

# SOUND_BAR_WIDTH = 10
# SOUND_BAR_HEIGHT = 2
# SOUND_BAR_PADDING = 4
# XMAX = 709 - WEBCAM_LEFT_2
# YMAX = 168 - WEBCAM_TOP
# PADDING_MAX = 2


model = keras.models.load_model(name_model)
def counting_soundbar_with_deeplearning(webcam, model = model):
    webcam = cv2.resize(webcam, (180,110))
    webcam = np.expand_dims(webcam, axis=0)
    prediction = model.predict(webcam, batch_size=None,steps=1)
    soundbar = np.argmax(prediction[0])
    return soundbar


# if frame.shape[0] == 1080:
#     WEBCAM_TOP = 30
#     WEBCAM_BOT = 195
#     WEBCAM_LEFT_2 = 690 # for people = 2
#     WEBCAM_LEFT_3 = 534  # for people = 3
#     WEBCAM_PADDING = 2
#     WEBCAM_WIDTH = 270
def countVoiceSpace(img, model):
    if(img.shape[1] == 270):
        img = cv2.resize(img, (180, 110), interpolation = cv2.INTER_AREA)
    img = img[26:90, 5:15, :] #lấy khung sound_area
    img = cv2.resize(img, (64, 64), interpolation = cv2.INTER_AREA)
    img = img /255 #scaler
    tensor = np.expand_dims(img, axis = 0)
    y_pred = model.predict(tensor)
    return int(y_pred.flatten()[0] + 0.5)

   
def count_people(frame):
    back_ground = frame[WEBCAM_TOP:WEBCAM_BOT,WEBCAM_LEFT_3 - WEBCAM_WIDTH//2 :WEBCAM_LEFT_3,:]
    img_2 = frame[WEBCAM_TOP:WEBCAM_BOT,WEBCAM_LEFT_3:WEBCAM_LEFT_3 + WEBCAM_WIDTH//2,:]
    img_1 = frame[WEBCAM_TOP:WEBCAM_BOT,WEBCAM_LEFT_3 + WEBCAM_WIDTH//2:WEBCAM_LEFT_3 + WEBCAM_WIDTH,:]
    b_a = np.average(back_ground)
    i_a1 = np.average(img_1)
    i_a2 = np.average(img_2)
    if(0.97*b_a < i_a1 and 1.03 * b_a > i_a1): 
        return 1
    if(0.97*b_a < i_a2 and 1.03 * b_a > i_a2):
        return 2
    return 3
def get_webcam_frame(frame, people_num):
    wc_padding = WEBCAM_PADDING
    wc_width = WEBCAM_WIDTH
    wc_top = WEBCAM_TOP
    wc_bot = WEBCAM_BOT
    wc_left = WEBCAM_LEFT_2  # for people = 2
    if people_num == 3:
        wc_left = WEBCAM_LEFT_3

    frame_webcams = []
    webcam_positions = []
    for each in range(0, people_num):
        wc_right = wc_left + wc_width
        web_frame = frame[wc_top:wc_bot, wc_left:wc_right]
        frame_webcams.append(web_frame)
        # cv2.imwrite(f"webcams_{each}.png", web_frame)
        webcam_positions.append([wc_top, wc_bot, wc_left, wc_right])
        wc_left = wc_right + wc_padding
    return frame_webcams, webcam_positions

name = 'Gia_Bao'
dir_list = os.listdir(name)
print(dir_list)
for file in dir_list:
    file_name = file[:-4]
    frame = cv2.imread(name +'/' + file_name + '.png')
    people_num = count_people(frame)
    list_wc = get_webcam_frame(frame, people_num)[0]
    for i in range(len(list_wc)):
        wc_frame = list_wc[i]
        num_sound_bar = counting_soundbar_with_deeplearning(wc_frame, model)
        if num_sound_bar > 0:
            cv2.imwrite(name + '_webcam/' + file_name + '.png', wc_frame)
            break



