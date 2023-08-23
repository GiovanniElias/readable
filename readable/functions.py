from __future__ import annotations

import os
import platform
import sys
import time
from multiprocessing import Pool
from tkinter import filedialog

import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path


CONVERTED_IMAGE_FOLDER_NAME = 'file'
CONVERTED_IMAGE_FILE_NAME = 'file'
OUTPUT_TEXT_FILE_NAME = 'converted.txt'
OUTPUT_TEXT_PATH = ''
CONVERTED_IMAGE_FOLDER_PATH = ''
PDF_PATH = ''
THRESHOLD = 100.0


class Util:
    def timer(func):
        def wrap(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            exc_time = end - start
            fn_name = func.__name__
            print(f'{fn_name} took {exc_time} to run.')
            return result

        return wrap

    def create_folder_if_not_exists():
        global CONVERTED_IMAGE_FOLDER_PATH
        path = os.environ.get('HOME')
        folder_path = os.path.join(path, CONVERTED_IMAGE_FOLDER_NAME)
        if not os.path.exists(folder_path):
            os.chdir(path)
            os.mkdir(CONVERTED_IMAGE_FOLDER_NAME)
        CONVERTED_IMAGE_FOLDER_PATH = folder_path

    def choose_output_directory():
        global OUTPUT_TEXT_PATH
        output_text_dir = filedialog.askdirectory()
        OUTPUT_TEXT_PATH = output_text_dir


class OnclickFunctions:
    def select_input_file():
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

    def convert_to_text():
        Util.choose_output_directory()
        Util.create_folder_if_not_exists()
        Conversion.convert_pdf_to_image()
        Conversion.write_output(
            input_path=CONVERTED_IMAGE_FOLDER_PATH,
            output_path=OUTPUT_TEXT_PATH,
        )

    def open_converted_file():
        platform = sys.platform
        output_file_path = os.path.join(
            OUTPUT_TEXT_PATH, OUTPUT_TEXT_FILE_NAME)
        match platform:
            case 'darwin':
                os.system(f'open {output_file_path}')
            case 'win32' | 'win64':
                os.startfile(output_file_path)
            case 'linux':
                os.system(f'xdg-open {output_file_path}')


class Conversion:
    def is_image_blurry(image):
        try:
            variance_of_laplacian = cv2.Laplacian(image, cv2.CV_64F).var()
            print(variance_of_laplacian)
        except Exception:
            return False
        return variance_of_laplacian < THRESHOLD

    def preprocess_image(image):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened_image = cv2.filter2D(image, -1, kernel)
        return sharpened_image

    def convert_pdf_to_image():
        # according to docparser: 300 dpi seems to give otpimal results
        convert_from_path(
            PDF_PATH,
            300,
            output_folder=CONVERTED_IMAGE_FOLDER_PATH,
            output_file=CONVERTED_IMAGE_FILE_NAME,
        )

    def conversion(filename, path):
        img_path = os.path.join(path, filename)
        img = cv2.imread(img_path)
        if Conversion.is_image_blurry(img):
            img = Conversion.preprocess_image(img)
        return pytesseract.image_to_string(img)

    def image_to_text(path):
        files_to_convert = sorted(os.listdir(path))
        return [filename for filename in files_to_convert if filename.startswith(CONVERTED_IMAGE_FILE_NAME)]

    def write_output(input_path, output_path):
        output_file_path = os.path.join(output_path, OUTPUT_TEXT_FILE_NAME)
        with Pool(processes=8) as pool:
            pages = pool.starmap(
                Conversion.conversion,
                [
                    (filename, input_path)
                    for filename in Conversion.image_to_text(input_path)
                ],
            )

        with open(output_file_path, 'w') as text:
            for page in pages:
                text.write(page)
        TempCleanup.delete_temporary_images()


class TempCleanup:
    def delete_temporary_images():
        command = f'rm -rf {CONVERTED_IMAGE_FOLDER_PATH}'
        os.system(command)
