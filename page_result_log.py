
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, scrolledtext

from coutil import PCRResults
import time
import page_result_chart, page_process_init, page_home, page_setting

from copic import img_button_process_off, img_button_home_off, img_button_setting_off
from copic import img_button_result_on, img_button_log_on, img_button_return_on

class PageResultLog(Frame):

    # user data
    #OUTPUT_PATH = Path(__file__).parent
    #ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\frame_result_log")


    #def relative_to_assets(self, path: str) -> Path:
    #    return self.ASSETS_PATH / Path(path)


    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        # set user data
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
            text="RESULTS LOG",
            fill="#569FCB",
            font=("Noto Sans", 32 * -1, "bold")
        )

        self.canvas.create_rectangle(
            904.0, 0.0, 1024.0, 600.0, fill="#E6EFF4", outline="")

        self.id_testid = self.canvas.create_text(578.0, 98.0, anchor="nw",
            text="1299-3377-2311", fill="#17171B", font=("Noto Sans", 24 * -1))

        self.canvas.create_text(426.0, 98.0, anchor="nw",
            text="TEST ID", fill="#7D8CA7", font=("Noto Sans", 24 * -1))

        self.id_timestamp = self.canvas.create_text(578.0, 148.0, anchor="nw",
            text="2023-08-23 13:00:33", fill="#17171B", font=("Noto Sans", 24 * -1))

        self.canvas.create_text(426.0, 148.0, anchor="nw",
            text="RUN TIME", fill="#7D8CA7", font=("Noto Sans", 24 * -1))


        self.image_result_on = PhotoImage(data=img_button_result_on)
        self.button_result = Button(self,
            image=self.image_result_on,
            borderwidth=0,
            highlightthickness=0,
            command=self.Cmd_btn_result,
            relief="flat"
        )
        self.button_result.place(x=0.0, y=206.0, width=120.0, height=103.0)

        self.image_log_on = PhotoImage(data=img_button_log_on)

        self.button_log = Button(self,
            image=self.image_log_on,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )

        self.button_log.place(x=903.0, y=496.0, width=121.0, height=103.0)

        self.image_return_off = PhotoImage(data=img_button_return_on)
        
        self.button_return = Button(self,
            image=self.image_return_off,
            borderwidth=0,
            highlightthickness=0,
            command=self.Cmd_btn_return,
            relief="flat"
        )
        self.button_return.place(
            x=904.0,
            y=393.0,
            width=120.0,
            height=103.0
        )

        # log of results
        self.id_ct1 = self.canvas.create_text(300.0, 98.0, anchor="nw",
            text="40", fill="#17171B", font=("Noto Sans", 24 * -1))

        self.canvas.create_text(148.0, 98.0, anchor="nw",
            text="CT-VALUE1", fill="#7D8CA7", font=("Noto Sans", 24 * -1))

        self.id_ct2 = self.canvas.create_text(300.0, 148.0, anchor="nw",
            text="32", fill="#17171B", font=("Noto Sans", 24 * -1))

        self.canvas.create_text(148.0, 148.0, anchor="nw",
            text="CT-VALUE2", fill="#7D8CA7", font=("Noto Sans", 24 * -1))

        # scrolled text
        scrolW = 78
        scrolH = 13
        self.log_text = scrolledtext.ScrolledText(self, width=scrolW, height=scrolH, wrap="word", font=("Noto Sans", 16 * -1), relief="flat")  # relief="solid"
        self.log_text.place(in_ = self.canvas, x = 148, y = 210)

        self.log_text.insert("insert",
            """\
Log content dummy text 1.2.3
More dummy text
CT cycle started...
95....55....95....
Temperature not reached
Log content dummy text 1.2.3

System started

Log content dummy text 1.2.3
More dummy text
CT cycle started...
95....55....95....
Temperature not reached


More dummy text
CT cycle started...
95....55....95....
Temperature not reached
More dummy text
CT cycle started...
95....55....95....
Temperature not reached

""")
        self.log_text.configure(state ='disabled')

        self.canvas.create_rectangle(
            146.0,
            208.0,
            871.0,
            578.0,
            outline="#F0F0F0")        

    def update(self):
        self.canvas.itemconfig(self.id_testid, text=self.pcrresults.test_id)
        self.canvas.itemconfig(self.id_ct1, text=self.pcrresults.ct1)
        self.canvas.itemconfig(self.id_ct2, text=self.pcrresults.ct2)
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(self.pcrresults.timestamp))
        self.canvas.itemconfig(self.id_timestamp, text=timestamp_str)

        self.log_text.configure(state = 'normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.insert("insert", '\n'.join(self.pcrresults.proc_log))
        self.log_text.configure(state = 'disabled')

        return

    def Cmd_btn_result(self):
        #self.controller.frames[page_result_list.PageResultList].fetchResults()
        #self.controller.show_frame(page_result_list.PageResultList)
        return

    def Cmd_btn_return(self):
        self.controller.show_frame(page_result_chart.PageResultChart)
        return

    def Cmd_btn_process(self):
        # need to check if there is cartridge inside
        #self.controller.frames[page_process_init.PageProcessInit].status = 0
        self.controller.frames[page_process_init.PageProcessInit].update_status()
        self.controller.show_frame(page_process_init.PageProcessInit)

    def Cmd_btn_home(self):
        self.controller.show_frame(page_home.PageHome)

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
    frame = PageResultLog(container, window)

    window.frames[PageResultLog] = frame
    frame.grid(row = 0, column = 0, sticky ="nsew")

    frame.tkraise()
    window.mainloop()
    
