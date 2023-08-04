from __future__ import annotations

import concurrent.futures
import os
from timeit import Timer
from tkinter import Button
from tkinter import filedialog
from tkinter import FLAT
from tkinter import Frame
from tkinter import Label
from tkinter import PhotoImage
from tkinter import SUNKEN
from tkinter import Tk
from tkinter import ttk

import cv2
import pytesseract
from function import timer
from pdf2image import convert_from_path

CANVAS_HEIGHT = 250
CANVAS_WIDTH = 150
GEOMETRY = f'{CANVAS_HEIGHT}x{CANVAS_WIDTH}'
BACKGROUND_COLOR = '#d6d6d6'

CONVERTED_IMAGE_BASE_PATH = 'file'
PDF_PATH = ''
CONVERTED_IMAGE_FOLDER_PATH = ''
OUTPUT_TEXT_PATH = ''
OUTPUT_TEXT_FILE_NAME = 'converted.txt'

window = Tk()

window.geometry(GEOMETRY)
window.title('Readable')
window.configure(background=BACKGROUND_COLOR)


@timer  # 0.13524599999999998
def get_file_path_to_convert():
    global PDF_PATH
    try:
        PDF_PATH = filedialog.askopenfilename(
            initialdir='/',
            title='Select a File',
            filetypes=(
                (
                    'PDF files',
                    '*.pdf',
                ),
                (
                    'all files',
                    '*.*',
                ),
            ),
        )
    except OSError:
        print('Input Error.')


def create_folder_if_not_exists(folder_name):
    global CONVERTED_IMAGE_FOLDER_PATH
    path = os.environ.get('HOME')
    folder_path = os.path.join(path, folder_name)
    if not os.path.exists(folder_path):
        os.chdir(path)
        os.mkdir(folder_name)
    CONVERTED_IMAGE_FOLDER_PATH = folder_path


@timer  # 0.3343799999999999
def pdf_to_image():
    get_file_path_to_convert()
    create_folder_if_not_exists(CONVERTED_IMAGE_BASE_PATH)
    convert_from_path(
        PDF_PATH,
        500,
        output_folder=CONVERTED_IMAGE_FOLDER_PATH,
        output_file='file',
    )


@timer
def write_output(path, output):
    path = os.path.join(path, OUTPUT_TEXT_FILE_NAME)
    with open(path, 'w') as text:
        for page_future in output:
            page = page_future.result()
            text.write(page)


def conversion(filename):
    img_path = os.path.join(CONVERTED_IMAGE_FOLDER_PATH, filename)
    img = cv2.imread(img_path)
    return pytesseract.image_to_string(img)


def with_threading(filename):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        return executor.submit(conversion, filename)


@timer  # 8.094518
def image_to_text():
    output = []
    for filename in sorted(os.listdir(CONVERTED_IMAGE_FOLDER_PATH)):
        output.append(with_threading(filename))

    return output


def choose_directory():
    global OUTPUT_TEXT_PATH
    output_text_dir = filedialog.askdirectory()
    OUTPUT_TEXT_PATH = output_text_dir


def convert_to_text():
    choose_directory()
    output = image_to_text()
    write_output(path=OUTPUT_TEXT_PATH, output=output)


def on_enter(e):
    # Function to change button border color when the mouse hovers over the button
    button_explore.configure(relief=SUNKEN)


def on_leave(e):
    # Function to reset button border color when the mouse leaves the button
    button_explore.configure(relief=FLAT)


# Create the frame with the same background color to simulate the "mac os feel"
frame = Frame(window, background=BACKGROUND_COLOR)

button_explore = Button(
    frame,
    text='Browse Files',
    command=pdf_to_image,
    relief=FLAT,
    background=BACKGROUND_COLOR,
    foreground='black',
    borderwidth=2,
    highlightbackground=BACKGROUND_COLOR,
    highlightthickness=0,
)
button_explore.bind('<Enter>', on_enter)
button_explore.bind('<Leave>', on_leave)

button_convert = Button(
    frame,
    text='Convert File',
    command=convert_to_text,
    relief=FLAT,
    background=BACKGROUND_COLOR,
    foreground='black',
    borderwidth=2,
    highlightbackground=BACKGROUND_COLOR,
    highlightthickness=0,
)

# Pack the buttons into the frame
button_explore.pack(padx=5, pady=12)
button_convert.pack(padx=5, pady=12)

# Pack the frame into the window
frame.pack(padx=10, pady=20)

window.mainloop()
