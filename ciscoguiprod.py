
#!/usr/bin/env python3
# TO DO:
#      A.  Turn on and off TV's from screens menu or switch to alternate inputs
#      B.  Create a single function for presets for the PC PTZ camera
#      C.  Test for ttyUSB0-5 to see if each device is correctly assigned in Linux.  Test at least to be sure each item returns the correct type of device info query results
#

import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import messagebox
import serial
import time
import os
import sys

# /usr/local/lib/python3.4/dist-packages/visca/
from visca import camera

# create the camera object to control the sony camera via visca
cam = camera.D100(output='/dev/sonyCAM')

# create the serial connection for the Polycom system
polycomcam = serial.Serial(port='/dev/polycomCAM',baudrate = 115200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)

cam.init()

# create the serial connections for the various screens to be turned and off
# udev rules set to symlink the usb ports 
centerscreen = serial.Serial(baudrate = 9600,port = '/dev/screenCenter',parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
screenright = serial.Serial(baudrate = 9600,port = '/dev/screenRight',parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
screenleft = serial.Serial(baudrate = 9600,port = '/dev/screenLeft',parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
screentopbottom = serial.Serial(baudrate = 9600,port = '/dev/screenTop',parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.subtitle_font = tkfont.Font(family='Helvetica', size=14, weight="bold")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")
        self.title("Cisco Room Controller")
        
        # open the window up to a specific size
        # self.update_idletasks()
        # width = 1024
        # height = 600
        # x = (self.winfo_screenwidth() // 2 ) - (width // 2)
        # y = (self.winfo_screenheight() // 2 ) - (height // 2)
        # self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        self.attributes("-fullscreen", True)
        container.pack(side="top", fill="both", expand=True)
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.grid_rowconfigure(3, weight=1)
        container.grid_columnconfigure(3, weight=1)

        self.frames = {}
        for F in (StartPage, Cisco, PC, Polycom, PolycomCamera, PolycomCameraControls, Camera, CameraControls):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def show_frame_cisco(self):
        '''Show the Cisco menu'''
        data2=bytearray(b'OUTPUT01 02;')
        Now=centerscreen.write(data2)
        Now2=screenright.write(data2)
        Now3=screenleft.write(data2)
        Now4=screentopbottom.write(data2)
        frame = self.frames['Cisco']
        frame.tkraise()

    def show_frame_pc(self):
        '''Show the Desktop menu'''
        data2=bytearray(b'OUTPUT01 01;')
        Now=centerscreen.write(data2)
        Now2=screenright.write(data2)
        Now3=screenleft.write(data2)
        Now4=screentopbottom.write(data2)
        frame = self.frames['PC']
        frame.tkraise()

    def show_frame_polycom(self):
        '''Show the Polycom menu'''
        data2=bytearray(b'OUTPUT01 03;')
        Now=centerscreen.write(data2)
        Now2=screenright.write(data2)
        Now3=screenleft.write(data2)
        Now4=screentopbottom.write(data2)
        frame = self.frames['Polycom']
        frame.tkraise()

    def show_screen1_pc(self):
        data2=bytearray(b'OUTPUT01 01;')
        now=screenleft.write(data2)

    def show_screen3_pc(self):
        data2=bytearray(b'OUTPUT01 01;')
        now3=centerscreen.write(data2)
        
    def show_screen4_pc(self):
        data2=bytearray(b'OUTPUT01 01;')
        now3=screentopbottom.write(data2)

    def show_frame_polycomcamera(self):
        '''Show the camera'''
        frame = self.frames['PolycomCamera']
        frame.tkraise()

    def show_frame_polycomcameracontrols(self):
        '''Show the camera'''
        frame = self.frames['PolycomCameraControls']
        frame.tkraise()

    def show_frame_camera(self):
        '''Show the camera'''
        frame = self.frames['Camera']
        frame.tkraise()
        
    def show_frame_cameracontrols(self):
        '''Show the camera'''
        frame = self.frames['CameraControls']
        frame.tkraise()

    def camera_preset_one(self):
        cam.preset_one()
        cam.autofocus_sens_high()
        cam.autofocus()

    def camera_preset_two(self):
        cam.preset_two()
        cam.autofocus_sens_high()
        cam.autofocus()

    def camera_preset_three(self):
        cam.preset_three()
        cam.autofocus_sens_high()
        cam.autofocus()

    def camera_preset_four(self):
        cam.preset_four()
        cam.autofocus_sens_high()
        cam.autofocus()

    def camera_preset_five(self):
        cam.preset_five()
        cam.autofocus_sens_high()
        cam.autofocus()

    def camera_preset_six(self):
        cam.preset_six()
        cam.autofocus_sens_high()
        cam.autofocus()

    def camera_left_up(self,pan,tilt):
        cam.left_up(pan,tilt)
        cam.stop()

    def camera_up(self):
        cam.up()

    def camera_down(self):
        cam.down()

    def camera_left(self):
        cam.left()

    def camera_right(self):
        cam.right()

    def camera_home(self):
        cam.home()
        
    def camera_upright(self):
        cam.right_up(5,5)
    
    def camera_downright(self):
        cam.right_down(5,5)
        
    def camera_upleft(self):
        cam.left_up(5,5)
        
    def camera_downleft(self):
        cam.left_down(5,5)

    def camera_set_preset(self,presetnum):
        cam.set_preset(presetnum)

    def camera_zoom_standard(self):
        cam.zoom_tele_standard()
        
    def camera_zoom_wide(self):
        cam.zoom_tele_wide()

    def camera_stop(self):
        cam.stop()
        cam.stop_zoom()

    def camera_zoom_3x(self):
        cam.zoom_3x()

    def exit_program(self):
        self.destroy()
        
    # Polycom Camera commands
    def pc_camera_goto_preset(self,presetnum):
        preset = presetnum
        data11 = "preset near go {}\r".format(preset)
        No = polycomcam.write(data11.encode())
      
    def pc_camera_up(self):
        data7 = "camera near move up\r"
        No = polycomcam.write(data7.encode())

    def pc_camera_down(self):
        data8 = "camera near move down\r"
        No = polycomcam.write(data8.encode())

    def pc_camera_left(self):
        data9 = "camera near move left\r"
        No = polycomcam.write(data9.encode())

    def pc_camera_right(self):
        data10 = "camera near move right\r"
        No = polycomcam.write(data10.encode())
    
    def pc_camera_home(self):
        cam.home()
        
    def pc_camera_upright(self):
        data10 = "camera near move right\r"
        No = polycomcam.write(data10.encode())
        data7 = "camera near move up\r"
        No = polycomcam.write(data7.encode())
    
    def pc_camera_downright(self):
        cam.right_down(5,5)
        
    def pc_camera_upleft(self):
        cam.left_up(5,5)
        
    def pc_camera_downleft(self):
        cam.left_down(5,5)

    def pc_camera_set_preset(self,presetnum):
        preset = presetnum
        data11 = "preset near set {}\r".format(preset)
        No = polycomcam.write(data11.encode())

    def pc_camera_zoom_standard(self):
        data12 = "camera near move zoom+\r"
        No = polycomcam.write(data12.encode())
         
    def pc_camera_zoom_wide(self):
        data13 = "camera near move zoom-\r"
        No = polycomcam.write(data13.encode())
        
    def pc_camera_stop(self):
        data14 = "camera near stop\r"
        No = polycomcam.write(data14.encode())

    def restart(self):
        result = messagebox.askyesno("Restart", "Are you sure?")
        if result == True:
            python3 = sys.executable
            os.execl(python3, python3, * sys.argv)
            #command = "/usr/bin/sudo /sbin/shutdown -r now"
            #import subprocess
            #process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            #output = process.communicate()[0]
  
      
class StartPage(tk.Frame):
    # Make this the 3 system choice menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)         
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)         
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)  

        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="assets/CISCO.gif")
        photo2 = tk.PhotoImage(file="assets/PCvideoconferencing.gif")
        photo3 = tk.PhotoImage(file="assets/Polycom.gif")
        photo4 = tk.PhotoImage(file="assets/restart.gif")

        # create the image button, image is above (top) the optional text
        button1 = tk.Button(self, width=256, height=266, image=photo1, borderwidth=0,
                            text="Cisco TelePresence", command=lambda: controller.show_frame_cisco())
        button2 = tk.Button(self, width=256, height=266, image=photo2,borderwidth=0,
                            text="PC Video conferencing", command=lambda: controller.show_frame_pc())
        button3 = tk.Button(self, width=256, height=266, image=photo3,borderwidth=0,
                            text="Polycom", command=lambda: controller.show_frame_polycom())
        button4 = tk.Button(self, width=64, height=64, image=photo4, borderwidth=0,text="Restart", command=lambda: controller.restart())

        button1.grid(row=1,column=2)
        button2.grid(row=1,column=3)
        button3.grid(row=1,column=4)
        button4.grid(row=2,column=3)

        button1.image = photo1
        button2.image = photo2
        button3.image = photo3
        button4.image = photo4


class Cisco(tk.Frame):
    # Make this the Cisco Screen selector
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)         
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)         
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)  
        

        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="assets/TV.gif")
        photo2 = tk.PhotoImage(file="assets/TVOff.gif")
        photo3 = tk.PhotoImage(file="assets/mediaTV.gif")

        label = tk.Label(self, text="Cisco", font=controller.title_font)
        label.grid(row=1,column=3)


        # create the image button
        button1 = tk.Button(self, width=257, height=165, image=photo1,borderwidth=0,
                            text="LCD 1", command=lambda: controller.show_frame("Cisco"))

        button2 = tk.Button(self, width=257, height=165, image=photo1,borderwidth=0,
                            text="LCD 2", command=lambda: controller.show_frame("Cisco"))

        button3 = tk.Button(self, width=257, height=165, image=photo1,borderwidth=0,
                            text="LCD 3", command=lambda: controller.show_frame("Cisco"))

        button4 = tk.Button(self, width=257, height=165, image=photo3,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_screen4_pc())

        button5 = tk.Button(self, width=257, height=165, image=photo3,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_frame("Cisco"))

        button6 = tk.Button(self, width=257, height=165, image=photo3,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_frame("Cisco"))


        button1.grid(row=2,column=2)
        button2.grid(row=2,column=3)
        button3.grid(row=2,column=4)
        button4.grid(row=1,column=2)
        button5.grid(row=1,column=4)
        button6.grid(row=3,column=3)

        button1.image = photo1
        button2.image = photo1
        button3.image = photo1
        button4.image = photo3
        button5.image = photo3
        button6.image = photo3

        button = tk.Button(self, text="Main Menu",command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3, column=2)



class PC(tk.Frame):
    # Make this the PC Screen selector
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)         
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)         
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)  
        
        
        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="assets/screen1TV.gif")
        photo2 = tk.PhotoImage(file="assets/screen2TV.gif")
        photo3 = tk.PhotoImage(file="assets/screen3TV.gif")
        photo4 = tk.PhotoImage(file="assets/screen4TV.gif")

        label = tk.Label(self, text="PC", font=controller.title_font)
        label.grid(row=1,column=3)


        # create the image button
        button1 = tk.Button(self, width=257, height=165, image=photo1,borderwidth=0,
                            text="LCD 1", command=lambda: controller.show_frame("PC"))

        button2 = tk.Button(self, width=257, height=165, image=photo2,borderwidth=0,
                            text="LCD 2", command=lambda: controller.show_frame("PC"))

        button3 = tk.Button(self, width=257, height=165, image=photo3,borderwidth=0,
                            text="LCD 3", command=lambda: controller.show_frame("PC"))

        button4 = tk.Button(self, width=257, height=165, image=photo4,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_frame("PC"))

        button5 = tk.Button(self, width=257, height=165, image=photo4,borderwidth=0,
                            text="LCD 4", command=lambda: controller.camera_zoom_3x())

        button6 = tk.Button(self, width=257, height=165, image=photo4,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_frame("PC"))

        button1.grid(row=2,column=2)
        button2.grid(row=2,column=3)
        button3.grid(row=2,column=4)
        button4.grid(row=1,column=2)
        button5.grid(row=1,column=4)
        button6.grid(row=3,column=3)

        button1.image = photo1
        button2.image = photo2
        button3.image = photo3
        button4.image = photo4
        button5.image = photo4
        button6.image = photo4

        button = tk.Button(self, text="Main Menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3, column=2, ipadx=(10), ipady=(10))

        button = tk.Button(self, text="Camera Controller",
                           command=lambda: controller.show_frame("Camera"))
        button.grid(row=3, column=4, ipadx=(10), ipady=(10))


class Polycom(tk.Frame):
    # Make this the Polycom Screen selector
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)         
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)         
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)  
        
        
        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="assets/localcameraTV.gif")
        photo2 = tk.PhotoImage(file="assets/TVOff.gif")
        photo3 = tk.PhotoImage(file="assets/remotecameraTV.gif")
        
        
        label = tk.Label(self, text="Polycom", font=controller.title_font)
        label.grid(row=1,column=3)


        # create the image button
        button1 = tk.Button(self, width=257, height=165, image=photo2,borderwidth=0,
                            text="LCD 1", command=lambda: controller.show_screen1_pc())

        button2 = tk.Button(self, width=257, height=165, image=photo3,borderwidth=0,
                            text="LCD 2", command=lambda: controller.show_frame("Polycom"))

        # displays the PC on screen 3 while in a polycom call
        button3 = tk.Button(self, width=257, height=165, image=photo2,borderwidth=0,
                            text="LCD 3", command=lambda: controller.show_screen3_pc())

        button4 = tk.Button(self, width=257, height=165, image=photo1,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_frame("Polycom"))

        button5 = tk.Button(self, width=257, height=165, image=photo1,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_frame("Polycom"))

        button6 = tk.Button(self, width=257, height=165, image=photo1,borderwidth=0,
                            text="LCD 4", command=lambda: controller.show_frame("Polycom"))


        button1.grid(row=2,column=2)
        button2.grid(row=2,column=3)
        button3.grid(row=2,column=4)
        button4.grid(row=1,column=2)
        button5.grid(row=1,column=4)
        button6.grid(row=3,column=3)

        button1.image = photo2
        button2.image = photo3
        button3.image = photo2
        button4.image = photo1
        button5.image = photo1
        button6.image = photo1

        button = tk.Button(self, text="Main Menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3, column=2, ipadx=(10), ipady=(10))
        button = tk.Button(self, text="Polycom Camera Controller",
                           command=lambda: controller.show_frame("PolycomCamera"))
        button.grid(row=3, column=4, ipadx=(10), ipady=(10))

class PolycomCamera(tk.Frame):
    # Make this the Camera Screen selector
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        photo0 = tk.PhotoImage(file="assets/presets.gif")
        

        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="assets/1.gif")
        photo2 = tk.PhotoImage(file="assets/2.gif")
        photo3 = tk.PhotoImage(file="assets/3.gif")
        photo4 = tk.PhotoImage(file="assets/4.gif") 
        photo5 = tk.PhotoImage(file="assets/5.gif")
        photo6 = tk.PhotoImage(file="assets/6.gif")
        photo7 = tk.PhotoImage(file="assets/7.gif")
        photo8 = tk.PhotoImage(file="assets/8.gif")
        photo9 = tk.PhotoImage(file="assets/9.gif")
        photo11 = tk.PhotoImage(file="assets/home.gif")


        label = tk.Label(self, text="Polycom Camera Controller", font=controller.title_font)
        label.grid(row=0,column=0,columnspan=7,pady=(30, 0))
        label = tk.Label(self, text="Camera presets", font=controller.subtitle_font)
        label.grid(row=2,column=0,columnspan=7,pady=(15))

        # create the image button
        button0 = tk.Button(self, width=456, height=456, image=photo0, borderwidth=0)
        button1 = tk.Button(self, width=128, height=128, image=photo1, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(1))
        button2 = tk.Button(self, width=128, height=128, image=photo2, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(2))
        button3 = tk.Button(self, width=128, height=128, image=photo3, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(3))
        button4 = tk.Button(self, width=128, height=128, image=photo4, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(4))
        button5 = tk.Button(self, width=128, height=128, image=photo5, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(5))
        button6 = tk.Button(self, width=128, height=128, image=photo6, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(6))

        button7 = tk.Button(self, width=128, height=128, image=photo7, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(7))
        button8 = tk.Button(self, width=128, height=128, image=photo8, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(8))
        button9 = tk.Button(self, width=128, height=128, image=photo9, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(9))
        #button11 = tk.Button(self, width=128, height=128, image=photo11, borderwidth=0,command=lambda: controller.pc_camera_home())

        # Layout the buttons
        button0.grid(row=3,column=3, columnspan=4, rowspan=3)
        button1.grid(row=3,column=0)
        button2.grid(row=3,column=1)
        button3.grid(row=3,column=2)
        button4.grid(row=4,column=0)
        button5.grid(row=4,column=1)
        button6.grid(row=4,column=2)
        button7.grid(row=5,column=0)
        button8.grid(row=5,column=1)
        button9.grid(row=5,column=2)
        #button11.grid(row=3,column=3)

        button0.image = photo0
        button1.image = photo1
        button2.image = photo2
        button3.image = photo3
        button4.image = photo4
        button5.image = photo5
        button6.image = photo6
        button7.image = photo7
        button8.image = photo8
        button9.image = photo9
        #button11.image = photo11

        button = tk.Button(self, text="Camera Controls", command=lambda: controller.show_frame("PolycomCameraControls"))
        button.grid(row=9, column=0, columnspan=7, padx=(100), pady=(20), ipadx=(10), ipady=(10))
        
        button = tk.Button(self, text="Back", command=lambda: controller.show_frame("Polycom"))
        button.grid(row=10, column=0, columnspan=7, ipadx=(10), ipady=(10))
        
                # create background image


class PolycomCameraControls(tk.Frame):
    # Make this the Camera Controls Screen selector
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)         
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)         
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)  

        # create background image
        #   background_image = tk.PhotoImage(file="assets/img13.gif")
        #   background_label = tk.Label(self, image=background_image)
        
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # background_label.grid(row=3, column=0, columnspan=6)

        photo1 = tk.PhotoImage(file="assets/pc_1.gif")
        photo2 = tk.PhotoImage(file="assets/pc_2.gif")
        photo3 = tk.PhotoImage(file="assets/pc_3.gif")
        photo4 = tk.PhotoImage(file="assets/pc_4.gif") 
        photo5 = tk.PhotoImage(file="assets/pc_5.gif")
        photo6 = tk.PhotoImage(file="assets/pc_6.gif")
        photo26 = tk.PhotoImage(file="assets/pc_7.gif")
        photo27 = tk.PhotoImage(file="assets/pc_8.gif")
        photo28 = tk.PhotoImage(file="assets/pc_9.gif")

        photo7 = tk.PhotoImage(file="assets/uparrow.gif")  
        photo8 = tk.PhotoImage(file="assets/down.gif")
        photo9 = tk.PhotoImage(file="assets/left.gif")
        photo10 = tk.PhotoImage(file="assets/right.gif")
        photo21 = tk.PhotoImage(file="assets/stoppantilt.gif")
        
        photo22 = tk.PhotoImage(file="assets/downright.gif") 
        photo23 = tk.PhotoImage(file="assets/downleft.gif")
        photo24 = tk.PhotoImage(file="assets/upright.gif")
        photo25 = tk.PhotoImage(file="assets/upleft.gif")

        photo18 = tk.PhotoImage(file="assets/zoomin.gif")
        photo19 = tk.PhotoImage(file="assets/zoomout.gif")


        label = tk.Label(self, text="Polycom Camera Controller", font=controller.title_font)
        label.grid(row=0,column=0,columnspan=7)
        label = tk.Label(self, text="Test presets", font=controller.subtitle_font)
        label.grid(row=4,column=0,columnspan=3)
        label = tk.Label(self, text="Set presets", font=controller.subtitle_font)
        label.grid(row=4,column=4,columnspan=3)

        # create the image button
        button1 = tk.Button(self, width=64, height=64, image=photo1, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(1))
        button2 = tk.Button(self, width=64, height=64, image=photo2, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(2))
        button3 = tk.Button(self, width=64, height=64, image=photo3, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(3))
        button4 = tk.Button(self, width=64, height=64, image=photo4, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(4))
        button5 = tk.Button(self, width=64, height=64, image=photo5, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(5))
        button6 = tk.Button(self, width=64, height=64, image=photo6, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(6))
        button26 = tk.Button(self, width=64, height=64, image=photo26, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(7))
        button27 = tk.Button(self, width=64, height=64, image=photo27, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(8))
        button28 = tk.Button(self, width=64, height=64, image=photo28, borderwidth=0,command=lambda: controller.pc_camera_goto_preset(9))


        button7 = tk.Button(self, width=64, height=64, image=photo7, borderwidth=0,command=lambda: controller.pc_camera_up()) 
        button8 = tk.Button(self, width=64, height=64, image=photo8, borderwidth=0,command=lambda: controller.pc_camera_down())
        button9 = tk.Button(self, width=64, height=64, image=photo9, borderwidth=0,command=lambda: controller.pc_camera_right())
        button10 = tk.Button(self, width=64, height=64, image=photo10, borderwidth=0,command=lambda: controller.pc_camera_left())
        
        button22 = tk.Button(self, width=64, height=64, image=photo22, borderwidth=0,command=lambda: controller.pc_camera_downleft()) 
        button23 = tk.Button(self, width=64, height=64, image=photo23, borderwidth=0,command=lambda: controller.pc_camera_downright())
        button24 = tk.Button(self, width=64, height=64, image=photo24, borderwidth=0,command=lambda: controller.pc_camera_upleft())
        button25 = tk.Button(self, width=64, height=64, image=photo25, borderwidth=0,command=lambda: controller.pc_camera_upright())
        

        button21 = tk.Button(self, width=96, height=96, image=photo21, borderwidth=0,command=lambda: controller.pc_camera_stop())   
       

        button18 = tk.Button(self, width=64, height=64, image=photo18, borderwidth=0,command=lambda: controller.pc_camera_zoom_standard())
        button19 = tk.Button(self, width=64, height=64, image=photo19, borderwidth=0,command=lambda: controller.pc_camera_zoom_wide())


        button12 = tk.Button(self, width=64, height=64, image=photo1, borderwidth=0,command=lambda: controller.pc_camera_set_preset(1))
        button13 = tk.Button(self, width=64, height=64, image=photo2, borderwidth=0,command=lambda: controller.pc_camera_set_preset(2))
        button14 = tk.Button(self, width=64, height=64, image=photo3, borderwidth=0,command=lambda: controller.pc_camera_set_preset(3))
        button15 = tk.Button(self, width=64, height=64, image=photo4, borderwidth=0,command=lambda: controller.pc_camera_set_preset(4))
        button16 = tk.Button(self, width=64, height=64, image=photo5, borderwidth=0,command=lambda: controller.pc_camera_set_preset(5))
        button17 = tk.Button(self, width=64, height=64, image=photo6, borderwidth=0,command=lambda: controller.pc_camera_set_preset(6))
        button29 = tk.Button(self, width=64, height=64, image=photo26, borderwidth=0,command=lambda: controller.pc_camera_set_preset(7))
        button30 = tk.Button(self, width=64, height=64, image=photo27, borderwidth=0,command=lambda: controller.pc_camera_set_preset(8))
        button31 = tk.Button(self, width=64, height=64, image=photo28, borderwidth=0,command=lambda: controller.pc_camera_set_preset(9))


        # Layout the buttons
        button1.grid(row=5,column=0)
        button2.grid(row=5,column=1)
        button3.grid(row=5,column=2)
        button4.grid(row=6,column=0)
        button5.grid(row=6,column=1)
        button6.grid(row=6,column=2)
        button26.grid(row=7,column=0)
        button27.grid(row=7,column=1)
        button28.grid(row=7,column=2)
        
        
        # Set presets buttons
        button12.grid(row=5,column=4)
        button13.grid(row=5,column=5)
        button14.grid(row=5,column=6)
        button15.grid(row=6,column=4)
        button16.grid(row=6,column=5)
        button17.grid(row=6,column=6)
        button29.grid(row=7,column=4)
        button30.grid(row=7,column=5)
        button31.grid(row=7,column=6)

        # Camera control buttons up,down,left,right,home
        button7.grid(row=1,column=3)
        button8.grid(row=3,column=3)
        button9.grid(row=2,column=1, sticky=tk.E)
        button10.grid(row=2,column=5, sticky=tk.W)

        button22.grid(row=3,column=4)
        button23.grid(row=3,column=2)
        button24.grid(row=1,column=4)
        button25.grid(row=1,column=2)

        button21.grid(row=2,column=3)   
        button18.grid(row=2, column=2)
        button19.grid(row=2, column=4)

        button1.image = photo1
        button2.image = photo2
        button3.image = photo3
        button4.image = photo4
        button5.image = photo5
        button6.image = photo6
        button26.image = photo26
        button27.image = photo27
        button28.image = photo28

        button7.image = photo7
        button8.image = photo8
        button9.image = photo9
        button10.image = photo10
       
        button18.image = photo18
        button19.image = photo19
        button21.image = photo21
        
        button22.image = photo22
        button23.image = photo23
        button24.image = photo24
        button25.image = photo25
        
        button12.image = photo1
        button13.image = photo2
        button14.image = photo3
        button15.image = photo4
        button16.image = photo5
        button17.image = photo6

        # background_label.image = background_image

        button = tk.Button(self, text="Back",command=lambda: controller.show_frame("PolycomCamera"))
        button.grid(row=8, column=0, columnspan=7)


class Camera(tk.Frame):
    # Make this the Camera Screen selector
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # create background image
        #   background_image = tk.PhotoImage(file="assets/img13.gif")
        #   background_label = tk.Label(self, image=background_image)
        
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #   background_label.grid(row=3, column=0, columnspan=6)

        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="assets/1.gif")
        photo2 = tk.PhotoImage(file="assets/2.gif")
        photo3 = tk.PhotoImage(file="assets/3.gif")
        photo4 = tk.PhotoImage(file="assets/4.gif") 
        photo5 = tk.PhotoImage(file="assets/5.gif")
        photo6 = tk.PhotoImage(file="assets/6.gif")
        photo11 = tk.PhotoImage(file="assets/home.gif")

        label = tk.Label(self, text="Camera Controller", font=controller.title_font)
        label.grid(row=0,column=0,columnspan=7,pady=(30, 0))
        label = tk.Label(self, text="Camera presets", font=controller.subtitle_font)
        label.grid(row=2,column=0,columnspan=7,pady=(15))

        # create the image button
        button1 = tk.Button(self, width=128, height=128, image=photo1, borderwidth=0,command=lambda: controller.camera_preset_one())
        button2 = tk.Button(self, width=128, height=128, image=photo2, borderwidth=0,command=lambda: controller.camera_preset_two())
        button3 = tk.Button(self, width=128, height=128, image=photo3, borderwidth=0,command=lambda: controller.camera_preset_three())
        button4 = tk.Button(self, width=128, height=128, image=photo4, borderwidth=0,command=lambda: controller.camera_preset_four())
        button5 = tk.Button(self, width=128, height=128, image=photo5, borderwidth=0,command=lambda: controller.camera_preset_five())
        button6 = tk.Button(self, width=128, height=128, image=photo6, borderwidth=0,command=lambda: controller.camera_preset_six())
        button11 = tk.Button(self, width=128, height=128, image=photo11, borderwidth=0,command=lambda: controller.camera_home())

        # Layout the buttons
        button1.grid(row=3,column=0)
        button2.grid(row=3,column=1)
        button3.grid(row=3,column=2)
        button4.grid(row=3,column=4)
        button5.grid(row=3,column=5)
        button6.grid(row=3,column=6)
        button11.grid(row=3,column=3)

        button1.image = photo1
        button2.image = photo2
        button3.image = photo3
        button4.image = photo4
        button5.image = photo5
        button6.image = photo6
        button11.image = photo11

        # background_label.image = background_image

        button = tk.Button(self, text="Camera Controls", command=lambda: controller.show_frame("CameraControls"))
        button.grid(row=9, column=0, columnspan=7, padx=(100), pady=(20), ipadx=(10), ipady=(10))
        
        button = tk.Button(self, text="Back", command=lambda: controller.show_frame("PC"))
        button.grid(row=10, column=0, columnspan=7, ipadx=(10), ipady=(10))


class CameraControls(tk.Frame):
    # Make this the Camera Controls Screen selector
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # create background image
        #   background_image = tk.PhotoImage(file="assets/img13.gif")
        #   background_label = tk.Label(self, image=background_image)
        
        # background_label.place(x=0, y=0, relwidth=1, relheight=1)
        #   background_label.grid(row=3, column=0, columnspan=6)

        # pick a (small) image file you have in the working directory ...
        photo1 = tk.PhotoImage(file="assets/1.gif")
        photo2 = tk.PhotoImage(file="assets/2.gif")
        photo3 = tk.PhotoImage(file="assets/3.gif")
        photo4 = tk.PhotoImage(file="assets/4.gif") 
        photo5 = tk.PhotoImage(file="assets/5.gif")
        photo6 = tk.PhotoImage(file="assets/6.gif")

        photo7 = tk.PhotoImage(file="assets/uparrow.gif")  
        photo8 = tk.PhotoImage(file="assets/down.gif")
        photo9 = tk.PhotoImage(file="assets/left.gif")
        photo10 = tk.PhotoImage(file="assets/right.gif")
        # photo11 = tk.PhotoImage(file="assets/home.gif")
        photo21 = tk.PhotoImage(file="assets/stoppantilt.gif")
        
        photo22 = tk.PhotoImage(file="assets/downright.gif") 
        photo23 = tk.PhotoImage(file="assets/downleft.gif")
        photo24 = tk.PhotoImage(file="assets/upright.gif")
        photo25 = tk.PhotoImage(file="assets/upleft.gif")

        photo18 = tk.PhotoImage(file="assets/zoomin.gif")
        photo19 = tk.PhotoImage(file="assets/zoomout.gif")

        label = tk.Label(self, text="PC Camera Controller", font=controller.title_font)
        label.grid(row=0,column=0,columnspan=7)
        label = tk.Label(self, text="Test presets", font=controller.subtitle_font)
        label.grid(row=4,column=0,columnspan=3)
        label = tk.Label(self, text="Set presets", font=controller.subtitle_font)
        label.grid(row=4,column=4,columnspan=3)

        # create the image button
        button1 = tk.Button(self, width=128, height=128, image=photo1, borderwidth=0,command=lambda: controller.camera_preset_one())
        button2 = tk.Button(self, width=128, height=128, image=photo2, borderwidth=0,command=lambda: controller.camera_preset_two())
        button3 = tk.Button(self, width=128, height=128, image=photo3, borderwidth=0,command=lambda: controller.camera_preset_three())
        button4 = tk.Button(self, width=128, height=128, image=photo4, borderwidth=0,command=lambda: controller.camera_preset_four())
        button5 = tk.Button(self, width=128, height=128, image=photo5, borderwidth=0,command=lambda: controller.camera_preset_five())
        button6 = tk.Button(self, width=128, height=128, image=photo6, borderwidth=0,command=lambda: controller.camera_preset_six())

        button7 = tk.Button(self, width=64, height=64, image=photo7, borderwidth=0,command=lambda: controller.camera_up()) 
        button8 = tk.Button(self, width=64, height=64, image=photo8, borderwidth=0,command=lambda: controller.camera_down())
        button9 = tk.Button(self, width=64, height=64, image=photo9, borderwidth=0,command=lambda: controller.camera_right())
        button10 = tk.Button(self, width=64, height=64, image=photo10, borderwidth=0,command=lambda: controller.camera_left())
        
        button22 = tk.Button(self, width=64, height=64, image=photo22, borderwidth=0,command=lambda: controller.camera_downleft()) 
        button23 = tk.Button(self, width=64, height=64, image=photo23, borderwidth=0,command=lambda: controller.camera_downright())
        button24 = tk.Button(self, width=64, height=64, image=photo24, borderwidth=0,command=lambda: controller.camera_upleft())
        button25 = tk.Button(self, width=64, height=64, image=photo25, borderwidth=0,command=lambda: controller.camera_upright())
        
        button21 = tk.Button(self, width=96, height=96, image=photo21, borderwidth=0,command=lambda: controller.camera_stop())   
    
        button18 = tk.Button(self, width=64, height=64, image=photo18, borderwidth=0,command=lambda: controller.camera_zoom_standard())
        button19 = tk.Button(self, width=64, height=64, image=photo19, borderwidth=0,command=lambda: controller.camera_zoom_wide())

        button12 = tk.Button(self, width=128, height=128, image=photo1, borderwidth=0,command=lambda: controller.camera_set_preset(0))
        button13 = tk.Button(self, width=128, height=128, image=photo2, borderwidth=0,command=lambda: controller.camera_set_preset(1))
        button14 = tk.Button(self, width=128, height=128, image=photo3, borderwidth=0,command=lambda: controller.camera_set_preset(2))
        button15 = tk.Button(self, width=128, height=128, image=photo4, borderwidth=0,command=lambda: controller.camera_set_preset(3))
        button16 = tk.Button(self, width=128, height=128, image=photo5, borderwidth=0,command=lambda: controller.camera_set_preset(4))
        button17 = tk.Button(self, width=128, height=128, image=photo6, borderwidth=0,command=lambda: controller.camera_set_preset(5))

        # Layout the buttons
        button1.grid(row=5,column=0)
        button2.grid(row=5,column=1)
        button3.grid(row=5,column=2)
        button4.grid(row=6,column=0)
        button5.grid(row=6,column=1)
        button6.grid(row=6,column=2)
        
        # Set presets buttons
        button12.grid(row=5,column=4)
        button13.grid(row=5,column=5)
        button14.grid(row=5,column=6)
        button15.grid(row=6,column=4)
        button16.grid(row=6,column=5)
        button17.grid(row=6,column=6)

        # Camera control buttons up,down,left,right,home
        button7.grid(row=1,column=3)
        button8.grid(row=3,column=3)
        button9.grid(row=2,column=1, sticky=tk.E)
        button10.grid(row=2,column=5, sticky=tk.W)

        button22.grid(row=3,column=4)
        button23.grid(row=3,column=2)
        button24.grid(row=1,column=4)
        button25.grid(row=1,column=2)

        # button11.grid(row=6,column=2,columnspan=2)
        button21.grid(row=2,column=3)   

        button18.grid(row=2, column=2)
        button19.grid(row=2, column=4)

        button1.image = photo1
        button2.image = photo2
        button3.image = photo3
        button4.image = photo4
        button5.image = photo5
        button6.image = photo6

        button7.image = photo7
        button8.image = photo8
        button9.image = photo9
        button10.image = photo10
        # button11.image = photo11
        button18.image = photo18
        button19.image = photo19
        button21.image = photo21
        
        button22.image = photo22
        button23.image = photo23
        button24.image = photo24
        button25.image = photo25
        
        button12.image = photo1
        button13.image = photo2
        button14.image = photo3
        button15.image = photo4
        button16.image = photo5
        button17.image = photo6

        # background_label.image = background_image

        button = tk.Button(self, text="Back",
                           command=lambda: controller.show_frame("Camera"))
        button.grid(row=7, column=0, columnspan=7)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
