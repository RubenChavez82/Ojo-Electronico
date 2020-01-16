#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      ochavez6
#
# Created:     21/11/2019
# Copyright:   (c) ochavez6 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import cv2
import tkinter
from tkinter import *
from PIL import Image
from PIL import ImageTk

class videoStream:
    panel=None
    window=None
    camera=None

    def b1_pressed():
        print("b1_pressed")
    def b2_pressed():
        print("b2_pressed")
    def b3_pressed():
        print("b3_pressed")
    def b4_pressed():
        print("b4_pressed")
    def b5_pressed():
        print("b5_pressed")
    def b6_pressed():
        print("b6_pressed")
    def b7_pressed():
        print("b7_pressed")
    def b8_pressed():
        print("b8_pressed")


    def __init__(self):
        self.window=tkinter.Tk()
        self.window.title('Video')
        self.window.geometry("400x400")
        self.panel=tkinter.Label(self.window)



        self.panel.pack()



     #   self.panel.grid(self.window,row =1, column = 0)
        self.camera=cv2.VideoCapture(0)
        self.Camera1()
        self.window.mainloop()

    def Camera1(self):
        _,frame=self.camera.read()
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame=Image.fromarray(frame)
        frame=ImageTk.PhotoImage(frame)
        self.panel.configure(image=frame)
        self.panel.image=frame
        self.panel.after(1,self.Camera1)

    Button

def main():
    objVideo=videoStream()

if __name__ == '__main__':
    main()
