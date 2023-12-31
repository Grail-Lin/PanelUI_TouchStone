
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar

import random, string, time

import page_process_play
import page_home
import page_process_edit
import page_result_list
import page_setting

from copic import img_button_process_off, img_button_home_off, img_button_result_off, img_button_setting_on
from copic import img_button_insert_on, img_button_insert_off
from copic import img_button_eject_on, img_button_eject_off
from copic import img_state_aborted, img_state_completed, img_state_not_started
from copic import img_btn_start_off, img_btn_start_on

from copic import image_test_on, image_reset_off, image_user_off, image_time_off, img_button_logout

class PageSettingSelftest(Frame):


    # process status
    # 0: not started, no cartridge
    # 1: completed
    # -1: error
    # 2: not started, with cartridge

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
        self.canvas.create_rectangle(120.0, 0.0, 904.0, 600.0, fill="#F9F9F9", outline="")

        self.button_image_setting_on = PhotoImage(data=img_button_setting_on)
        self.button_setting = Button(self, image=self.button_image_setting_on, 
                                     borderwidth=0, highlightthickness=0,
                                     command=self.Cmd_btn_setting,
                                     relief="flat")
        self.button_setting.place(x=0.0, y=497.0, width=120.0, height=103.0)

        self.button_image_home_off = PhotoImage(data=img_button_home_off)
        self.button_home = Button(self, image=self.button_image_home_off,
                                  borderwidth=0, highlightthickness=0,
                                  command=self.Cmd_btn_home,
                                  relief="flat")
        self.button_home.place(x=0.0, y=0.0, width=120.0, height=103.0)

        self.button_image_process_off = PhotoImage(data=img_button_process_off)
        self.button_process = Button(self, image=self.button_image_process_off,
                                     borderwidth=0, highlightthickness=0,
                                     command=lambda: print("button_1 clicked"),
                                     relief="flat")
        self.button_process.place(x=0.0, y=103.0, width=120.0, height=103.0)

        self.canvas.create_text(
            148.0,
            24.0,
            anchor="nw",
            text="SETTINGS / SELF-TEST",
            fill="#569FCB",
            font=("Noto Sans", 32 * -1, "bold")
        )

        self.canvas.create_rectangle(
            904.0, 0.0,
            1024.0, 600.0,
            fill="#E6EFF4",
            outline="")


        self.button_image_result_off = PhotoImage(data=img_button_result_off)
        self.button_result = Button(self, image=self.button_image_result_off,
                                    borderwidth=0, highlightthickness=0,
                                    command=self.Cmd_btn_result,
                                    relief="flat")
        self.button_result.place(x=0.0, y=206.0, width=120.0, height=103.0)

        # button: user, time, test, reset, logout
        self.image_user_off = PhotoImage(data = image_user_off)
        self.button_user = Button(self,
            image=self.image_user_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("image_user_off clicked"),
            relief="flat"
        )
        self.button_user.place(
            x=904.0,
            y=0.0,
            width=120.0,
            height=103.0
        )

        self.image_time_off = PhotoImage(data = image_time_off)
        self.button_time = Button(self,
            image=self.image_time_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("image_time_off clicked"),
            relief="flat"
        )
        self.button_time.place(
            x=904.0,
            y=103.0,
            width=120.0,
            height=103.0
        )

        self.image_test_on = PhotoImage(data = image_test_on)
        self.button_test = Button(self,
            image=self.image_test_on,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("image_test_on clicked"),
            relief="flat"
        )
        self.button_test.place(
            x=904.4,
            y=206.0,
            width=120.0,
            height=103.0
        )

        self.image_reset_off = PhotoImage(data = image_reset_off)
        self.button_reset = Button(self,
            image=self.image_reset_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("image_reset_off clicked"),
            relief="flat"
        )
        self.button_reset.place(
            x=904.0,
            y=394.0,
            width=120.0,
            height=103.0
        )

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



        self.img_btn_start_off = PhotoImage(data=img_btn_start_off)
        self.button_start_01 = Button(self, image=self.img_btn_start_off,
                                      borderwidth=0, highlightthickness=0,
                                      command=lambda: print("button_10 clicked"),
                                      relief="flat")
        self.button_start_01.place(x=354.0, y=96.0, width=200.0, height=70.0)


        # button_11
        self.img_btn_start_on = PhotoImage(data=img_btn_start_on)
        self.button_start_02 = Button(self, image=self.img_btn_start_on,
                                      borderwidth=0, highlightthickness=0,
                                      command=lambda: print("button_11 clicked"),
                                      relief="flat")
        self.button_start_02.place(x=354.0, y=191.0, width=200.0, height=70.0)

        # fix labels
        self.canvas.create_text(
            148.0,
            113.0,
            anchor="nw",
            text="HEATER TEST",
            fill="#7D8CA7",
            font=("Noto Sans", 24 * -1)
        )

        self.canvas.create_text(
            582.0,
            210.0,    # 229.0
            anchor="nw",
            text="Started...10%",
            fill="#7D8CA7",
            font=("Noto Sans", 24 * -1)
        )

        self.canvas.create_text(
            582.0,
            114.0,     # 330.0
            anchor="nw",
            text="Passed",
            fill="#1ACE8D",
            font=("Noto Sans", 24 * -1)
        )


        self.canvas.create_text(
            148.0,
            208.0,     # 29.0
            anchor="nw",
            text="MOTION TEST",
            fill="#7D8CA7",
            font=("Noto Sans", 24 * -1)
        )

    def Cmd_btn_home(self):
        self.controller.show_frame(page_home.PageHome)

    def Cmd_btn_edit(self):
        # pass the value of process setting
        if self.process_status == 2:
            self.controller.frames[page_process_edit.PageProcessEdit].process_setting = self.process_setting
            self.controller.frames[page_process_edit.PageProcessEdit].update_status()
            self.controller.show_frame(page_process_edit.PageProcessEdit)

    def Cmd_btn_play(self):
        # pass the value of process setting
        print("process_status: " + str(self.process_status))
        if self.process_status == 2:
            #self.controller.frames[page_process_play.PageProcessPlay].process_setting = self.process_setting
            #self.controller.frames[page_process_play.PageProcessPlay].update_status()
            
            self.controller.frames[page_process_play.PageProcessPlay].preextract_bar.start()
            self.controller.frames[page_process_play.PageProcessPlay].extract_bar.start()
            self.controller.frames[page_process_play.PageProcessPlay].qpcr_bar.start()
            '''
            self.controller.frames[page_process_play.PageProcessPlay].preextract_bar.toggle_pause()
            '''
            self.controller.frames[page_process_play.PageProcessPlay].step()
            self.controller.show_frame(page_process_play.PageProcessPlay)

    def Cmd_btn_result(self):
        self.controller.frames[page_result_list.PageResultList].fetchResults()
        self.controller.show_frame(page_result_list.PageResultList)

    def Cmd_btn_setting(self):
        self.controller.show_frame(page_setting.PageSetting)

if __name__ == "__main__":
    window = Tk()
    window.geometry("1024x600")
    window.configure(bg = "#FFFFFF")

    container = Frame(window, bg="#FFFFFF")
    container.pack(side = "top", fill = "both", expand = True)
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)

    window.frames = {}
    frame = PageSettingSelftest(container, window)

    window.frames[PageSettingSelftest] = frame
    frame.grid(row = 0, column = 0, sticky ="nsew")
    frame.tkraise()
    window.mainloop()






