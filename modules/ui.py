"""
Module for buiding the application's UI
"""

import tkinter as tk
import subprocess
import tempfile
import os
from typing import Callable, Any, List
from tkinter import ttk, filedialog, messagebox
from pygame import mixer
from modules.bnkwizard import BNKWizard


class UserInterfaceElements:
    """
    Class to create UI elements
    """

    def create_root(self, title: str):
        """Create Root"""
        root = tk.Tk()
        root.title(title)
        return root

    def create_checkbox(self, root: tk.Tk, text: str, var_type: Callable, def_val: Any):
        """Create Checkbox"""
        var = var_type(root, value=def_val)
        btn = ttk.Checkbutton(master=root, text=text, variable=var)
        return var, btn

    def create_label(self, root: tk.Tk, text: str):
        """Create Label"""
        lbl = ttk.Label(master=root, text=text)
        return lbl

    def create_button(self, root: tk.Tk, text: str, command: Callable):
        """Create Button"""
        btn = ttk.Button(master=root, text=text, command=command)
        return btn

    def create_option(self, root: tk.Tk, option_list: List[str]):
        """Create Button"""
        opt = ttk.Combobox(master=root, *option_list)
        return opt


class Application:
    """
    Class for buiding the application's interface
    """

    def __init__(self):
        mixer.init()
        self.bnkwizard = BNKWizard()
        ui_elem = UserInterfaceElements()
        self.root = ui_elem.create_root("BNK Wizard")

        self.little_endian, self.little_endian_check = ui_elem.create_checkbox(
            self.root, "Little Endian", tk.BooleanVar, 1
        )
        self.little_endian_check.grid(row=0, column=2, padx=(10, 5), pady=(10, 10))

        self.open_bnk_button = ui_elem.create_button(
            self.root,
            text="OPEN BNK",
            command=self.read_base_bnk,
        )
        self.open_bnk_button.grid(row=0, column=0, padx=(10, 5), pady=(10, 10))
        self.save_bnk_button = ui_elem.create_button(
            self.root,
            text="SAVE BNK",
            command=self.write_new_bnk,
        )
        self.save_bnk_button["state"] = tk.DISABLED
        self.save_bnk_button.grid(row=0, column=1, padx=(5, 10), pady=(10, 10))

        top_wem_sep = ttk.Separator(
            self.root,
            orient=tk.HORIZONTAL,
        )
        top_wem_sep.grid(
            row=1, column=0, columnspan=6, sticky=tk.NSEW, padx=(5, 5), pady=(5, 5)
        )

        self.edit_wem_opt = ui_elem.create_option(
            self.root, self.bnkwizard.wem_array.wem_ids
        )
        self.edit_wem_opt.grid(
            row=2, column=0, columnspan=2, sticky=tk.EW, padx=(10, 10), pady=(10, 10)
        )
        self.edit_wem_opt["state"] = "readonly"
        self.play_btn = ui_elem.create_button(self.root, "Play Audio", self.play_audio)
        self.play_btn.grid(row=2, column=2, padx=(10, 10), pady=(10, 10))
        self.root.resizable(False, False)
        for i in range(self.root.grid_size()[0]):
            self.root.grid_columnconfigure(i, weight=1)

        self.root.mainloop()

    def read_base_bnk(self):
        """
        Get the Base BNK file
        """
        src_bnkfile = filedialog.askopenfilename(
            filetypes=[("WWise Bank Files", ".bnk")]
        )
        if src_bnkfile != "":
            self.save_bnk_button["state"] = tk.ACTIVE
            self.bnkwizard.read_bnk(src_bnkfile, self.little_endian)
            self.edit_wem_opt["values"] = self.bnkwizard.wem_array.wem_ids
            self.edit_wem_opt.set(self.bnkwizard.wem_array.wem_ids[0])

    def play_audio(self):
        """
        Play selected audio
        """
        sel_id = int(self.edit_wem_opt.get())
        if sel_id in self.bnkwizard.wem_array.wem_ids:
            wem_data = self.bnkwizard.wem_array.get_wem(sel_id)
            wem_filename = tempfile.gettempdir() + "\\temp.wem"
            with open(wem_filename, mode="wb") as wem_file:
                wem_file.write(wem_data.data)
            try:
                mixer.music.unload()
            finally:
                pass
            try:
                wav_filename = wem_filename.split(".wem")[0] + ".wav"
                subprocess.check_call(
                    [
                        r"modules\\vgmstream-win64\\vgmstream-cli.exe",
                        "-o",
                        wav_filename,
                        wem_filename,
                    ]
                )
                mixer.music.load(wav_filename)
                mixer.music.play(0)
            except subprocess.CalledProcessError as err:
                print(err.output)
            except Exception as err:
                print(err)

    def write_new_bnk(self):
        """
        Write the Base BNK file
        """
        dst_bnkfile = filedialog.asksaveasfilename(
            defaultextension=".bnk", filetypes=[("WWise Bank Files", ".bnk")]
        )

        self.bnkwizard.write_bnk(dst_bnkfile, self.little_endian)
        messagebox.showinfo("BNK Wizard", "File Saved!")
