from pathlib import Path
import os,sys
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import  Tk, \
    Canvas, Entry, Text, Button, PhotoImage,filedialog,StringVar,ttk,END,font,Checkbutton,BooleanVar,messagebox
import translate



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Users/nowhereman/Desktop/testGui/build/assets/frame0")


def dirdialog_clicked(entry_2):
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = filedialog.askdirectory(initialdir = iDir)
    iDirPath = filedialog.asksaveasfilename(filetypes=[("Mp4 Files", "*.mp4")])
    print(iDirPath)
    entry_2.delete(0, END)
    entry_2.insert(0,str(iDirPath))


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def trans(url,path,booltrans):

    error  = translate.translate(url,path,booltrans)
    if error == 0:
        messagebox.showinfo("Successed", "Complete")
    if error == 1:
        messagebox.showerror("failure", "Failure")
    if error == 2:
        messagebox.showwarning("url is nothing", "please input url")
    if error == 3:
        messagebox.showwarning("path is nothing", "please input path")
    if error == 4:
        messagebox.showerror("failure", "Failure Download")


def main():


    window = Tk()

    myfont = font.Font(family="Ink Free",slant="italic")


    window.geometry("609x425")
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=425,
        width=609,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        304.0,
        212.0,
        image=image_image_1
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        compound = "top",
        borderwidth=0,
        highlightthickness=0,
        command=lambda:trans(entry_1.get(), entry_2.get(), booltrans.get()),
        relief="flat"
    )
    button_1.place(
        x=414.0,
        y=249.0,
        width=165.0,
        height=37.0
    )

    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        436.0,
        118.5,
        image=entry_image_1
    )
    entry_1 = Entry(
        bd=0,
        bg="#C2C2C2",
        fg="#000716",
        highlightthickness=0
    )
    entry_1.place(
        x=303.0,
        y=100.0,
        width=266.0,
        height=31.0
    )

    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_2.png"))
    entry_bg_2 = canvas.create_image(
        436.0,
        180.5,
        image=entry_image_2
    )
    entry_2 = Entry(
        bd=0,
        bg="#C2C2C2",
        fg="#000716",
        highlightthickness=0
    )
    entry_2.place(
        x=303.0,
        y=167.0,
        width=236.0,
        height=31.0
    )
    entry_button_image = PhotoImage(
        file=relative_to_assets("image_2.png"))
    entry_button = Button(
        image=entry_button_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:dirdialog_clicked(entry_2),
        relief="flat"
    )
    entry_button.place(
        x=546.0,
        y=168.0,
        width=33.0,
        height=26.0
    )


    booltrans = BooleanVar()
    booltrans.set(True)

    chk = Checkbutton(variable=booltrans , text='subtitle')
    chk.place(
        x=500,
        y=210.0
    )

    canvas.create_text(
        293.0,
        81.0,
        anchor="nw",
        text="yotube url",
        fill="#FFFFFF",
        font=(myfont, 16  * -1)
    )

    canvas.create_text(
        293.0,
        144.0,
        anchor="nw",
        text="output path",
        fill="#FFFFFF",
        font=("Stoke Regular", 16 * -1)
    )
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    main()