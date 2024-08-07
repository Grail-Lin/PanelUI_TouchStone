
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar
from GradientFrame import GradientFrame                       # add for gradient color background

import page_home
import coutil

import platform

if platform.system() == "Windows":
    import win_popup_kb as popup_kb
else:
    import linux_popup_kb as popup_kb

from copic import img_entry_bg, img_button_login_off, img_button_login_on, img_logo
from copic import img_keyboard

class PageLogin(Frame):

    # user data
    uname_input = ""
    pwd_input = ""
    value_vk_on = False


    #OUTPUT_PATH = Path(__file__).parent
    #ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame_login")

    #def relative_to_assets(self, path: str) -> Path:
    #    return self.ASSETS_PATH / Path(path)

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # set user data
        self.uname_input = StringVar(self, "ENTER USER NAME")
        self.pwd_input = StringVar(self, "ENTER PASSWORD")

        # set window size
        width = 1024
        height = 600

        screenwidth = controller.winfo_screenwidth()
        screenheight = controller.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        controller.geometry(alignstr)
        controller.resizable(width=False, height=False)

        # gradient background
        self.canvas = GradientFrame(self, colors = ("white", "#F0F0F0"), width = 1024, height = 600)
        self.canvas.config(direction = self.canvas.top2bottom)
        self.canvas.grid(row = 0, column = 0, sticky = "nsew")
        
        # flat background
        #self.canvas = Canvas(
        #    self,
        #    bg = "#FFFFFF",
        #    height = 600,
        #    width = 1024,
        #    bd = 0,
        #    highlightthickness = 0,
        #    relief = "ridge"
        #)
        #self.canvas.place(x = 0, y = 0)


        # self.entry_image_1 = PhotoImage(
        #     file=self.relative_to_assets("entry_1.png"))
        self.img_entry_bg = PhotoImage(data=img_entry_bg)

        self.entry_bg_1 = self.canvas.create_image(
            525.0,
            214.0,
            image=self.img_entry_bg
        )


        self.entry_1 = Entry(self,
            bd=0,
            bg="#EAEAEA",
            fg="#7E8DA8", # "#17171B",
            highlightthickness=0,
            font = ("Noto Sans", 24 * -1),
            textvariable = self.uname_input
        )

        self.entry_1.place(
            x=217.0,
            y=171.0,
            width=330,
            height=84.0
        )
        self.entry_1.bind("<1>", self.Focus_entry_uname)

        #self.entry_image_2 = PhotoImage(
        #    file=self.relative_to_assets("entry_1.png"))
        self.entry_bg_2 = self.canvas.create_image(
            525.0,
            327.0,
            image=self.img_entry_bg
        )
        self.entry_2 = Entry(self,
            bd=0,
            bg="#EAEAEA",
            fg="#7E8DA8", # "#17171B",
            #show="*",
            highlightthickness=0,
            font = ("Noto Sans", 24 * -1),
            textvariable = self.pwd_input
        )


        self.entry_2.place(
            x=217.0,
            y=284.0,
            width=330,
            height=84.0
        )
        self.entry_2.bind("<1>", self.Focus_entry_pwd)
        self.entry_2.bind("<FocusIn>", self.Focus_entry_pwd)


        self.error_password = self.canvas.create_text(
            830.0,
            303.0,
            anchor="ne",
            text="Password Error",
            fill="#F02C95",
            font=("Noto Sans", 24 * -1)
        )


        self.error_username = self.canvas.create_text(
            830.0,
            190.0,
            anchor="ne",
            text="No Account",
            fill="#F02C95",
            font=("Noto Sans", 24 * -1)
        )

        self.canvas.itemconfigure(self.error_password, state="hidden")
        self.canvas.itemconfigure(self.error_username, state="hidden")

        #self.image_image_1 = PhotoImage(
        #    file=self.relative_to_assets("image_1.png"))

        self.img_logo = PhotoImage(data=img_logo)
		
        self.image_logo = self.canvas.create_image(
            525.0,
            93.0,
            image=self.img_logo
        )

        #self.button_image_1 = PhotoImage(
        #    file=self.relative_to_assets("button_1.png"))
        #self.button_image_1_click = PhotoImage(
        #    file=self.relative_to_assets("button_1_click.png"))
        self.img_button_login_off = PhotoImage(data=img_button_login_off)
        self.img_button_login_on = PhotoImage(data=img_button_login_on)
        self.img_keyboard = PhotoImage(data=img_keyboard)

        self.btn_keyboard = Button(self, 
            image=self.img_keyboard, borderwidth = 0, highlightthickness=0,
            command = self.Cmd_btn_keyboard,
            relief="flat",
            font=("Noto San", 24*-1)
        )

        self.btn_keyboard.place(y=397.0, x=867, width=96.0, height=86.0)

        self.button_1 = Button(self,
            image=self.img_button_login_off,
            borderwidth=0,
            highlightthickness=0,
            command=0, #lambda: print("button_1 clicked"),
            relief="flat",
            font=("Noto Sans", 24 * -1),
        )

        self.button_1.place(
            y=397.0,
            x=185.0,
            width=680.0,
            height=86.0
        )

        #self.button_1['state']="disabled"
        


    def Cmd_btn_login(self):
        # change login btn image
        #self.button_1['state']="disabled"
        self.button_1['image']=self.img_button_login_off
        self.button_1['command']=0

        # close kb
        if self.value_vk_on == True:
            self.value_vk_on = False
            popup_kb.popup_keyboard(self)


        # get uname and pwd
        uname = self.uname_input.get()
        pwd = self.pwd_input.get()

        if uname == "":
            self.canvas.itemconfigure(self.error_username, state="normal")
        elif pwd == "":
            self.canvas.itemconfigure(self.error_password, state="normal")
        else:
            cosql = coutil.COSQLite('data.db')
        
            if cosql.queryLogin(uname, pwd):
                self.controller.show_frame(page_home.PageHome)
            else:
                if cosql.queryUser(uname):
                    # username exists, password wrong
                    self.canvas.itemconfigure(self.error_username, state="hidden")
                    self.canvas.itemconfigure(self.error_password, state="normal")
                else:
                    # username not exist, password unknown
                    self.canvas.itemconfigure(self.error_username, state="normal")
                    self.canvas.itemconfigure(self.error_password, state="hidden")

    def Focus_entry_uname(self, event):
        # clear uname
        self.uname_input.set("")
        # change font color
        self.entry_1['fg']="#17171B"
        # change login btn image
        #self.button_1['state']="normal"
        self.button_1['image']=self.img_button_login_on
        self.button_1['command']=self.Cmd_btn_login

        #if self.value_vk_on == False:
        #    self.value_vk_on = True
        #    win_popup_kb.popup_keyboard(self)
        #win_popup_kb.popup_keyboard(self)



    def Focus_entry_pwd(self, event):
        # clear pwd
        self.pwd_input.set("")
        # change font color
        self.entry_2['fg']="#17171B"
        self.entry_2['show']="*"
        # change login btn image
        #self.button_1['state']="normal"
        self.button_1['image']=self.img_button_login_on
        self.button_1['command']=self.Cmd_btn_login
        #if self.value_vk_on == False:
        #    self.value_vk_on = True
        #    win_popup_kb.popup_keyboard(self)
        #win_popup_kb.popup_keyboard(self)

    def Cmd_btn_keyboard(self):
        popup_kb.popup_keyboard(self)
        return



if __name__ == "__main__":
    window = Tk()
    window.geometry("1024x600")
    window.configure(bg = "#FFFFFF")

    container = Frame(window, bg="#FFFFBB")
    container.pack(side = "top", fill = "both", expand = True)
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)

    window.frames = {}
    frame = PageLogin(container, window)
    frame.grid(row = 0, column = 0, sticky ="nsew")

    window.frames[PageLogin] = frame
    frame.tkraise()

    window.mainloop()
    
