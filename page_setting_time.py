
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
#from GradientFrame import GradientFrame                       # add for gradient color background

from copic import img_button_setting_on, img_button_home_off, img_button_process_off
from copic import img_button_logout, img_button_result_off, img_button_settime_on, img_button_cancel_off
from copic import image_test_off, image_reset_off, image_user_off, image_time_on, img_entry_bg

class PageSettingTime(Frame):

    # user data
    '''
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame5")                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
	
	
    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    '''

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # set user data

        # set window size
        width = 1024
        height = 600

        screenwidth = controller.winfo_screenwidth()
        screenheight = controller.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        controller.geometry(alignstr)
        controller.resizable(width=False, height=False)


        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 600,
            width = 1024,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        
        self.canvas.place(x = 0, y = 0)

        # add elements here
        self.canvas.create_rectangle(120.0, 0.0, 904.0, 600.0,
            fill="#F9F9F9", outline="")

        self.img_button_setting_on = PhotoImage(data=img_button_setting_on)
        self.button_setting = Button(
            image=self.img_button_setting_on,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_setting.place(
            x=0.0,
            y=497.0,
            width=120.0,
            height=103.0
        )

        self.img_button_home_off = PhotoImage(data=img_button_home_off)
        self.button_home = Button(
            image=self.img_button_home_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_home.place(
            x=0.0,
            y=0.0,
            width=120.0,
            height=103.0
        )

        self.img_button_process_off = PhotoImage(data=img_button_process_off)
        self.button_process = Button(
            image=self.img_button_process_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_process.place(
            x=0.0,
            y=103.0,
            width=120.0,
            height=103.0
        )

        self.canvas.create_text(
            148.0,
            16.0,  # 24.0,
            anchor="nw",
            text="SETTINGS / TIME",
            fill="#569FCB",
            font=("Noto Sans", 32 * -1, "bold")
        )

        self.canvas.create_rectangle(
            904.0, 0.0, 1024.0, 600.0,
            fill="#E6EFF4",
            outline="")

        self.img_button_logout = PhotoImage(data = img_button_logout)
        self.button_logout = Button(self,
            image=self.img_button_logout,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_logout clicked"),
            relief="flat"
        )
        self.button_logout.place(
            x=904.0,
            y=497.0,
            width=120.0,
            height=103.0
        )

        self.img_button_result_off = PhotoImage(data = img_button_result_off)
        self.button_result = Button(self,
            image=self.img_button_result_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_logout clicked"), #self.Cmd_btn_result,
            bg="#FFFFFF",
            relief="flat"
        )
        self.button_result.place(
            x=0.0,
            y=206.0,
            width=120.0,
            height=103.0
        )

        self.image_time_on = PhotoImage(data=image_time_on)
        self.button_time = Button(
            image=self.image_time_on,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )

        self.button_time.place(
            x=904.0,
            y=103.0,
            width=121.0,
            height=103.0
        )

        self.image_user_off = PhotoImage(data=image_user_off)
        self.button_user = Button(
            image=self.image_user_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        self.button_user.place(
            x=904.0,
            y=0.0,
            width=121.0,
            height=103.0
        )

        self.image_reset_off = PhotoImage(data=image_reset_off)
        self.button_reset = Button(
            image=self.image_reset_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_8 clicked"),
            relief="flat"
        )
        self.button_reset.place(
            x=904.0,
            y=394.0,
            width=121.0,
            height=103.0
        )

        self.image_test_off = PhotoImage(data = image_test_off)
        self.button_test = Button(self,
            image=self.image_test_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("image_test_off clicked"),
            relief="flat"
        )
        self.button_test.place(
            x=904.4,
            y=206.0,
            width=120.0,
            height=103.0
        )

        self.img_button_settime_on = PhotoImage(data=img_button_settime_on)
        self.button_settime = Button(
            image=self.img_button_settime_on,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_10 clicked"),
            relief="flat"
        )
        self.button_settime.place(
            x=513.0,
            y=415.0,
            width=315.0,
            height=86.0
        )

        self.img_button_cancel_off = PhotoImage(data=img_button_cancel_off)
        self.button_cancel = Button(
            image=self.img_button_cancel_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_11 clicked"),
            relief="flat"
        )
        self.button_cancel.place(
            x=148.0,
            y=416.0,
            width=315.0,
            height=86.0
        )

        self.img_entry_bg = PhotoImage(data=img_entry_bg)

        '''
        self.entry_bg_1 = self.canvas.create_image(
            430.0,
            96.0,
            image=self.img_entry_bg
        )
        '''

        self.entry_1 = Entry(self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font = ("Noto Sans", 24 * -1),
            #textvariable = self.uname_input
        )

        self.entry_1.place(
            x=430.0,
            y=96.0,
            width=398.0,
            height=84.0
        )
        #self.entry_1.bind("<1>", self.Focus_entry_uname)

        '''
        self.entry_bg_2 = self.canvas.create_image(
            430.0,
            196.0,
            image=self.img_entry_bg
        )
        '''

        self.entry_2 = Entry(self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font = ("Noto Sans", 24 * -1),
            #textvariable = self.uname_input
        )

        self.entry_2.place(
            x=430.0,
            y=196.0,
            width=398.0,
            height=84.0
        )
        #self.entry_2.bind("<1>", self.Focus_entry_uname)

        self.canvas.create_text(
            148.0, 128.0,
            anchor="nw",
            text="DATE",
            fill="#7D8CA7",
            font=("Noto Sans", 24 * -1)
        )

        self.canvas.create_text(
            148.0, 229.0,
            anchor="nw",
            text="TIME",
            fill="#7D8CA7",
            font=("Noto Sans", 24 * -1)
        )


if __name__ == "__main__":
    window = Tk()
    window.geometry("1024x600")
    window.configure(bg = "#FFFFFF")

    container = Frame(window, bg="#FFFFFF")
    container.pack(side = "top", fill = "both", expand = True)
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)

    window.frames = {}
    frame = PageSettingTime(container, window)

    window.frames[PageSettingTime] = frame
    frame.grid(row = 0, column = 0, sticky ="nsew")

    frame.tkraise()
    window.mainloop()
    