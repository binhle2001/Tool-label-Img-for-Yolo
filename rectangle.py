import cv2
SOUND_BAR_WIDTH = 7
SOUND_BAR_HEIGHT = 2
SOUND_BAR_PADDING = 2
XMAX = [472, 654]
YMAX = 112
PADDING_MAX = 1


WEBCAM_TOP = 30
WEBCAM_BOT = 195
WEBCAM_LEFT_2 = 690 # for people = 2
WEBCAM_LEFT_3 = 534  # for people = 3
WEBCAM_PADDING = 2
WEBCAM_WIDTH = 270


name = 'trucAnh'
num = '1809'
num_cam = 0
num_sound_bar  = 8
label = 1
frame = cv2.imread(name + '/' + name + num + '.png')
def return_coordinate(num_sound_bar, i):
    YMIN = YMAX - num_sound_bar * SOUND_BAR_HEIGHT - SOUND_BAR_PADDING * (num_sound_bar)
    XMIN = XMAX[i] - SOUND_BAR_WIDTH
    XCENTER = (XMAX[i] + XMIN)/2
    YCENTER = (YMAX + YMIN)/2
    WIDTH = (XMAX[i] - XMIN)/frame.shape[1]
    HEIGHT = (YMAX - YMIN)/frame.shape[0]
    XCENTER = XCENTER/frame.shape[1]
    YCENTER = YCENTER/frame.shape[0]
    
    image = cv2.rectangle(frame, (XMIN, YMIN), (XMAX[i], YMAX), (0, 0, 255))
    return str(XCENTER), str(YCENTER), str(WIDTH), str(HEIGHT), image

xcenter, ycenter, width, height, img = return_coordinate(num_sound_bar, num_cam)

f = open(name + '_label/' + name + num + '.txt', 'w')
f.write(str(label) + ' ' + xcenter + ' ' + ycenter + ' ' + width + ' ' + height)
cv2.imwrite(name + '_rectangle/' + name + num + '.png', img)
