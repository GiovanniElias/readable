from __future__ import annotations

from functions import Conversion
from functions import OnclickFunctions
from functions import Util
from ui import UI


def select_input_file():
    OnclickFunctions.select_input_file()
    ui.button_convert.configure(state='active')


def convert_to_text():
    OnclickFunctions.convert_to_text()
    ui.button_open_converted_file.configure(state='active')


if __name__ == '__main__':
    ui = UI(
        select_input_file=select_input_file, convert_to_text=convert_to_text,
        open_converted_file=OnclickFunctions.open_converted_file,
    )
    ui.render()
