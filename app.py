import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import customtkinter as ctk
import pd
import ttkbootstrap as tkb
from ttkbootstrap.constants import *

def main():
    root = tkb.Window(themename="darkly")

    t1 = TranslatorApp()
    t1.create_layout(root)
    root.mainloop()

    translator = pd.BBYTranslator()


class TranslatorApp:
    def __init__(self):
        self.filename_var = ctk.StringVar()
        self.radio_var = tk.IntVar(value=0)

    def create_layout(self, root):
        root.title("Translation Tool")
        root.geometry("1000x600")
        root.resizable(False, False)

        frame = ctk.CTkFrame(root)
        frame.place(x=0, y=0, relwidth=1, relheight=1)

        label_frame = tkb.Frame(frame)
        label_frame.place(relx=0.006, rely=0.01, relwidth=0.2, relheight=0.98)

        label = tkb.Label(master=label_frame, text="File", bootstyle="DEFAULT")
        label.place(relx=0.055, rely=0.01)

        # StringVar to store the filename
        filename = tkb.Entry(label_frame, textvariable=self.filename_var)
        filename.place(relx=0.05, rely=0.05, relwidth=0.9)

        browse_button = tkb.Button(
            label_frame, text="Browse", command=lambda: self.browse_file(), bootstyle="LIGHT"
        )
        browse_button.place(relx=0.5, rely=0.11, relwidth=0.44)

        radiobutton_1 = tkb.Radiobutton(
            label_frame,
            text="SKU",
            command=self.radiobutton_event(),
            variable=self.radio_var,
            value=1,
        )
        radiobutton_2 = tkb.Radiobutton(
            label_frame,
            text="Word",
            command=self.radiobutton_event(),
            variable=self.radio_var,
            value=2,
        )
        radiobutton_1.place(relx=0.05, rely=0.18)
        radiobutton_2.place(relx=0.4, rely=0.18)

        cols = (
            ["SKU"],
            ["SKU_DESC"],
            ["SKU_DESC FR"],
            ["SHORT_DESC"],
            ["SHORT_DESC FR"],
        )
        output = ctk.CTkTextbox(master=frame, width=50)
        output.place(relx=0.215, rely=0.01, relwidth=0.78, relheight=0.98)

        output.insert(tk.INSERT,text="SKU\t\t")
   

        output.insert(tk.INSERT,text="DESCRIPTION\n")
        output.configure(state="disabled")





    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.filename_var.set(file_path)
            print("Selected file:", file_path)

    def radiobutton_event(self):
        pass


if __name__ == "__main__":
    main()
