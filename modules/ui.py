"""
Module for buiding the application's UI
"""

import tkinter as tk
import tkinter.font as font
from dataclasses import dataclass
from tkinter.filedialog import askopenfilename
from modules.bnkwizard import BNKWizard


class UI:

    """
    Class for buiding the application's UI
    """

    @dataclass
    class WEMUI:
        """
        WEM UI Element
        """

        display_label: tk.Label
        edit_btn: tk.Button
        replace_label: tk.Label
        remove_btn: tk.Button

        def __init__(self):
            pass

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BNK Wizard")
        self.root.configure(bg="black")
        self.bnkwizard = BNKWizard()
        self.background = "black"
        self.bg_button_color = self.background
        self.bg_checkbox_color = self.background
        self.bg_label_color = "blue"
        self.fg_button_color = "aqua"
        self.fg_checkbox_color = "yellow"
        self.fg_label_color = "white"
        self.wem_ui_list = []
        self.src_bnkfile = ""
        self.top_font_settings = font.Font(family="Helvetica", size=12)
        self.wem_font_settings = font.Font(family="Helvetica", size=16)

        self.little_endian = tk.BooleanVar(self.root)
        self.little_endian.set(True)
        self.little_endian_check = tk.Checkbutton(
            self.root,
            text="Little Endian",
            background=self.background,
            activebackground=self.bg_button_color,
            activeforeground=self.fg_checkbox_color,
            foreground=self.fg_checkbox_color,
            selectcolor=self.bg_button_color,
            variable=self.little_endian,
            font=self.top_font_settings,
        )
        self.little_endian_check.grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=(10, 10),
        )
        self.open_bnk_button = tk.Button(
            self.root,
            text="OPEN BNK",
            background=self.bg_button_color,
            foreground=self.fg_button_color,
            activeforeground=self.fg_button_color,
            activebackground=self.bg_button_color,
            command=self.read_base_bnk,
            font=self.top_font_settings,
        )
        self.open_bnk_button.grid(row=0, column=3, padx=(10, 5), pady=(10, 10))
        self.save_bnk_button = tk.Button(
            self.root,
            text="SAVE BNK",
            background=self.bg_button_color,
            foreground=self.fg_button_color,
            activeforeground=self.fg_button_color,
            activebackground=self.bg_button_color,
            state="disabled",
            command=self.write_new_bnk,
            font=self.top_font_settings,
        )
        self.save_bnk_button.grid(
            row=0,
            column=5,
            padx=(5, 10),
            pady=(10, 10),
        )
        self.root.resizable(False, False)

        self.wem_array_frame = tk.Frame(self.root, bg="blue")
        self.wem_array_frame.grid(row=1, column=3, padx=(10, 10), pady=(0, 10))

    def read_base_bnk(self):
        """
        Get the Base BNK file
        """
        self.src_bnkfile = askopenfilename(filetypes=[("WWise Bank Files", ".bnk")])
        if self.src_bnkfile != "":
            if self.save_bnk_button["state"] == tk.DISABLED:
                self.save_bnk_button["state"] = tk.ACTIVE
            self.bnkwizard.read_bnk(self.src_bnkfile, self.little_endian)
            edit_image = tk.PhotoImage(file="assets/edit.png")
            remove_img = tk.PhotoImage(file="assets/remove.png")
            for i in range(5):
                wem = self.bnkwizard.wem_array.wems[i]
                wem_ui = self.WEMUI()
                wem_ui.display_label = tk.Label(
                    self.wem_array_frame,
                    text=str(wem.wem_id) + ".bnk",
                    foreground=self.fg_label_color,
                    background=self.bg_label_color,
                    font=self.wem_font_settings,
                )
                wem_ui.display_label.grid(row=i, column=0, padx=(10, 5), pady=(5, 5))
                wem_ui.edit_btn = tk.Button(
                    self.wem_array_frame,
                    image=edit_image,
                    background=self.bg_button_color,
                    foreground=self.fg_button_color,
                    activeforeground=self.fg_button_color,
                    activebackground=self.bg_button_color,
                )
                wem_ui.edit_btn.image = edit_image
                wem_ui.edit_btn.grid(row=i, column=1, padx=(5, 5), pady=(5, 5))
                wem_ui.replace_label = tk.Label(
                    self.wem_array_frame,
                    text="",
                    foreground=self.fg_label_color,
                    background=self.bg_label_color,
                    font=self.wem_font_settings,
                )
                wem_ui.replace_label.grid(row=i, column=2, padx=(5, 5), pady=(5, 5))
                wem_ui.remove_btn = tk.Button(
                    self.wem_array_frame,
                    image=remove_img,
                    background=self.bg_button_color,
                    foreground=self.fg_button_color,
                    activeforeground=self.fg_button_color,
                    activebackground=self.bg_button_color,
                )
                wem_ui.remove_btn.image = remove_img
                wem_ui.remove_btn.grid(row=i, column=3, padx=(5, 5), pady=(5, 5))

    def write_new_bnk(self):
        """
        Write the Base BNK file
        """
