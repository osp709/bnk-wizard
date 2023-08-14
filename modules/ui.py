"""
Module for buiding the application's UI
"""

import tkinter as tk
from typing import Callable, Any, List
from tkinter import ttk, filedialog, messagebox
from pygame import mixer
from PIL import Image, ImageTk
from modules.bnkwizard import BNKWizard
from modules.audioutils import play_wem_audio, stop_wem_audio


class UserInterfaceElements:
    """
    Class to create UI elements
    """

    def create_root(self, title: str):
        """Create Root"""
        root = tk.Tk()
        root.title(title)
        return root

    def load_image(self, file: str, size: int):
        """Load Tk PhotoImage"""
        img = Image.open(file)
        return ImageTk.PhotoImage(img.resize((size, size), Image.Resampling.LANCZOS))

    def create_frame(self, root: tk.Tk):
        """Create Frame"""
        frame = ttk.Frame(root)
        return frame

    def create_checkbox(
        self,
        root: tk.Tk,
        text: str,
        var_type: Callable,
        def_val: Any,
    ):
        """Create Checkbox"""
        var = var_type(root, value=def_val)
        btn = ttk.Checkbutton(master=root, text=text, variable=var)
        return var, btn

    def create_label(self, root: tk.Tk, text: str):
        """Create Label"""
        lbl = ttk.Label(master=root, text=text)
        return lbl

    def create_button(
        self,
        root: tk.Tk,
        text: str,
        image: tk.PhotoImage,
        command: Callable,
        disabled: bool = False,
    ):
        """Create Button"""
        if image:
            btn = ttk.Button(
                master=root, text=text, image=image, compound=tk.LEFT, command=command
            )
            btn.image = image
        else:
            btn = ttk.Button(master=root, text=text, command=command)
        if disabled:
            btn["state"] = tk.DISABLED
        return btn

    def create_option(self, root: tk.Tk, option_list: List[str]):
        """Create Button"""
        opt = ttk.Combobox(master=root, *option_list)
        opt["state"] = "readonly"
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
            self.root, text="OPEN BNK", command=self.read_base_bnk, image=None
        )
        self.open_bnk_button.grid(row=0, column=0, padx=(10, 5), pady=(10, 10))
        self.save_bnk_button = ui_elem.create_button(
            self.root, text="SAVE BNK", command=self.write_new_bnk, image=None
        )
        self.wem_edit_btns = {}
        self.save_bnk_button["state"] = tk.DISABLED
        self.save_bnk_button.grid(row=0, column=1, padx=(5, 10), pady=(10, 10))

        top_wem_sep = ttk.Separator(
            self.root,
            orient=tk.HORIZONTAL,
        )
        top_wem_sep.grid(
            row=1, column=0, columnspan=6, sticky=tk.NSEW, padx=(5, 5), pady=(5, 5)
        )

        self.wem_id_list = ui_elem.create_option(
            self.root, self.bnkwizard.wem_array.wem_ids
        )
        self.wem_id_list.grid(
            row=2, column=0, sticky=tk.EW, padx=(10, 10), pady=(10, 10)
        )
        self.wem_id_list.set("All Id List")
        self.rep_wem_id_list = ui_elem.create_option(
            self.root, list(self.bnkwizard.wem_array.rep_wem_ids)
        )
        self.rep_wem_id_list.grid(
            row=3, column=0, sticky=tk.EW, padx=(10, 10), pady=(10, 10)
        )
        self.rep_wem_id_list.set("Replaced Id List")

        wem_btns_frame = ui_elem.create_frame(self.root)
        wem_btns_frame.grid(row=2, column=1, rowspan=2, columnspan=2)
        self.wem_edit_btns["play"] = ui_elem.create_button(
            wem_btns_frame,
            text="Play",
            image=ui_elem.load_image(file="assets\\play_black.png", size=24),
            command=self.play_audio,
            disabled=True,
        )
        self.wem_edit_btns["play"].grid(row=2, column=1, padx=(10, 5), pady=(10, 10))
        self.wem_edit_btns["stop"] = ui_elem.create_button(
            wem_btns_frame,
            text="Stop",
            image=ui_elem.load_image(file="assets\\stop_black.png", size=24),
            command=stop_wem_audio,
            disabled=True,
        )
        self.wem_edit_btns["stop"].grid(row=2, column=2, padx=(5, 10), pady=(10, 10))
        self.wem_edit_btns["replace"] = ui_elem.create_button(
            wem_btns_frame,
            text="Replace",
            image=ui_elem.load_image(file="assets\\replace_black.png", size=24),
            command=self.add_wem_replacement,
            disabled=True,
        )
        self.wem_edit_btns["replace"].grid(row=3, column=1, padx=(10, 5), pady=(10, 10))
        self.wem_edit_btns["remove"] = ui_elem.create_button(
            wem_btns_frame,
            text="Undo",
            image=ui_elem.load_image(file="assets\\clear_black.png", size=24),
            command=self.remove_wem_replacement,
            disabled=True,
        )
        self.wem_edit_btns["remove"].grid(row=3, column=2, padx=(5, 10), pady=(10, 10))
        self.root.resizable(False, False)
        for i in range(self.root.grid_size()[0]):
            self.root.grid_columnconfigure(i, weight=1)

        self.root.mainloop()

    def read_base_bnk(self):
        """Get the Base BNK file"""
        src_bnkfile = filedialog.askopenfilename(
            filetypes=[("WWise Bank Files", ".bnk")]
        )
        if src_bnkfile != "":
            self.save_bnk_button["state"] = tk.ACTIVE
            for btn in self.wem_edit_btns.values():
                btn["state"] = tk.ACTIVE
            self.bnkwizard.read_bnk(src_bnkfile, self.little_endian)
            self.wem_id_list["values"] = self.bnkwizard.wem_array.wem_ids
            self.wem_id_list.set(self.bnkwizard.wem_array.wem_ids[0])
            self.rep_wem_id_list.set("")

    def play_audio(self):
        """Play selected audio"""
        sel_id = int(self.wem_id_list.get()) if self.wem_id_list.get() else -1
        if sel_id in self.bnkwizard.wem_array.wem_ids:
            wem_data = self.bnkwizard.wem_array.get_wem(sel_id)
            play_wem_audio(wem_data)

    def add_wem_replacement(self):
        """Edit the selected wem"""
        wem_id = int(self.wem_id_list.get()) if self.wem_id_list.get() else -1
        if wem_id in self.bnkwizard.wem_array.wem_ids:
            new_wemfile = filedialog.askopenfilename(
                filetypes=[("Audio Files", ".wem .wav .mp3")]
            )
            if new_wemfile != "":
                self.bnkwizard.wem_array.make_replacement(wem_id, new_wemfile)
                rep_list = list(self.bnkwizard.wem_array.rep_wem_ids)
                self.rep_wem_id_list["values"] = rep_list
                self.rep_wem_id_list.set(rep_list[0])

    def remove_wem_replacement(self):
        """Remove replacment wem"""
        sel_id = int(self.rep_wem_id_list.get()) if self.rep_wem_id_list.get() else -1
        if sel_id in self.bnkwizard.wem_array.rep_wem_ids:
            self.bnkwizard.wem_array.remove_replacement(sel_id)
            rep_list = list(self.bnkwizard.wem_array.rep_wem_ids)
            self.rep_wem_id_list["values"] = list(self.bnkwizard.wem_array.rep_wem_ids)
            self.rep_wem_id_list.set(rep_list[0] if len(rep_list) > 0 else "")

    def write_new_bnk(self):
        """Write the Base BNK file"""
        dst_bnkfile = filedialog.asksaveasfilename(
            defaultextension=".bnk", filetypes=[("WWise Bank Files", ".bnk")]
        )
        if dst_bnkfile != "":
            self.bnkwizard.write_bnk(dst_bnkfile, self.little_endian)
            messagebox.showinfo("BNK Wizard", "File Saved!")
