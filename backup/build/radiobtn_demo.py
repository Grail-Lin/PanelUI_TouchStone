import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

# user data
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame_process_init")



val = tk.StringVar()

radio_btn1 = tk.Radiobutton(root, text='Apple', variable=val, value='apple')    # 放入第一個單選按鈕
radio_btn1.pack()
radio_btn1.select()

radio_btn2 = tk.Radiobutton(root, text='Banana', variable=val, value='banana')   # 放入第二個單選按鈕
radio_btn2.pack()

root.mainloop()