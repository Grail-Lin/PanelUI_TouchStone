import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from page0 import StartPage
from page_menu import PageMenu
from page_system_configuration import PageSC
from page_sc_user_advanced import PageSCUserAdv

from page_calibration import PageCalibration
from page_sc_bluetooth import PageSCBluetooth
from page_sc_date import PageSCDate
from page_sc_time import PageSCTime
from page_sc_user_mode import PageSCUserMode
from page_userinfo import PageUserInfo
from page_sc_network import PageSCNetwork
from page_user_login import PageUserLogin

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # setting fullscreen attr
        # self.attributes('-fullscreen', True)

        #set window title
        self.title("Coherence Demo")
        
        # width/height
        width=1356
        height=787
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(alignstr)
        self.resizable(width=False, height=False)
        
        
        # creating a container
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        #initializing frames to an empty array
        self.frames = {}
        
        # iterating through a tuple consisting of the different page layouts
        for F in (StartPage, PageMenu, PageSC, PageSCUserAdv, PageCalibration, PageSCBluetooth, 
		          PageSCDate, PageSCTime, PageSCUserMode, PageUserInfo, PageSCNetwork, PageUserLogin):
            frame = F(container, self)
            
            # initializing frame of the object from all pages respectively with for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()