from tkinter import *
from tkcalendar import DateEntry
 
# Create Object
root = Tk()
 
# Set geometry
root.geometry("960x600")
 
# Add Calendar
#cal = Calendar(root, selectmode = 'day',
#               year = 2020, month = 5,
#               day = 22)
cal = DateEntry(root, width=24, font=("Noto Sans", 24 * -1), fieldbackground="#EBEBEB", style='flat.TButton',
                date_pattern='yyyy/mm/dd')

 
cal.pack(pady = 20)
 
def grad_date():
    date.config(text = "Selected Date is: " + cal.get())
    
 
# Add Button and Label
Button(root, text = "Get Date",
       command = grad_date).pack(pady = 20)
 
date = Label(root, text = "")
date.pack(pady = 20)
 
# Execute Tkinter
root.mainloop()