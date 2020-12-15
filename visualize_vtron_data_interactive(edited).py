import cv2
import crop_video_beep ###########
import pandas
from os.path import isfile
from pylab import *
from crop_video_beep import video_file_02 ###########


video_file = "familiar_driver/relaxed/360_view/GS010055_0_to_60s.mp4"
video_file02 = f"familiar_driver/relaxed/face_view/{video_file_02}_shifted.mp4" ########################
excel_file = "familiar_driver/relaxed/Familiar_Driver_Relaxed.xlsx"


# helper class for an interactive plot with a cross-hair
class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """

    def __init__(self, ax, x, y, video, video02):
        self.ax = ax
        self.lx = ax.axhline(color='k')  # the horiz line
        self.ly = ax.axvline(color='k')  # the vert line
        self.x = x
        self.y = y
        self.video = video
        self.video02 = video02 #################################
        # text location in axes coords
        self.txt = ax.text(0.7, 0.9, '', transform=ax.transAxes)
        
    def __del__(self):
        print("destructor called")
       #video.release()

    def mouse_move(self, event):

        if not event.inaxes:
            return

        x, y = event.xdata, event.ydata

        indx = searchsorted(self.x, [x])[0]
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)

        self.txt.set_text('x=%1.2f, y=%1.2f' % (x, y))
        print('x=%1.2f, y=%1.2f' % (x, y))
        draw()
        
        # seek to the selected position in the video file
        video.set(cv2.CAP_PROP_POS_MSEC, x*1000)
        video02.set(cv2.CAP_PROP_POS_MSEC, x*1000) ######################################
        # Frame acquisition
        (_, frame) = video.read()  

        frame_output = cv2.resize(frame, (round(0.25*frame.shape[1]), round(0.25*frame.shape[0])))
    
        # show output
        cv2.imshow('ball_tracker', frame_output)
        
        ###############################################
        (_, frame) = video02.read() ###################
        frame_output02 = cv2.resize(frame, (round(0.25*frame.shape[1]), round(0.25*frame.shape[0]))) ###################
        cv2.imshow('balllllll_tracker', frame_output02) ###################

        # process events
        cv2.waitKey(1)


if isfile('data_cached.npy'):
    data = load('data_cached.npy', allow_pickle=True)
else:
    print("wait while loading excel file - this will take a few seconds.")
    data_xls = pandas.read_excel(excel_file)
    data = array(data_xls)
    save('data_cached.npy', data)
    

start_row = 6;

# plot the first 60 seconds of brake paddle value
fps = int(1/0.02) # data in xls file seems to be recorded at roughly 50 fps

header_strings = data[5,:]

time = data[start_row: start_row + 60 * fps ,0]

idx = where(header_strings == 'V_GAS_PEDAL')

paddle = data[start_row: start_row + 60 * fps , idx[0][0]]


video = cv2.VideoCapture(video_file)
video02 = cv2.VideoCapture(video_file02)

fig, ax = plt.subplots()
cursor = SnaptoCursor(ax, time, paddle, video, video02)
plt.connect('motion_notify_event', cursor.mouse_move)



ax.plot(time, paddle, 'r')
plt.axis([0, time[-1], 0, 500])
plt.show()





