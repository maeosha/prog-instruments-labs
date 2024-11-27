#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import webbrowser
import tkinter as tk
from typing import Dict, Any

import i18n
from Tape import Tape
from execute_code import (
    import_code, execute_code, move, write, clear_tape
)
from generate_template import generate_template
from initialisation import initialisation


class TuringMachineApp:
    def __init__(self) -> None:
        """Initialize the Turing Machine application."""
        initialisation(self)

        window_width = 800
        window_height = 380
        self.root = tk.Tk()
        self.root.geometry(
            '%dx%d+%d+%d' % (
                window_width,
                window_height,
                int(self.root.winfo_screenwidth() / 2 - window_width / 2),
                int(self.root.winfo_screenheight() / 2 - window_height / 2)
            )
        )
        self.root.resizable(width=False, height=False)
        self.root.title(i18n.t("main_title"))
        self.root.bind(
            "<Control-o>", lambda event: import_code(self)
        )

        self.input_data: Dict[str, Any] = {}
        self.execution_history = ()
        self.cell_coordinates: Dict[str, list] = {
            '14': [40, 20, self.color_blank], '13': [42, 40, self.color_blank],
            '12': [45, 60, self.color_blank], '11': [49, 80, self.color_blank],
            '10': [54, 100, self.color_blank], '9': [60, 120, self.color_blank],
            '8': [68, 140, self.color_blank], '7': [78, 160, self.color_blank],
            '6': [90, 180, self.color_blank], '5': [104, 200, self.color_blank],
            '4': [118, 220, self.color_blank], '3': [136, 237, self.color_blank],
            '2': [156, 252, self.color_blank], '1': [178, 265, self.color_blank],
            '0': [204, 270, self.color_blank], '-1': [228, 265, self.color_blank],
            '-2': [250, 252, self.color_blank], '-3': [270, 237, self.color_blank],
            '-4': [288, 220, self.color_blank], '-5': [304, 200, self.color_blank],
            '-6': [318, 180, self.color_blank], '-7': [330, 160, self.color_blank],
            '-8': [340, 140, self.color_blank], '-9': [348, 120, self.color_blank],
            '-10': [354, 100, self.color_blank], '-11': [359, 80, self.color_blank],
            '-12': [363, 60, self.color_blank], '-13': [366, 40, self.color_blank],
            '-14': [368, 20, self.color_blank]
        }
        self.tape = Tape()
        self.current_directory = os.getcwd()
        self.templates_directory = os.path.join(
            self.current_directory, "default_templates"
        )

        self.create_menus()
        self.create_execution_frame()
        self.create_state_frame()

    def create_menus(self) -> None:
        """Create the application menus."""
        main_menu = tk.Menu(self.root)
        file_menu = tk.Menu(tearoff=0)
        main_menu.add_cascade(label=i18n.t("file"), menu=file_menu)
        file_menu.add_command(
            label=i18n.t("open"), command=lambda: import_code(self)
        )
        file_menu.add_command(
            label=i18n.t("config_editor"), command=self.open_config_editor
        )
        file_menu.add_command(label=i18n.t("exit"), command=self.root.destroy)

        templates_menu = tk.Menu(tearoff=0)
        main_menu.add_cascade(label=i18n.t("templates"), menu=templates_menu)
        templates_menu.add_command(
            label=i18n.t("generate"), command=lambda: generate_template(self)
        )
        load_templates_menu = tk.Menu(tearoff=0)
        templates_menu.add_cascade(label=i18n.t("load"), menu=load_templates_menu)
        load_templates_menu.add_command(
            label=i18n.t("invert_value"),
            command=lambda: import_code(self, os.path.join(
                self.templates_directory, "invert_values.ptm"))
        )
        load_templates_menu.add_command(
            label=i18n.t("add_one"),
            command=lambda: import_code(self, os.path.join(
                self.templates_directory, "add_one_binary.ptm"))
        )
        load_templates_menu.add_command(
            label=i18n.t("remove_one"),
            command=lambda: import_code(self, os.path.join(
                self.templates_directory, "remove_one_binary.ptm"))
        )

        language_menu = tk.Menu(tearoff=0)
        main_menu.add_cascade(label=i18n.t("language"), menu=language_menu)
        language_menu.add_command(
            label="English", command=lambda: self.change_language("en")
        )
        language_menu.add_command(
            label="Français", command=lambda: self.change_language("fr")
        )

        main_menu.add_command(
            label=i18n.t("help"),
            command=lambda: subprocess.Popen(
                [os.path.join(self.current_directory, "documentation.pdf")],
                shell=True
            )
        )
        main_menu.add_command(
            label="Github",
            command=lambda: webbrowser.open(
                "https://github.com/Yoween/PythonTuringMachine"
            )
        )

        self.root.config(menu=main_menu)

    def create_execution_frame(self) -> None:
        """Create the execution area to display the Turing machine's operation."""
        try:
            self.execution_frame.destroy()
        except AttributeError:
            pass
        self.execution_frame = tk.Frame(self.root, bg='AntiqueWhite2')

        canvas = tk.Canvas(self.execution_frame, height=310, bg='AntiqueWhite2')
        canvas.grid(row=1, column=0, columnspan=8, sticky='nesw')
        for coordinates in self.cell_coordinates.values():
            self.draw_cell(
                canvas, coordinates[0], coordinates[1], 6, coordinates[2]
            )

        slow_var = tk.IntVar()
        start_button = tk.Button(
            self.execution_frame,
            text=i18n.t("start"),
            command=lambda: execute_code(
                self, self, self.input_data, slow_var.get()
            )
        )
        start_button.grid(row=10, column=0, padx=10, sticky='nesw')
        clear_button = tk.Button(
            self.execution_frame,
            text=i18n.t("clear"),
            command=lambda: clear_tape(self, self)
        )
        clear_button.grid(row=10, column=1, sticky='nesw')
        left_button = tk.Button(
            self.execution_frame,
            text=i18n.t("left"),
            command=lambda: move(self, self, "<")
        )
        left_button.grid(row=10, column=2, sticky='nesw')
        right_button = tk.Button(
            self.execution_frame,
            text=i18n.t("right"),
            command=lambda: move(self, self, ">")
        )
        right_button.grid(row=10, column=3, sticky='nesw')
        value_label = tk.Label(self.execution_frame, text=i18n.t("value"))
        value_label.grid(row=10, column=4, padx=(10, 0), sticky='nesw')
        next_value_label = tk.Label(self.execution_frame, text=i18n.t("next_value"))
        next_value_label.grid(row=10, column=5, padx=(0, 10), sticky='nesw')

        tk.Checkbutton(
            self.execution_frame,
            text=i18n.t("slow"),
            variable=slow_var,
            offvalue=0,
            onvalue=1
        ).grid(row=11, column=0, padx=10, sticky='nesw')

        b_button = tk.Button(
            self.execution_frame,
            text="b",
            bg=self.color_blank,
            command=lambda: write(self, self, "b")
        )
        b_button.grid(row=11, column=1, sticky='nesw')
        zero_button = tk.Button(
            self.execution_frame,
            text="0",
            bg=self.color_zero,
            command=lambda: write(self, self, "0")
        )
        zero_button.grid(row=11, column=2, sticky='nesw')
        one_button = tk.Button(
            self.execution_frame,
            text="1",
            bg=self.color_one,
            command=lambda: write(self, self, "1")
        )
        one_button.grid(row=11, column=3, sticky='nesw')

        current_value_label = tk.Label(self.execution_frame, text="")
        current_value_label.grid(row=11, column=4, padx=(10, 0), sticky='nesw')
        next_value_display_label = tk.Label(self.execution_frame, text="")
        next_value_display_label.grid(row=11, column=5, padx=(0, 10), sticky='nesw')

        self.execution_frame.pack(side='right', expand=True, fill='both')
        for i in range(5):
            self.execution_frame.columnconfigure(i, weight=1)

    def create_state_frame(self) -> None:
        """Create the state area to display the current states of the Turing machine."""
        try:
            self.state_frame.destroy()
        except AttributeError:
            pass
        self.state_frame = tk.Frame(self.root)

        self.setup_scrollable_area(self.state_frame, self.root.winfo_screenwidth())

        state_names = ("state", "read", "write", "move", "new_state")
        for i in range(5):
            self.__dict__[f"label_{state_names[i]}"] = tk.Label(
                self.scroll_frame, text=f"{i18n.t(state_names[i])}", relief=tk.RIDGE
            )
            self.__dict__[f"label_{state_names[i]}"].grid(
                row=0, column=i, sticky='nesw'
            )

        self.state_frame.pack(side='left', expand=True, fill='both')
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        for i in range(5):
            self.scroll_frame.columnconfigure(i, weight=1)

        x = 1
        while f"label_state{x}" in self.__dict__.keys():
            for symbol in ("b", "0", "1"):
                del self.__dict__[f"label_read{x}_{symbol}"]
                del self.__dict__[f"label_write{x}_{symbol}"]
                del self.__dict__[f"label_move{x}_{symbol}"]
                del self.__dict__[f"label_new_state{x}_{symbol}"]
            del self.__dict__[f"label_state{x}"]
            x += 1
        self.scroll_frame.update()

    def add_new_state(self, instructions: Dict[str, list]) -> None:
        """Add a new state to the state area.

        Args:
            instructions (dict): A dictionary containing instructions for the new state.
        """
        x = 1
        symbols = ("b", "0", "1")
        while True:
            if not f'label_state{x}' in self.__dict__.keys():
                for i in range(3):
                    self.__dict__[f"label_state{x}"] = tk.Label(
                        self.scroll_frame, text=f"{x}"
                    )
                    self.__dict__[f"label_state{x}"].grid(
                        row=3 * x - 1, column=0, sticky='nesw'
                    )
                    tk.Label(self.scroll_frame, text='||').grid(
                        row=3 * x, column=0, sticky='nesw'
                    )
                    tk.Label(self.scroll_frame, text='||').grid(
                        row=3 * x - 2, column=0, sticky='nesw'
                    )

                    self.__dict__[f"label_read{x}_{symbols[i]}"] = tk.Label(
                        self.scroll_frame, text=f"{symbols[i]}"
                    )
                    self.__dict__[f"label_read{x}_{symbols[i]}"].grid(
                        row=3 * x - 2 + i, column=1, sticky='nesw'
                    )

                    self.__dict__[f"label_write{x}_{symbols[i]}"] = tk.Label(
                        self.scroll_frame, text=f"{instructions[symbols[i]][0]}"
                    )
                    self.__dict__[f"label_write{x}_{symbols[i]}"].grid(
                        row=3 * x - 2 + i, column=2, sticky='nesw'
                    )

                    self.__dict__[f"label_move{x}_{symbols[i]}"] = tk.Label(
                        self.scroll_frame, text=f"{instructions[symbols[i]][1]}"
                    )
                    self.__dict__[f"label_move{x}_{symbols[i]}"].grid(
                        row=3 * x - 2 + i, column=3, sticky='nesw'
                    )

                    self.__dict__[f"label_new_state{x}_{symbols[i]}"] = tk.Label(
                        self.scroll_frame, text=f'{instructions[symbols[i]][2]}'
                    )
                    self.__dict__[f"label_new_state{x}_{symbols[i]}"].grid(
                        row=3 * x - 2 + i, column=4, sticky='nesw'
                    )

                break
            x += 1

    def draw_cell(self, canvas: tk.Canvas, x: int, y: int, radius: int, color: str) -> None:
        """Draw a cell on the canvas.

        Args:
            canvas (tk.Canvas): The canvas on which the cell is drawn.
            x (int): The x-coordinate of the cell's center.
            y (int): The y-coordinate of the cell's center.
            radius (int): The radius of the cell.
            color (str): The color of the cell.
        """
        canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            width=0, fill=f'{color}'
        )

    def setup_scrollable_area(self, parent: tk.Frame, width: int) -> None:
        """Set up a scrollable area for displaying states.

        Args:
            parent (tk.Frame): The parent widget for the scrollable area.
            width (int): The width of the scrollable area.
        """
        self.scroll_canvas = tk.Canvas(
            parent, width=int(width / 7), bg='gray94'
        )
        self.scrollbar = tk.Scrollbar(
            parent, orient="vertical", command=self.scroll_canvas.yview
        )
        self.scroll_frame = tk.Frame(self.scroll_canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")
            )
        )

        self.scroll_canvas.create_window(
            (0, 0), window=self.scroll_frame, anchor="nw", width=int(width / 6)
        )
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

    def change_language(self, language: str) -> None:
        """Change the application's language.

        Args:
            language (str): The language code for the change.
        """
        with open(self.config_file, "w") as config_file:
            self.config["language"] = language
            json.dump(self.config, config_file)
        self.restart_application()

    def update_colors(self, highlight_color: str, blank_color: str,
                      zero_color: str, one_color: str) -> None:
        """Update the interface colors.

        Args:
            highlight_color (str): The highlight color.
            blank_color (str): The blank cell color.
            zero_color (str): The zero cell color.
            one_color (str): The one cell color.
        """
        with open(self.config_file, "w") as config_file:
            self.config["color_highlight"] = highlight_color
            self.config["color_blank"] = blank_color
            self.config["color_zero"] = zero_color
            self.config["color_one"] = one_color
            json.dump(self.config, config_file)
        self.restart_application()

    def open_config_editor(self) -> None:
        """Open the configuration editor window."""
        config_window = tk.Toplevel(self.root)
        config_window.attributes('-topmost', 'true')
        self.root.eval(f'tk::PlaceWindow {str(config_window)} center')
        tk.Label(config_window, text=i18n.t("config_editor")).pack()

        tk.Label(config_window, text=i18n.t("color_highlight")).pack()
        highlight_color_entry = tk.Entry(config_window)
        highlight_color_entry.pack()
        highlight_color_entry.insert(0, self.color_highlight)

        tk.Label(config_window, text=i18n.t("color_blank")).pack()
        blank_color_entry = tk.Entry(config_window)
        blank_color_entry.pack()
        blank_color_entry.insert(0, self.color_blank)

        tk.Label(config_window, text=i18n.t("color_zero")).pack()
        zero_color_entry = tk.Entry(config_window)
        zero_color_entry.pack()
        zero_color_entry.insert(0, self.color_zero)

        tk.Label(config_window, text=i18n.t("color_one")).pack()
        one_color_entry = tk.Entry(config_window)
        one_color_entry.pack()
        one_color_entry.insert(0, self.color_one)

        tk.Button(
            config_window, text=i18n.t("save"),
            command=lambda: self.update_colors(
                highlight_color_entry.get(),
                blank_color_entry.get(),
                zero_color_entry.get(),
                one_color_entry.get()
            )
        ).pack()
        tk.Button(
            config_window, text=i18n.t("cancel"),
            command=config_window.destroy
        ).pack()

    def restart_application(self) -> None:
        """Restart the application after configuration changes."""
        restart_window = tk.Toplevel(self.root)
        restart_window.attributes('-topmost', 'true')
        self.root.eval(f'tk::PlaceWindow {str(restart_window)} center')
        tk.Label(restart_window, text=i18n.t("restart_required")).pack()
        tk.Button(
            restart_window, text=i18n.t("indeed"),
            command=lambda: os.execv(sys.executable, ['python'] + sys.argv)
        ).pack()
        tk.Button(
            restart_window, text=i18n.t("please_no"),
            command=restart_window.destroy
        ).pack()


if __name__ == '__main__':
    app = TuringMachineApp()
    app.root.mainloop()
