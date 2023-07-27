from __future__ import annotations

from tkinter import Button
from tkinter import filedialog
from tkinter import Tk

CANVAS_HEIGHT = 800
CANVAS_WIDTH = 1422

window = Tk()

window.geometry('800x1422')


def get_file_path_to_convert():
    file_path = filedialog.askopenfilename(
        initialdir='/',
        title='Select a File',
        filetypes=(
            (
                'PDF files',
                '*.pdf*',
            ),
            (
                'all files',
                '*.*',
            ),
        ),
    )

    # Change label contents
    return file_path


button_explore = Button(
    window,
    text='Browse Files',
    command=get_file_path_to_convert,
)

button_exit = Button(
    window,
    text='Exit',
    command=exit,
)
button_explore.grid(column=1, row=2)

button_exit.grid(column=1, row=3)

window.mainloop()
