import cv2
import numpy as np
import time
from tensorflow import keras

import os  


SOUND_BAR_WIDTH = 7
SOUND_BAR_HEIGHT = 2
SOUND_BAR_PADDING = 2
XMAX = [472, 654]
YMAX = 112

PADDING_MAX = 1
WEBCAM_TOP = 20
WEBCAM_BOT = 130
WEBCAM_LEFT_2 = 460 # for people = 2
WEBCAM_LEFT_3 = 370  # for people = 3
WEBCAM_PADDING = 2
WEBCAM_WIDTH = 180



name_model = 'vgg16_classification_soundbar.h5'


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
#video feed 


def return_coordinate(num_sound_bar, i):
    YMIN = YMAX - num_sound_bar * SOUND_BAR_HEIGHT - SOUND_BAR_PADDING * num_sound_bar
    XMIN = XMAX[i] - SOUND_BAR_WIDTH
    XCENTER = (XMAX[i] + XMIN)/2
    YCENTER = (YMAX + YMIN)/2
    WIDTH = (XMAX[i] - XMIN)/frame.shape[1]
    HEIGHT = (YMAX - YMIN)/frame.shape[0]
    XCENTER = XCENTER/frame.shape[1]
    YCENTER = YCENTER/frame.shape[0]
    
    image = cv2.rectangle(frame, (XMIN, YMIN), (XMAX[i], YMAX), (0, 0, 255))
    return str(XCENTER), str(YCENTER), str(WIDTH), str(HEIGHT), image

def return_label(frame, i):
    if np.average(frame[YMAX - PADDING_MAX - SOUND_BAR_HEIGHT  : YMAX - PADDING_MAX, XMAX[i] - SOUND_BAR_WIDTH + SOUND_BAR_PADDING : XMAX[i] - SOUND_BAR_PADDING,  :]) < 130:
        return 1 #green
    return 0 #yellow

name = 'Nhu_y'
dir_list = os.listdir(name)
print(dir_list)
for file in dir_list:
    file_name = file[:-4]
    frame = cv2.imread(name +'/' + file_name + '.png')
    people_num = count_people(frame)
    list_wc = get_webcam_frame(frame, people_num)[0]
    f = open(name + '_label/' + file_name + '.txt', 'w')
    for i in range(len(list_wc)):
        wc_frame = list_wc[i]
        num_sound_bar = counting_soundbar_with_deeplearning(wc_frame, model)
        if num_sound_bar > 0:
            label = return_label(frame, i)
            xcenter, ycenter, width, height, img = return_coordinate(num_sound_bar, i)
            f.write(str(label) + ' ' + xcenter + ' ' + ycenter + ' ' + width + ' ' + height)
            cv2.imwrite(name + '_rectangle/' + file_name + '.png', img)



