
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import round_rect

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\CO_BT\20230718_UI\TDVersion\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1024x600")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 1024,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1024.0,
    600.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    120.0,
    0.0,
    904.0,
    600.0,
    fill="#F9F9F9",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=0.0,
    y=103.0,
    width=120.0,
    height=103.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=0.0,
    y=0.0,
    width=120.0,
    height=103.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=0.0,
    y=206.0,
    width=120.0,
    height=103.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=0.0,
    y=497.0,
    width=120.0,
    height=103.0
)

canvas.create_text(
    148.0,
    16.0, #24.0,
    anchor="nw",
    text="PROCESS",
    fill="#569FCB",
    font=("Noto Sans", 32 * -1)
)

canvas.create_rectangle(
    904.0,
    0.0,
    1024.0,
    600.0,
    fill="#E6EFF4",
    outline="")

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
button_5.place(
    x=938.0,
    y=130.0,
    width=52.0,
    height=52.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
button_6.place(
    x=938.0,
    y=233.0,
    width=52.0,
    height=52.0
)

canvas.create_text(
    148.0,
    105.0, #113.0,
    anchor="nw",
    text="PRE-EXTRACT",
    fill="#7D8CA7",
    font=("Noto Sans", 24 * -1)
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
button_7.place(
    x=354.0,
    y=96.0,
    width=140.0,
    height=70.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat"
)
button_8.place(
    x=522.0,
    y=96.0,
    width=140.0,
    height=70.0
)

canvas.create_text(
    148.0,
    200.0, #208.0,
    anchor="nw",
    text="PRE-COOL",
    fill="#7D8CA7",
    font=("Noto Sans", 24 * -1)
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat"
)
button_9.place(
    x=354.0,
    y=191.0,
    width=140.0,
    height=70.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat"
)
button_10.place(
    x=522.0,
    y=191.0,
    width=140.0,
    height=70.0
)

canvas.create_text(
    148.0,
    293.0, #301.0,
    anchor="nw",
    text="EXTRACT TIME",
    fill="#7D8CA7",
    font=("Noto Sans", 24 * -1)
)

canvas.create_text(
    148.0,
    387.0, #395.0,
    anchor="nw",
    text="SPIN RPM",
    fill="#7D8CA7",
    font=("Noto Sans", 24 * -1)
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_11 clicked"),
    relief="flat"
)
button_11.place(
    x=522.0,
    y=284.0,
    width=140.0,
    height=70.0
)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_12 clicked"),
    relief="flat"
)
button_12.place(
    x=352.0,
    y=284.0,
    width=140.0,
    height=70.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_13 clicked"),
    relief="flat"
)
button_13.place(
    x=688.0,
    y=285.0,
    width=140.0,
    height=70.0
)

button_image_14 = PhotoImage(
    file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_14 clicked"),
    relief="flat"
)
button_14.place(
    x=354.0,
    y=378.0,
    width=140.0,
    height=70.0
)

button_image_15 = PhotoImage(
    file=relative_to_assets("button_15.png"))
button_15 = Button(
    image=button_image_15,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_15 clicked"),
    relief="flat"
)
button_15.place(
    x=522.0,
    y=378.0,
    width=140.0,
    height=70.0
)

button_image_16 = PhotoImage(
    file=relative_to_assets("button_16.png"))
button_16 = Button(
    image=button_image_16,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_16 clicked"),
    relief="flat"
)
button_16.place(
    x=521.0,
    y=473.0,
    width=140.0,
    height=70.0
)

button_image_17 = PhotoImage(
    file=relative_to_assets("button_17.png"))
button_17 = Button(
    image=button_image_17,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_17 clicked"),
    relief="flat"
)
button_17.place(
    x=688.0,
    y=378.0,
    width=140.0,
    height=70.0
)

canvas.create_text(
    148.0,
    480.0, #488.0,
    anchor="nw",
    text="PCR CYCLE",
    fill="#7D8CA7",
    font=("Noto Sans", 24 * -1)
)

button_image_18 = PhotoImage(
    file=relative_to_assets("button_18.png"))
button_18 = Button(
    image=button_image_18,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_18 clicked"),
    relief="flat"
)
button_18.place(
    x=688.0,
    y=473.0,
    width=140.0,
    height=70.0
)

button_image_19 = PhotoImage(
    file=relative_to_assets("button_19.png"))
button_19 = Button(
    image=button_image_19,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_19 clicked"),
    relief="flat"
)
button_19.place(
    x=355.0,
    y=473.0,
    width=140.0,
    height=70.0
)

button_image_20 = PhotoImage(
    file=relative_to_assets("button_20.png"))
button_20 = Button(
    image=button_image_20,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_20 clicked"),
    relief="flat"
)
button_20.place(
    x=903.0,
    y=2.0,
    width=121.0,
    height=103.0
)

canvas.create_text(
    495.0,
    21.0, #29.0,
    anchor="nw",
    text="Total Time:",
    fill="#7D8CA7",
    font=("Noto Sans", 24 * -1)
)

canvas.create_rectangle(
    635.0,
    25.0,
    828.0,
    69.0,
    fill="#FFFFFF",
    outline="black")

canvas.create_text(
    732.0,
    43.0,
    anchor="center",
    text="00:48",
    fill="#17171B",
    font=("Noto Sans", 24 * -1)
)


window.resizable(False, False)
window.mainloop()