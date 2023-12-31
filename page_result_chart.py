
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame
import numpy as np
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline, BSpline
from coutil import PCRResults
import page_result_list, page_process_init, page_home, page_setting, page_result_log

from copic import img_button_process_off, img_button_home_off, img_button_setting_off
from copic import img_button_log_off, img_button_export_off, img_button_folder_off, img_button_result_on

class PageResultChart(Frame):

    # user data
    #OUTPUT_PATH = Path(__file__).parent
    #ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame_result_chart")


    #def relative_to_assets(self, path: str) -> Path:
    #    return self.ASSETS_PATH / Path(path)


    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # set user data
        # set result data
        self.pcrresults = PCRResults()

        # set window size
        width = 1024
        height = 600

        screenwidth = controller.winfo_screenwidth()
        screenheight = controller.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        controller.geometry(alignstr)
        controller.resizable(width=False, height=False)

        # flat background

        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 600,
            width = 1024,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.grid(row = 0, column = 0, sticky = "nsew")

        # add elements here
        self.canvas.create_rectangle(
            120.0,
            0.0,
            904.0,
            600.0,
            fill="#F9F9F9",
            outline="")

        self.image_process_off = PhotoImage(data=img_button_process_off)
        self.button_process = Button(self,
            image=self.image_process_off,
            borderwidth=0,
            highlightthickness=0,
            command=self.Cmd_btn_process,
            relief="flat"
        )

        self.button_process.place(
            x=0.0,
            y=103.0,
            width=120.0,
            height=103.0
        )

        self.image_home_off = PhotoImage(data=img_button_home_off)
        self.button_home = Button(self,
            image=self.image_home_off,
            borderwidth=0,
            highlightthickness=0,
            command=self.Cmd_btn_home,
            relief="flat"
        )
        self.button_home.place(
            x=0.0,
            y=0.0,
            width=120.0,
            height=103.0
        )

        self.image_setting_off = PhotoImage(data=img_button_setting_off)
        self.button_setting = Button(self,
            image=self.image_setting_off,
            borderwidth=0,
            highlightthickness=0,
            command=self.Cmd_btn_setting,
            relief="flat"
        )
        self.button_setting.place(
            x=0.0,
            y=497.0,
            width=120.0,
            height=103.0
        )

        self.canvas.create_text(
            148.0,
            24.0,
            anchor="nw",
            text="RESULTS",
            fill="#569FCB",
            font=("Noto Sans", 32 * -1, "bold")
        )

        self.canvas.create_rectangle(
            904.0, 0.0, 1024.0, 600.0, fill="#E6EFF4", outline="")

        self.id_testid = self.canvas.create_text(276.0, 94.0, anchor="nw",
            text="1299-3377-2311", fill="#17171B", font=("Noto Sans", 20 * -1))

        self.id_ct1 = self.canvas.create_text(678.0, 94.0, anchor="nw",
            text="22", fill="#17171B", font=("Noto Sans", 20 * -1))

        self.canvas.create_text(148.0, 94.0, anchor="nw",
            text="TEST ID", fill="#7D8CA7", font=("Noto Sans", 20 * -1))

        self.id_timestamp = self.canvas.create_text(276.0, 133.0, anchor="nw",
            text="2023-08-23 13:00:33", fill="#17171B", font=("Noto Sans", 20 * -1))

        self.canvas.create_text(148.0, 133.0, anchor="nw",
            text="RUN TIME", fill="#7D8CA7", font=("Noto Sans", 20 * -1))

        self.canvas.create_text(519.0, 94.0, anchor="nw",
            text="WELL 1 CT", fill="#7D8CA7", font=("Noto Sans", 20 * -1))

        self.canvas.create_rectangle(647.0, 104.0, 667.0, 124.0,
            fill="#F466B3", outline="")

        self.id_ct2 = self.canvas.create_text(678.0, 137.0, anchor="nw",
            text="32", fill="#17171B", font=("Noto Sans", 20 * -1))

        self.canvas.create_text(519.0, 137.0, anchor="nw",
            text="WELL 2 CT", fill="#7D8CA7", font=("Noto Sans", 20 * -1))

        self.canvas.create_rectangle(647.0, 147.0, 667.0, 167.0,
            fill="#3DAAEB", outline="")


        self.image_log_off = PhotoImage(data=img_button_log_off)

        self.button_log = Button(self,
            image=self.image_log_off,
            borderwidth=0,
            highlightthickness=0,
            command=self.Cmd_btn_result_log,
            relief="flat"
        )

        self.button_log.place(x=903.0, y=496.0, width=121.0, height=103.0)

        self.image_export_off = PhotoImage(data=img_button_export_off)

        self.button_leave = Button(self,
            image=self.image_export_off,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )

        self.button_leave.place(x=903.0, y=395.0, width=121.0, height=103.0)

        self.image_folder_off = PhotoImage(data=img_button_folder_off)

        self.button_folder = Button(self,
            image=self.image_folder_off,
            borderwidth=0,
            highlightthickness=0,
            command=self.Cmd_btn_result,
            relief="flat"
        )

        self.button_folder.place(x=903.0, y=0.0, width=121.0, height=103.0)

        self.image_result_on = PhotoImage(data=img_button_result_on)
        self.button_result = Button(self,
            image=self.image_result_on,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_result.place(x=0.0, y=206.0, width=120.0, height=103.0)



        # list of results

        # curve chart
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.figure.subplots_adjust(left=0, bottom=0, right=0.97, top=1, wspace=0, hspace=0)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)

        self.axes = self.figure.add_subplot()

        # create the curve chart
        time_array = np.arange(0, 41)

        self.axes.set_xlim([0,40])
        self.axes.set_ylim([-0.2,2])
        self.axes.set_xticks([10, 20, 30, 40])
        self.axes.set_yticks([])
        self.axes.vlines(10, 0, 2, color="#CECECE")
        self.axes.vlines(20, 0, 2, color="#CECECE")
        self.axes.vlines(30, 0, 2, color="#CECECE")
        self.axes.spines['bottom'].set_position(('data', 0))
        self.axes.spines[['right', 'top']].set_visible(False)

        # smooth or not
        smooth_curve = True

        if smooth_curve:
            xnew = np.linspace(0, 41, 300)
            spl1 = make_interp_spline(time_array, self.pcrresults.well1_array, k = 1)  # type: BSpline
            a1_smooth = spl1(xnew)

            spl2 = make_interp_spline(time_array, self.pcrresults.well2_array, k = 1)  # type: BSpline
            a2_smooth = spl2(xnew)
            self.curve1, = self.axes.plot(xnew, a1_smooth, color="#F467B3")
            self.curve2, = self.axes.plot(xnew, a2_smooth, color="#3EAAEC")

        else:
            self.curve1, = self.axes.plot(time_array, self.pcrresults.well1_array, color="#F467B3")
            self.curve2, = self.axes.plot(time_array, self.pcrresults.well2_array, color="#3EAAEC")

        # place the chart
        self.figure_canvas.get_tk_widget().place(x=148.0, y=210.0, width=728.0, height=364.0)

        self.update()

    def update(self):
        self.canvas.itemconfig(self.id_testid, text=self.pcrresults.test_id)
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.pcrresults.timestamp))
        self.canvas.itemconfig(self.id_timestamp, text=timestamp_str)
        self.canvas.itemconfig(self.id_ct1, text=self.pcrresults.ct1)
        self.canvas.itemconfig(self.id_ct2, text=self.pcrresults.ct2)

        # smooth or not
        smooth_curve = True
        # create the curve chart
        time_array = np.arange(0, 41)
        
        if smooth_curve:
            xnew = np.linspace(0, 41, 300)
            spl1 = make_interp_spline(time_array, self.pcrresults.well1_array, k = 1)  # type: BSpline
            a1_smooth = spl1(xnew)

            spl2 = make_interp_spline(time_array, self.pcrresults.well2_array, k = 1)  # type: BSpline
            a2_smooth = spl2(xnew)
            # update y value
            self.curve1.set_ydata(a1_smooth)
            self.curve2.set_ydata(a2_smooth)
        else:
            # update y value
            self.curve1.set_ydata(self.pcrresults.well1_array)
            self.curve2.set_ydata(self.pcrresults.well2_array)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        
        print(self.pcrresults.ct1)

        return

    def Cmd_btn_result(self):
        self.controller.frames[page_result_list.PageResultList].fetchResults()
        self.controller.show_frame(page_result_list.PageResultList)

    def Cmd_btn_process(self):
        # need to check if there is cartridge inside
        #self.controller.frames[page_process_init.PageProcessInit].status = 0
        self.controller.frames[page_process_init.PageProcessInit].update_status()
        self.controller.show_frame(page_process_init.PageProcessInit)

    def Cmd_btn_home(self):
        self.controller.show_frame(page_home.PageHome)

    def Cmd_btn_setting(self):
        self.controller.show_frame(page_setting.PageSetting)

    def Cmd_btn_result_log(self):
        self.controller.frames[page_result_log.PageResultLog].pcrresults = self.pcrresults
        self.controller.frames[page_result_log.PageResultLog].update()
        self.controller.show_frame(page_result_log.PageResultLog)


if __name__ == "__main__":
    window = Tk()
    window.geometry("1024x600")
    window.configure(bg = "#FFFFFF")

    container = Frame(window, bg="#FFFFFF")
    container.pack(side = "top", fill = "both", expand = True)
    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)

    window.frames = {}
    frame = PageResultChart(container, window)

    window.frames[PageResultChart] = frame
    frame.grid(row = 0, column = 0, sticky ="nsew")

    frame.tkraise()
    window.mainloop()
    
