from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Create a window
root = Tk()

# Title of window 
root.title("Button click example")

# Set the resolution of window
root.geometry("500x300+10+10")
 
# Allow Window to be resizable
root.resizable(width = True, height = True)

# Variable type Image 'tick'
tick = PhotoImage(file='assets/frame_process/button_open_on.png')
tick_clicked = PhotoImage(file='assets/frame_process/button_open_clicked.png')

def acceptClicked():
    answer = messagebox.showinfo(message='Your answer was accepted!')
    return answer

OneP = Button(root, text="1P", font=("Ink Free", 100), bg="white", activebackground="white", activeforeground="#6f56b3", borderwidth=0)
OneP.grid(row=1,column=0)

accept = Button(root, image=tick, bg="white", borderwidth=0, command=acceptClicked)
accept.grid(row=2,column=0)

accept.bind("<Button-1>", lambda click: accept.configure(image=tick_clicked))
accept.bind("<ButtonRelease-1>", lambda release: accept.configure(image=tick))



root.mainloop()