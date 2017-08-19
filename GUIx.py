#  Made By: Adarsh Pradyut

import tkinter
import time
import random
import _thread
import queue
import serial
import cv2
from PIL import Image, ImageTk
import argparse
from imutils.video import *
import imutils
import math


backgroundMain = "BLACK"
background1 = "#263238"  # "BLUE"
background2 = "#263238"  # "GREEN"
background3 = "#263238"  # "YELLOW"
foreground = "WHITE"
welcomeback = "#00838F"

# image paths
logoTeam = "/home/pi/Downloads/TeamLogo.png"
logoSrm = "/home/pi/Downloads/SrmLogo.png"
backing = "/home/pi/Downloads/back2.png"

# Screen dimensions
Height = 480
Width = 800

# Variables
bdvalue =0

#trying connection to the Arduino
#port detection is automatic for raspi
try:
    ser = serial.Serial('/dev/ttyACM0',baudrate = 9600)
except:
    print ("ARDUINO NOT CONNECTED!!!")
    time.sleep(1)
    

#webcam settings
ap = argparse.ArgumentParser()
ap.add_argument("-p","--picamera",type = int, default=-1, help = "whether or not the Raspberry Pi should be used")
args = vars(ap.parse_args())
print("Switch Camera ON")
#time.sleep(2)
print("Moving on...")
#time.sleep(1)

class Menu:
    
    def videoLoop(self):
            self.vs = VideoStream(usePiCamera=args["picamera"]>0).start()

            while (True):
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width = 466 )
                self.frame = cv2.flip(self.frame,1)
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                self.frameimgMain = tkinter.Frame(self.root,width = Width, height = (Height/2)+40,bg = backgroundMain, bd = bdvalue)
                self.frameimgL = tkinter.Frame(self.frameimgMain,width = Width/3-100, height = (Height/2)+40,bg = background1, bd = bdvalue)
                self.frameimgC = tkinter.Frame(self.frameimgMain,width = Width/3+200, height = (Height/2)+40,bg = background2, bd = bdvalue)
                self.frameimgR = tkinter.Frame(self.frameimgMain,width = Width/3-100, height = (Height/2)+40,bg = background3, bd = bdvalue)
                if self.panel is None:
                    self.panel = tkinter.Label(self.frameimgC,image=image)
                    self.panel.image = image
                    self.frameimgMain.pack(side = 'bottom', fill ='x')
                    self.frameimgL.pack(side = 'left',expand = 'yes', fill ='both')
                    self.panel.pack(anchor = 'center')
                    self.frameimgC.pack(side = 'left',expand = 'yes', fill ='x')
                    self.frameimgR.pack(side = 'left',expand = 'yes', fill ='both')
                    #Top frame starts
                    #Image objects
                    self.team = tkinter.PhotoImage(file =logoTeam)
                    self.srm = tkinter.PhotoImage(file = logoSrm)
                    #Image labels
                    self.LabelTeam = tkinter.Label(self.frameimgR, image = self.team)
                    self.LabelSrm = tkinter.Label(self.frameimgL, image = self.srm)
                    self.LabelTeam.pack(anchor = 'center')
                    self.LabelSrm.pack(anchor = 'center')

                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

    def getNum(value):
        value = str(value)
        line = []
        i = 2
        while(value[i].isnumeric()):
            line.append(value[i])
            i = i+ 1
        n = -1
        reverse = 0
        for i in line:
            n += 1
            digit = math.pow(10,n)
            reverse = int(i)*digit + reverse
        reverse = int(reverse)
        final = int(str(reverse)[::-1])
        return final
    def GetTemp(self):

        while(1):

            value = ser.readline()
            value = str(value)
            line = []
            i = 2
            while(value[i].isnumeric()):
                line.append(value[i])
                i = i+ 1
            n = -1
            reverse = 0
            for i in line:
                n += 1
                digit = math.pow(10,n)
                reverse = int(i)*digit + reverse
            reverse = int(reverse)
            final = int(str(reverse)[::-1])
            value = final
            self.speedValue.set(str(value))
            print(self.speedValue.get())
            time.sleep(0.5)

        
    def __init__(self):    
        self.frame = None
        self.vs = cv2.VideoCapture(0)
        #welcome screen
        self.welcome = tkinter.Tk()
        self.welcome.attributes("-fullscreen",True)
        self.back = tkinter.PhotoImage(file =backing)
        self.center = tkinter.Frame(self.welcome,width = Width, height = Height,bg = welcomeback)
        self.center.pack()
        self.LabelBack = tkinter.Label(self.center, image = self.back)
        self.LabelBack.pack(side='left')
        self.welcome.after(4000,self.welcome.destroy)
        self.welcome.mainloop()


        self.root = tkinter.Tk()
        self.frame = None
        self.panel = None
        #Frames definitions

        self.framelabelsMain = tkinter.Frame(self.root,width = Width, height = (Height/2)-40, bg = backgroundMain ,bd = bdvalue )
        self.framelabelsL = tkinter.Frame(self.framelabelsMain,width = (Width/2),height = (Height/2)-40,bg = background3 ,bd = bdvalue )
        self.framelabelsR = tkinter.Frame(self.framelabelsMain,width = (Width/2),height = (Height/2)-40,bg = background2, bd = bdvalue)


        



        self.framelabelsMain.pack(side = 'top', fill = 'both', expand = 'yes')


        self.framelabelsL.pack(side = 'left', fill = 'both', expand = 'yes')


        self.framelabelsR.pack(side = 'left', fill = 'both', expand = 'yes')

        self.root.attributes("-fullscreen",True)
        

        #Right frame starts
        self.speedValue = tkinter.StringVar()
        self.labelkmph = tkinter.Label(self.framelabelsL, fg = foreground, bg = background2, text = "kmph", font = ("Times_New_Roman",43))
        self.labelSpeedValue = tkinter.Label(self.framelabelsL, fg = foreground, bg = background2, textvariable = self.speedValue, font = ("Times_New_Roman",56))
        self.labelSpeedValue.place(y = 10, x = 380)
        self.labelkmph.place(y = 90, x = 350)
        
        self.closeButton = tkinter.Button(self.framelabelsR, text = "X", command = self.root.destroy, bg = background2)
        self.closeButton.pack(anchor = 'se')
        #Right frame ends
        self.root.after(200, _thread.start_new_thread, self.GetTemp, ())
        self.root.after(200, _thread.start_new_thread, self.videoLoop, ())
        self.root.mainloop()
        
gui = Menu()
