import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from page_home import PageHome
from page_login import PageLogin

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # setting fullscreen attr
        # self.attributes('-fullscreen', True)

        #set window title
        self.title("TouchStone")
        
        # width/height
        width=1024
        height=600
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
        for F in (PageHome, PageLogin):
            frame = F(container, self)
            
            # initializing frame of the object from all pages respectively with for loop
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(PageLogin)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

'''
        frame = PageLogin(container, self)
        self.frames[PageLogin] = frame
        frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(PageLogin)
'''



if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()