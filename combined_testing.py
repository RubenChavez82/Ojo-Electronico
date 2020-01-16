#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ochavez6
#
# Created:     25/11/2019
# Copyright:   (c) ochavez6 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PIL import Image as ImagePIL
from PIL import ImageTk
import tkinter as tk
from tkinter import *
import argparse
import datetime
import cv2
import os
import configparser
from functools import partial
import numpy as np
import time
import threading
import multitimer
import RPi.GPIO as GPIO

class Application:

    unlock=False  #used to unlock config buttons

    # Used for the 8 different types

    Type0=""
    Type1=""
    Type2=""
    Type3=""
    Type4=""
    Type5=""
    Type6=""
    Type7=""


    blowTime = ""   # Used for how long the valves will remain open
    current_image=""     # Used to store the image
    img_rgb=""           # Used to convert image to rgb
    loops = 0            # how many loops will be scanned
    loop_delay = 2       # how long will take from snap to snap during loop cycle

    def bOut0(self):
        print(float(self.blowTime))
        GPIO.output(self.Valve0,FALSE)
        #GPIO.digitalWrite(self.Valve0, GPIO.LOW)
        time.sleep(float(self.blowTime))
        #GPIO.digitalWrite(self.Valve0, GPIO.HIGH)
        GPIO.output(self.Valve0,TRUE)
        print('off')
    def bOut1(self):
        print("bOut1")
        GPIO.output(self.Valve1,FALSE)
        #GPIO.digitalWrite(self.Valve0, GPIO.LOW)
        time.sleep(float(self.blowTime))
        #GPIO.digitalWrite(self.Valve0, GPIO.HIGH)
        GPIO.output(self.Valve1,TRUE)
    def bOut2(self):
        print("bOut2")
        GPIO.output(self.Valve2,FALSE)
        #GPIO.digitalWrite(self.Valve0, GPIO.LOW)
        time.sleep(float(self.blowTime))
        #GPIO.digitalWrite(self.Valve0, GPIO.HIGH)
        GPIO.output(self.Valve2,TRUE)
    def bOut3(self):
        print("bOut3")
        GPIO.output(self.Valve3,FALSE)
        #GPIO.digitalWrite(self.Valve0, GPIO.LOW)
        time.sleep(float(self.blowTime))
        #GPIO.digitalWrite(self.Valve0, GPIO.HIGH)
        GPIO.output(self.Valve3,TRUE)
    def bOut4(self):
        print("bOut4")
        GPIO.output(self.Valve4,FALSE)
        #GPIO.digitalWrite(self.Valve0, GPIO.LOW)
        time.sleep(float(self.blowTime))
        #GPIO.digitalWrite(self.Valve0, GPIO.HIGH)
        GPIO.output(self.Valve4,TRUE)
    def bOut5(self):
        print("bOut5")
        GPIO.output(self.Valve5,FALSE)
        #GPIO.digitalWrite(self.Valve0, GPIO.LOW)
        time.sleep(float(self.blowTime))
        #GPIO.digitalWrite(self.Valve0, GPIO.HIGH)
        GPIO.output(self.Valve5,TRUE)

    def reset_Counters(self):
        pass
    def unlock_buttons(self):

        if self.unlock:
            self.unlock=False
            self.b0Out.config(state=DISABLED)
            self.b1Out.config(state=DISABLED)
            self.b2Out.config(state=DISABLED)
            self.b3Out.config(state=DISABLED)
            self.b4Out.config(state=DISABLED)
            self.b5Out.config(state=DISABLED)
            #self.b6Out.config(state=DISABLED)
            #self.b7Out.config(state=DISABLED)

            self.b0Cap.config(state=DISABLED)
            self.b1Cap.config(state=DISABLED)
            self.b2Cap.config(state=DISABLED)
            self.b3Cap.config(state=DISABLED)
            self.b4Cap.config(state=DISABLED)
            self.b5Cap.config(state=DISABLED)
            self.b6Cap.config(state=DISABLED)
            self.b7Cap.config(state=DISABLED)

            self.loopCapture.config(state=DISABLED)

            self.opMenu.configure(state = DISABLED)

            self.resetCounters.configure(state = DISABLED)

        else:

            self.unlock=True
            self.b0Out.config(state=NORMAL)
            self.b1Out.config(state=NORMAL)
            self.b2Out.config(state=NORMAL)
            self.b3Out.config(state=NORMAL)
            self.b4Out.config(state=NORMAL)
            self.b5Out.config(state=NORMAL)
            #self.b6Out.config(state=NORMAL)
            #self.b7Out.config(state=NORMAL)

            self.b0Cap.config(state=NORMAL)
            self.b1Cap.config(state=NORMAL)
            self.b2Cap.config(state=NORMAL)
            self.b3Cap.config(state=NORMAL)
            self.b4Cap.config(state=NORMAL)
            self.b5Cap.config(state=NORMAL)
            self.b6Cap.config(state=NORMAL)
            self.b7Cap.config(state=NORMAL)

            self.loopCapture.config(state=NORMAL)

            self.opMenu.configure(state = NORMAL)

            self.resetCounters.configure(state = NORMAL)

            self.btnTrain.configure(state = NORMAL)


    def read_ini(self):
        #Create and read the ini file

        if not os.path.isfile("config.ini"):
            f=open("config.ini","w+")
            f.write("#Configuration File\n")
            f.write("[Types]\n")
            f.write("Type 0 = Type 0\n")
            f.write("Type 1 = Type 1\n")
            f.write("Type 2 = Type 2\n")
            f.write("Type 3 = Type 3\n")
            f.write("Type 4 = Type 4\n")
            f.write("Type 5 = Type 5\n")
            f.write("Type 6 = Type 6\n")
            f.write("Type 7 = Type 7\n")
            f.write("[IO Ports]\n")
            f.write("Blow Time = .25\n")
            f.write("Loop Capture = 1000\n")
            f.write("loop Delay = 2\n")

            f.close()

        config=configparser.ConfigParser()
        config.read("config.ini")
        self.Type0 = config['Types']['Type 0']
        self.Type1 = config['Types']['Type 1']
        self.Type2 = config['Types']['Type 2']
        self.Type3 = config['Types']['Type 3']
        self.Type4 = config['Types']['Type 4']
        self.Type5 = config['Types']['Type 5']
        self.Type6 = config['Types']['Type 6']
        self.Type7 = config['Types']['Type 7']
        self.blowTime=config['IO Ports']['Blow Time']
        self.loops=config['IO Ports']['Loop Capture']
        self.loop_delay=config['IO Ports']['Loop Delay']
        self.notTrainedNuts = 8

    def update_types(self):
        #update the labels based on the info read from ini file
        self.ltype0.config(text=self.Type0)
        self.ltype1.config(text=self.Type1)
        self.ltype2.config(text=self.Type2)
        self.ltype3.config(text=self.Type3)
        self.ltype4.config(text=self.Type4)
        self.ltype5.config(text=self.Type5)
        self.ltype6.config(text=self.Type6)
        self.ltype8.config(text=self.Type7)



    def __init__(self, output_path = "./"):

        self.durationTime = 0
        
        # Used to enable the valves
        self.Valve0 = 40
        self.Valve1 = 38
        self.Valve2 = 37
        self.Valve3 = 36
        self.Valve4 = 35
        self.Valve5 = 33
        #Valve6 = 24
        #Valve7 = 26

        self.midIR = 32     #Input to detect using IR sensor
        self.endIR = 31        #Input to detect using IR sensor

        #GPIO Port Config
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.Valve0,GPIO.OUT)
        GPIO.setup(self.Valve1,GPIO.OUT)
        GPIO.setup(self.Valve2,GPIO.OUT)
        GPIO.setup(self.Valve3,GPIO.OUT)
        GPIO.setup(self.Valve4,GPIO.OUT)
        GPIO.setup(self.Valve5,GPIO.OUT)
        GPIO.setup(self.midIR,GPIO.IN)
        GPIO.setup(self.endIR,GPIO.IN)
        GPIO.output(self.Valve0,TRUE)
        """ Initialize application which uses OpenCV + Tkinter. It displays
            a video stream in a Tkinter window and stores current snapshot on disk """
                
        self.vs = cv2.VideoCapture(0) # capture video frames, 0 is your default video camera
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera

        self.window = tk.Tk()  # initialize root window
        self.window.title("Pendiente ponerle titulo")  # set window title
        # self.destructor function gets fired when the window is closed
        self.window.protocol('WM_DELETE_WINDOW', self.destructor)

        self.opMenuVar = StringVar(self.window)
        self.opMenuVar.set("")

        #Frames
        self.fImage= tk.LabelFrame(self.window, text = "Image", relief = RIDGE )
        self.fTypes = tk.LabelFrame(self.window, text = "Types",  relief = RIDGE )
        self.fOptions = tk.LabelFrame(self.window, text = "Options",  relief = RIDGE )

        # define layout

        #Menu bar
        menubar=Menu(self.window)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_checkbutton(label="Unlock Buttons",onvalue=0, offvalue=1,command=self.unlock_buttons)
        #filemenu.add_command(label="Capture Background",command=self.unlock_buttons)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command =self.destructor)
        menubar.add_cascade(label="Options",menu=filemenu )
        self.window.config(menu=menubar)

        # Frames
        self.fImage.grid(row=0, column = 0, rowspan = 9, columnspan=1, padx=(2,2), pady=(2,2))
        self.fTypes.grid(row = 0, column = 1, padx=(2,2), pady=(2,2))
        self.fOptions.grid(row = 2, column = 1, padx=(2,2), pady=(2,2))

        self.panel = tk.Label(self.fImage)  # initialize image panel
        self.panel.grid(row=0,column=0,padx=(2,2), pady=(2,2))

        #Labels for types
        Label(self.fTypes, text = "Types").grid(row = 0, column = 0, sticky = EW, padx = 5, pady = 0, columnspan=2)
        Label(self.fTypes, text = "Type 0:").grid(row = 1, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Type 1:").grid(row = 2, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Type 2:").grid(row = 3, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Type 3:").grid(row = 4, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Type 4:").grid(row = 5, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Type 5:").grid(row = 6, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Type 6:").grid(row = 7, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Type 7:").grid(row = 8, column = 0, sticky = EW, padx = 5, pady = 0)
        Label(self.fTypes, text = "Otros:").grid(row = 9, column = 0, sticky = EW, padx = 5, pady = 0)

       # Label(self.fTypes, text = "Types").grid(row = 0, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype0 = Label(self.fTypes, text = "Type 0")
        self.ltype1 = Label(self.fTypes, text = "Type 1")
        self.ltype2 = Label(self.fTypes, text = "Type 2")
        self.ltype3 = Label(self.fTypes, text = "Type 3")
        self.ltype4 = Label(self.fTypes, text = "Type 4")
        self.ltype5 = Label(self.fTypes, text = "Type 5")
        self.ltype6 = Label(self.fTypes, text = "Type 6")
        self.ltype7 = Label(self.fTypes, text = "Type 7")
        self.ltype8 = Label(self.fTypes, text = "Otros")

        self.ltype0.grid(row = 1, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype1.grid(row = 2, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype2.grid(row = 3, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype3.grid(row = 4, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype4.grid(row = 5, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype5.grid(row = 6, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype6.grid(row = 7, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype7.grid(row = 8, column = 1, sticky = EW, padx = 5, pady = 0)
        self.ltype8.grid(row = 9, column = 1, sticky = EW, padx = 5, pady = 0)

        Label(self.fTypes, text = "Cantidad").grid(row = 0, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount0 = Label(self.fTypes, text = "0")
        self.lCount1 = Label(self.fTypes, text = "0")
        self.lCount2 = Label(self.fTypes, text = "0")
        self.lCount3 = Label(self.fTypes, text = "0")
        self.lCount4 = Label(self.fTypes, text = "0")
        self.lCount5 = Label(self.fTypes, text = "0")
        self.lCount6 = Label(self.fTypes, text = "0")
        self.lCount7 = Label(self.fTypes, text = "0")
        self.lCount8 = Label(self.fTypes, text = "0")


        self.lCount0.grid(row = 1, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount1.grid(row = 2, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount2.grid(row = 3, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount3.grid(row = 4, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount4.grid(row = 5, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount5.grid(row = 6, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount6.grid(row = 7, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount7.grid(row = 8, column = 2, sticky = EW, padx = 5, pady = 0)
        self.lCount8.grid(row = 9, column = 2, sticky = EW, padx = 5, pady = 0)

        #Output enable buttons
        self.b0Out = tk.Button(self.fOptions, text = "Ouput 0", command = self.bOut0, state = DISABLED)
        self.b1Out = tk.Button(self.fOptions, text = "Ouput 1", command = self.bOut1, state = DISABLED)
        self.b2Out = tk.Button(self.fOptions, text = "Ouput 2", command = self.bOut2, state = DISABLED)
        self.b3Out = tk.Button(self.fOptions, text = "Ouput 3", command = self.bOut3, state = DISABLED)
        self.b4Out = tk.Button(self.fOptions, text = "Ouput 4", command = self.bOut4, state = DISABLED)
        self.b5Out = tk.Button(self.fOptions, text = "Ouput 5", command = self.bOut5, state = DISABLED)
        #self.b6Out = tk.Button(self.fOptions, text = "Ouput 6", command = self.bOut6, state = DISABLED)
        #self.b7Out = tk.Button(self.fOptions, text = "Ouput 7", command = self.bOut7, state = DISABLED)

        self.b0Out.grid(row = 0, column = 1, sticky = EW, padx = 5, pady = 0 )
        self.b1Out.grid(row = 1, column = 1, sticky = EW, padx = 5, pady = 0 )
        self.b2Out.grid(row = 2, column = 1, sticky = EW, padx = 5, pady = 0 )
        self.b3Out.grid(row = 3, column = 1, sticky = EW, padx = 5, pady = 0 )
        self.b4Out.grid(row = 4, column = 1, sticky = EW, padx = 5, pady = 0 )
        self.b5Out.grid(row = 5, column = 1, sticky = EW, padx = 5, pady = 0 )
        #self.b6Out.grid(row = 6, column = 1, sticky = EW, padx = 5, pady = 0 )
        #self.b7Out.grid(row = 7, column = 1, sticky = EW, padx = 5, pady = 0 )

        #single Capture buttons
        self.b0Cap = tk.Button(self.fOptions, text = "Capture 0", command = lambda: self.take_snapshot(1), state = DISABLED)
        self.b1Cap = tk.Button(self.fOptions, text = "Capture 1", command = lambda: self.take_snapshot(2), state = DISABLED)
        self.b2Cap = tk.Button(self.fOptions, text = "Capture 2", command = lambda: self.take_snapshot(3), state = DISABLED)
        self.b3Cap = tk.Button(self.fOptions, text = "Capture 3", command = lambda: self.take_snapshot(4), state = DISABLED)
        self.b4Cap = tk.Button(self.fOptions, text = "Capture 4", command = lambda: self.take_snapshot(5), state = DISABLED)
        self.b5Cap = tk.Button(self.fOptions, text = "Capture 5", command = lambda: self.take_snapshot(6), state = DISABLED)
        self.b6Cap = tk.Button(self.fOptions, text = "Capture 6", command = lambda: self.take_snapshot(7), state = DISABLED)
        self.b7Cap = tk.Button(self.fOptions, text = "Capture 7", command = lambda: self.take_snapshot(8), state = DISABLED)

        self.b0Cap.grid(row = 0, column = 2, sticky = EW, padx = 5, pady = 0 )
        self.b1Cap.grid(row = 1, column = 2, sticky = EW, padx = 5, pady = 0 )
        self.b2Cap.grid(row = 2, column = 2, sticky = EW, padx = 5, pady = 0 )
        self.b3Cap.grid(row = 3, column = 2, sticky = EW, padx = 5, pady = 0 )
        self.b4Cap.grid(row = 4, column = 2, sticky = EW, padx = 5, pady = 0 )
        self.b5Cap.grid(row = 5, column = 2, sticky = EW, padx = 5, pady = 0 )
        self.b6Cap.grid(row = 6, column = 2, sticky = EW, padx = 5, pady = 0 )
        self.b7Cap.grid(row = 7, column = 2, sticky = EW, padx = 5, pady = 0 )


        #button to reset counters

        self.resetCounters = tk.Button(self.fOptions, text = "Reset Counters", command = lambda: self.reset_Counters, state = DISABLED)

        self.resetCounters.grid(row = 1, column = 3, sticky = EW, padx = 5, pady = 0, columnspan =2  )



       # create a button, that when pressed, will take the current frame and save it to file
       # btn = tk.Button(self.window, text="Snapshot!", command=self.take_snapshot)
       # btn.grid(row=3,column=0,padx=(2,2), pady=(2,2))

        self.read_ini()
        self.update_types()
        self.Types = {0:self.Type0,
            1: self.Type1,
            2: self.Type2,
            3: self.Type3,
            4: self.Type4,
            5: self.Type5,
            6: self.Type6,
            7: self.Type7}
        self.LTypes = {0:self.ltype0,
            1: self.ltype1,
            2: self.ltype2,
            3: self.ltype3,
            4: self.ltype4,
            5: self.ltype5,
            6: self.ltype6,
            7: self.ltype7}
        self.TypesTrained = {}
        self.nuts = {}
        
        for i in self.Types:
            if os.path.isfile(str(self.Types[i])+'autotrained.xml'):
                self.LTypes[i].configure(fg='green')
                self.TypesTrained[i] = cv2.CascadeClassifier('Type '+str(i)+'autotrained.xml')
                #print('ok')
            else:
                self.LTypes[i].configure(fg='red')
                #print('not')
        #Option Menu to loop capture for type identifying
        self.opMenu = tk.OptionMenu(self.fOptions,self.opMenuVar,self.Type0,self.Type1,self.Type2,self.Type3,self.Type4,self.Type5,self.Type6,self.Type7,"Background")
        self.opMenu.grid(row = 0, column = 3, sticky = EW, padx = 5, pady = 0)
        self.opMenu.configure(state = DISABLED)

        self.loopCapture = tk.Button(self.fOptions, text = "Loop Capture "+self.loops, command = lambda: self.loop_snap(self.opMenuVar.get()), state = DISABLED)

        self.loopCapture.grid(row = 0, column = 4, sticky = EW, padx = 5, pady = 0 )
        #IR Labels

        self.lblmidIR = Label(self.fOptions, text ="0", bg = "red")
        self.lblendIR = Label(self.fOptions, text ="0", bg = "red")


        self.lblmidIR.grid(row = 3, column = 3, sticky = EW, columnspan = 1 )
        self.lblendIR.grid(row = 4, column = 3, sticky = EW, columnspan = 1 )
        

        # start a self.video_loop that constantly pools the video sensor
        # for the most recently read frame
        self.video_loop()
        self.window.resizable(False, False)

         #button to train

        self.btnTrain = tk.Button(self.fOptions, text = "Train", command = lambda: self.training(), state = DISABLED)

        self.btnTrain.grid(row = 2, column = 3, sticky = EW, padx = 5, pady = 0, columnspan =2  )

     

    def video_loop(self):
        
        if (GPIO.input(self.midIR)==FALSE):
            self.lblmidIR.configure(bg="blue",text='1')
            #print('mid')
        else:
            self.lblmidIR.configure(bg="red",text='0')

        if (GPIO.input(self.endIR)==FALSE):
            self.lblendIR.configure(bg="green",text='1')
            #print('end')
        else:
            self.lblendIR.configure(bg="red",text='0')
        
     #   print(str(datetime.datetime.now()))
        """ Get frame from the video stream and show it in Tkinter """
        ok, frame = self.vs.read()  # read frame from video stream
  
        if ok:  # frame captured without any errors
            #cv2.putText(frame,str(self.notTrainedNuts-len(self.TypesTrained))+' not trained',(1,100),cv2.FONT_HERSHEY_COMPLEX,1,(250,250,250),2,cv2.LINE_AA)
            '''if str(self.loopCapture['text']).find('Loop Capture') != -1:
                    #identify image or snapshot for training
                    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                    for j in self.TypesTrained:
                        self.nuts[j]=self.TypesTrained[j].detectMultiScale3(gray, outputRejectLevels=True)
                        #print(str(j))
                        for (x,y,w,h) in self.nuts[j][0]:
                            #print('nut detected on'+str(x)+', '+str(y))
                            font = cv2.FONT_HERSHEY_COMPLEX
                            #cv2.putText(frame,str(self.Types[j]),(x+w,y+h),font,1,(250,250,250),2,cv2.LINE_AA)
                            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                            roi_gray = gray[y:y+h, x:x+w]
                            roi_color = frame[y:y+h, x:x+w]
                            #print(self.nuts[j][2])
'''
            #show image on tkinter
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.img_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            self.current_image= ImagePIL.fromarray(cv2image)
            self.img_rgb=ImagePIL.fromarray(self.img_rgb)
           # self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image



        self.window.after(30, self.video_loop)  # call the same function after 30 milliseconds


    def bpress(self,i):
        switcher={
            1:'Type0',
            2:'Type1',
            3:'Type2',
            4:'Type3',
            5:'Type4',
            6:'Type5',
            7:'Type6',
            8:'Type7'
                }
        return switcher.get(i,"0")

    def loop_snap(self,idT):

        print("loop Snapshot " + str(idT))
        if self.opMenuVar.get()!="":
            if str(self.loopCapture['text']).find('Loop Capture') != -1:
                self.loopCapture.configure(text = "Stop " + str(self.loops))
                self.opMenu.configure(state= DISABLED)
                #self.snap_timer = threading.Timer(2,self.get_snap,args=None,kwargs=None)
                self.snap_timer = multitimer.MultiTimer(interval=2,function = self.get_snap,count=int(self.loops)+1)
                self.snap_timer.start()

            else:
                print("cancel timer")
                self.read_ini()
                self.loopCapture.configure(text="Loop Capture " +str(self.loops))
                self.opMenu.configure(state= NORMAL)
                self.snap_timer.stop()

    def get_snap(self):
        dummyCnt = 0
        print("loops: " + str(self.loops))
        while int(self.loops)!=0:
            ts = datetime.datetime.now() # grab the current timestamp
            p=os.path.join(os.getcwd()+"//"+self.opMenuVar.get())
            filename = p+"//"+self.opMenuVar.get()+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename

            if not os.path.isdir(p):
               os.mkdir(p)
            #startTimer = datetime.datetime.now()   
            #print(str(startTimer))
            #print(filename)
            if (self.opMenuVar.get() != "Background")&(GPIO.input(self.midIR)==FALSE):
                self.img_rgb.save(filename, "JPEG")  # save image as jpeg file
                self.loops= int(self.loops)-1
            
                print("[INFO] saved {}".format(filename))
            #self.loops= int(self.loops)-1
                self.loopCapture.configure(text = "Stop " + str(self.loops))
                print(int(self.loops))
                time.sleep(.13)
                dummyCnt = dummyCnt + 1
            elif (self.opMenuVar.get() == "Background"):
                self.img_rgb.save(filename, "JPEG")  # save image as jpeg file
                self.loops= int(self.loops)-1
            
                print("[INFO] saved {}".format(filename))
            
                self.loopCapture.configure(text = "Stop " + str(self.loops))
                print(int(self.loops))
                time.sleep(.33)
                
            if GPIO.input(self.endIR)==FALSE:
                dummyCnt = dummyCnt - 1
                time.sleep(.13)
            if dummyCnt > 5:
                print('[ERROR]')
                self.loops = 0
            #print(dummyCnt)   
            #Creates txt files for training 0.110345
            #endTimer=datetime.datetime.now()
            #self.durationTime = self.durationTime + (endTimer-startTimer)
            #print(str(endTimer))
            if self.loops == 0:
                if os.path.exists(str(self.opMenuVar.get())+'.txt'):
                    os.unlink(str(self.opMenuVar.get())+'.txt')
                for img in os.listdir(self.opMenuVar.get()):
                    if self.opMenuVar.get() == "Background":
                        line = str(self.opMenuVar.get())+"/" + img + "\n"
                    else:
                        line = str(self.opMenuVar.get())+"/" + img + " 1 0 0 50 50\n"
                    with open(str(self.opMenuVar.get())+'.txt','a') as f:
                        f.write(line)
        else:
            print("entering else statement")
            self.snap_timer.stop()
            self.read_ini()
            self.loopCapture.configure(text="Loop Capture " +self.loops)
            self.opMenu.configure(state= NORMAL)


    def take_snapshot(self,idT):
        """ Take snapshot and save it to the file """
        ts = datetime.datetime.now() # grab the current timestamp
        if idT==0:
            p=os.path.join(os.getcwd()+"\\"+self.Type0)
            filename = p+"\\"+self.Type1+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        if idT==1:
            p=os.path.join(os.getcwd()+"\\"+self.Type1)
            filename = p+"\\"+self.Type2+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        if idT==2:
            p=os.path.join(os.getcwd()+"\\"+self.Type2)
            filename = p+"\\"+self.Type3+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        if idT==3:
            p=os.path.join(os.getcwd()+"\\"+self.Type3)
            filename = p+"\\"+self.Type4+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        if idT==4:
            p=os.path.join(os.getcwd()+"\\"+self.Type4)
            filename = p+"\\"+self.Type5+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        if idT==5:
            p=os.path.join(os.getcwd()+"\\"+self.Type5)
            filename = p+"\\"+self.Type6+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        if idT==6:
            p=os.path.join(os.getcwd()+"\\"+self.Type6)
            filename = p+"\\"+self.Type7+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
        if idT==7:
            p=os.path.join(os.getcwd()+"\\"+self.Type7)
            filename = p+"\\"+self.Type8+" {}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename

        if not os.path.isdir(p):
            os.mkdir(p)


        print(filename)

        self.img_rgb.save(filename, "JPEG")  # save image as jpeg file
        print("[INFO] saved {}".format(filename))

    def destructor(self):
        """ Destroy the root object and release all resources """
        print("[INFO] closing...")
        self.window.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

    def training(self):
        if not(os.path.exists('Background.txt')):
            print("[ERROR] Missing Background.txt")
        elif not(os.path.exists(str(self.opMenuVar.get())+'.txt')):
            print("[ERROR] Missing"+str(self.opMenuVar.get())+'.txt')
        elif(str(self.opMenuVar.get())=="Background"):
            print("[ERROR] Can't Train Background Images")
        else:
            #Trainig comands only active if the files exists
            print('[INFO] Training...')



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
    help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())

# start the app
print("[INFO] starting...")
#try:
pba = Application(args["output"])
pba.window.mainloop()
#except Exception as e:
#    print(str(e))




