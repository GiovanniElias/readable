from __future__ import annotations

import ttkbootstrap as ttk


CANVAS_HEIGHT = 300
CANVAS_WIDTH = 200
GEOMETRY = f'{CANVAS_HEIGHT}x{CANVAS_WIDTH}'


class UI:
    def __init__(self, select_input_file, convert_to_text, open_converted_file) -> None:
        self.window = ttk.Window(themename='lumen')
        self.window.geometry(GEOMETRY)
        self.window.title('Readable')
        self.select_input_file = select_input_file
        self.convert_to_text = convert_to_text
        self.open_converted_file = open_converted_file
        self.buttons()

    def buttons(self):
        self.button_explore = ttk.Button(
            self.window,
            text='Browse Files',
            command=self.select_input_file,
            width=9,
        )

        self.button_convert = ttk.Button(
            self.window,
            text='Convert File',
            command=self.convert_to_text,
            state='disabled',
            width=9,
        )

        self.button_open_converted_file = ttk.Button(
            self.window,
            text='Open File',
            command=self.open_converted_file,
            bootstyle='info',
            state='disabled',
            width=9,
        )

    def render(self):
        # Pack the buttons into the frame
        self.button_explore.pack(padx=5, pady=12)
        self.button_convert.pack(padx=5, pady=12)
        self.button_open_converted_file.pack(padx=5, pady=12)
        self.window.mainloop()
