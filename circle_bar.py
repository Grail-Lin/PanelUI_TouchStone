try:
    import Tkinter as tk
    import tkFont
    import ttk
except ImportError:  # Python 3
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.ttk as ttk


class CircularProgressbar(object):
    def __init__(self, canvas, x0, y0, x1, y1, width=2, start_ang=0, full_extent=360., clockwise=0, fg="#0F0F0F", bg="#FFFFFF", fill="#FFFFFF", total_time=15):
        self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
        self.canvas = canvas
        self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
        self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
        self.width = width
        self.start_ang, self.full_extent = start_ang, full_extent

        self.fg = fg
        self.bg = bg
        self.fill = fill
        # draw static bar outline
        w2 = width / 2
        self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                self.x1+w2, self.y1+w2, fill=self.bg, outline=self.fill)
        self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                self.x1-w2, self.y1-w2, fill="#FFFFFF", outline=self.fill)
        self.running = False
        self.clockwise = clockwise    # 0: counterclockwise, 1: clockwise
        self.total_time = total_time

    '''
        total_time = N (default 15s)
        circle bar total arc = full_extent = 360
        1 sec as interval = 1000 ms
        every second increment = (total arc)/(total time)
        a step is 1000/internal second
    '''

    def start(self, interval=100):
        self.interval = interval  # Msec delay between updates.
        #self.increment = self.full_extent / interval
        self.increment = self.full_extent * self.interval / self.total_time / 1000.0
        self.extent = 0
        self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                             start=self.start_ang, extent=self.extent,
                                             width=self.width, style='arc', outline=self.fg)
        percent = '0%'
        self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                font=self.custom_font)
        self.running = True
        self.canvas.after(interval, self.step, self.increment)

    def step(self, delta):
        """Increment extent and update arc and label displaying how much completed."""
        if self.running:
            self.extent = (self.extent + delta) % 360

            if self.clockwise == 0:
                self.canvas.itemconfigure(self.arc_id, extent=self.extent)
            elif self.clockwise == 1:
                self.canvas.itemconfigure(self.arc_id, extent=360.0-self.extent)


            # Update percentage value displayed.
            percent = '{:.0f}%'.format(
                                    round(float(self.extent) / self.full_extent * 100))
            self.canvas.itemconfigure(self.label_id, text=percent)
        self.canvas.after(self.interval, self.step, delta)


    def toggle_pause(self):
        self.running = not self.running


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self, width=200, height=200, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.progressbar = CircularProgressbar(self.canvas, 0, 0, 200, 200, 20, start_ang=90, clockwise=1, fg="#CECECE", bg="#569FCB", fill="#FFFFFF", total_time=10)

        self.pauseButton = tk.Button(self, text='Pause', command=self.pause)
        self.pauseButton.grid(row=1, column=0)
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row=1, column=1)

    def start(self):
        self.progressbar.start()
        self.mainloop()

    def pause(self):
        self.progressbar.toggle_pause()

if __name__ == '__main__':
    app = Application()
    app.master.title('Sample application')
    app.start()