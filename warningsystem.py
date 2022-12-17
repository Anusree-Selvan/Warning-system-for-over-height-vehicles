import os
import sys
import time
from gtts import gTTS
from math import hypot
import cv2
import random
from playsound import*
#local files
import frame_capture
import frame_draw
def alert(tst):
    myobj=gTTS(text=tst, lang='en', slow=False)
    fname=str(random.randint(1000,2000))+'.mp3'
    myobj.save("E:\\check\\"+fname)
    playsound("E:\\check\\"+fname)
    os.remove("E:\\check\\"+fname)
    #camera values
    camera_id=0
    camera_width=1920
    camera_height=1080
    camera_frame_rate=30
    #camera_fourcc=cv2.VideoWriter_fourcc(*"YUYV")
    camera_fourcc=cv2.VideoWriter_fourcc(*"MJPG")
    #auto measure mouse events
    auto_percent=0.2
    auto_threshold=127
    auto_blur=5
    #normalisation mouse events
    norm_alpha=0
    norm_beta=255
    #read local config values
    configfile='camruler_config.csv'
    if os.path.isfile(configfile):
        with open(configfile)as f:
            for line in f:
                line=line.strip()
                if line and line[0]!='#'and (','in line or'=' in line):
                    if ','in line:
                        item,value=[x.strip()for x in line.split(',',1)]
                    elif '='in line:
                        item,value=[x.strip()for x in line.split('=',1)]
                    else:
                        continue
                    if item in 'camera_id camera_width camera_height camera_frame_rate camera_fourcc auto_percent auto_threshold auto_blur norm_alpha norm_beta'\
                                .split():
                            try:
                                exec(f'{item}={value}')
                                print('CONFIG:',(item, value))
                            except:
                                print('CONFIG ERROR:',(item, value))
                    # camera setup
                    # get camera id from argv[1]
                    # example "python3 camruler.py2"
                    if len(sys.argv)>1:
                        camera_id=sys.argv[1]
                        if camera_id.isdigit():
                            camera_id=int(camera_id)
                    #camera thread setup
                    camera=frame_capture.Camera_Thread()
                    camera.camera_source=1 #camera_id #SET THE CORRECT CAMERA NUMBER
                    camera.camera_width=camera_width
                    camera.camera_height=camera_height
                    camera.camera_frame_rate=camera_frame_rate
                    camera.camera_fourcc=camera_fourcc
                    #1 start camera thread
                    camera.start()
                    