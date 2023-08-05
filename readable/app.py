from __future__ import annotations

import concurrent.futures
import os
from multiprocessing import Pool
from timeit import Timer
from tkinter import Button
from tkinter import filedialog
from tkinter import FLAT
from tkinter import Frame
from tkinter import Label
from tkinter import PhotoImage
from tkinter import SUNKEN
from tkinter import Tk

import cv2
import pytesseract
import ttkbootstrap as ttk
from function import timer
from pdf2image import convert_from_path

CANVAS_HEIGHT = 200
CANVAS_WIDTH = 150
GEOMETRY = f'{CANVAS_HEIGHT}x{CANVAS_WIDTH}'
BACKGROUND_COLOR = '#d6d6d6'

CONVERTED_IMAGE_BASE_PATH = 'file'
PDF_PATH = ''
CONVERTED_IMAGE_FOLDER_PATH = ''
OUTPUT_TEXT_PATH = ''
OUTPUT_TEXT_FILE_NAME = 'converted.txt'
HIGHLIGHT_BUTTON_COLOR = '#007AFF'
HIGHLIGHT_BUTTON_FLAG = False


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


def conversion(filename, path):
    img_path = os.path.join(path, filename)
    img = cv2.imread(img_path)
    return pytesseract.image_to_string(img)


@timer  # 8.094518
def image_to_text(path):
    files_to_convert = sorted(os.listdir(path))
    return [filename for filename in files_to_convert]


@timer
def write_output(input_path, output_path):
    output_file_path = os.path.join(output_path, OUTPUT_TEXT_FILE_NAME)
    with Pool(processes=8) as pool:
        pages = pool.starmap(
            conversion, [(filename, input_path)
                         for filename in image_to_text(input_path)],
        )

    with open(output_file_path, 'w') as text:
        for page in pages:
            text.write(page)


def choose_directory():
    global OUTPUT_TEXT_PATH
    output_text_dir = filedialog.askdirectory()
    OUTPUT_TEXT_PATH = output_text_dir


def convert_to_text():
    choose_directory()
    write_output(
        input_path=CONVERTED_IMAGE_FOLDER_PATH,
        output_path=OUTPUT_TEXT_PATH,
    )


def on_enter(e):
    # Function to change button border color when the mouse hovers over the button
    button_explore.configure(relief=SUNKEN)


def on_leave(e):
    # Function to reset button border color when the mouse leaves the button
    button_explore.configure(relief=FLAT)


if __name__ == '__main__':
    window = Tk()

    window.geometry(GEOMETRY)
    window.title('Readable')
    window.configure(background=BACKGROUND_COLOR)

    # Create the frame with the same background color to simulate the "mac os feel"

    button_explore = ttk.Button(
        window,
        text='Browse Files',
        command=pdf_to_image,
    )
    button_explore.bind('<Enter>', on_enter)
    button_explore.bind('<Leave>', on_leave)

    button_convert = ttk.Button(
        window,
        text='Convert File',
        command=convert_to_text,
    )

    # Pack the buttons into the frame
    button_explore.pack(padx=5, pady=12)
    button_convert.pack(padx=5, pady=12)

    window.mainloop()
