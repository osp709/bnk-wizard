"""
Module for buiding the application's UI
"""

import tkinter as tk
from typing import Callable, Any, List
from tkinter import ttk, filedialog, messagebox
from pygame import mixer
from PIL import Image, ImageTk
from modules.bnkwizard import BNKWizard
from modules.audioutils import play_wem_audio, stop_wem_audio, save_wem_to_file
import os


class UserInterfaceElements:
    """Class to create UI elements"""

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

    def create_combobox(self, root: tk.Tk, option_list: List[str]):
        """Create Combobox"""
        opt = ttk.Combobox(master=root, *option_list)
        opt["state"] = "readonly"
        return opt

    def create_tree(self, root: tk.Tk, columns: [], headings: []):
        """Create Tree"""
        tree = ttk.Treeview(root, columns=columns, show="headings")
        for col, head in zip(columns, headings):
            tree.heading(col, text=head)
        return tree


class Application:
    """Class for buiding the application's interface"""

    def __init__(self):
        mixer.init()
        self.bnkwizard = BNKWizard()
        ui_elem = UserInterfaceElements()
        self.root = ui_elem.create_root("BNK Wizard")

        self.all_btns = {}
        self.all_btns["open"] = ui_elem.create_button(
            self.root,
            text="Open Bank",
            image=ui_elem.load_image(file="assets\\open.png", size=16),
            command=self.read_base_bnk,
        )
        self.all_btns["open"].grid(row=0, column=0, padx=(10, 5), pady=(10, 10))
        self.all_btns["export"] = ui_elem.create_button(
            self.root,
            text="Export Bank",
            image=ui_elem.load_image(file="assets\\export.png", size=16),
            command=self.write_new_bnk,
            disabled=True,
        )
        self.all_btns["export"].grid(row=0, column=1, padx=(5, 5), pady=(10, 10))
        self.all_btns["playo"] = ui_elem.create_button(
            self.root,
            text="Play(O)",
            image=ui_elem.load_image(file="assets\\play.png", size=16),
            command=lambda: self.play_audio(False),
            disabled=True,
        )
        self.all_btns["playo"].grid(row=0, column=2, padx=(5, 5), pady=(10, 10))
        self.all_btns["playr"] = ui_elem.create_button(
            self.root,
            text="Play(R)",
            image=ui_elem.load_image(file="assets\\play.png", size=16),
            command=lambda: self.play_audio(True),
            disabled=True,
        )
        self.all_btns["playr"].grid(row=0, column=3, padx=(5, 10), pady=(10, 10))
        self.all_btns["save"] = ui_elem.create_button(
            self.root,
            text="Save",
            image=ui_elem.load_image(file="assets\\save.png", size=16),
            command=self.save_wem,
            disabled=True,
        )
        self.all_btns["save"].grid(row=1, column=0, padx=(10, 5), pady=(10, 10))
        self.all_btns["replace"] = ui_elem.create_button(
            self.root,
            text="Replace",
            image=ui_elem.load_image(file="assets\\replace.png", size=16),
            command=self.add_wem_replacement,
            disabled=True,
        )
        self.all_btns["replace"].grid(row=1, column=1, padx=(5, 5), pady=(10, 10))
        self.all_btns["remove"] = ui_elem.create_button(
            self.root,
            text="Undo",
            image=ui_elem.load_image(file="assets\\clear.png", size=16),
            command=self.remove_wem_replacement,
            disabled=True,
        )
        self.all_btns["remove"].grid(row=1, column=2, padx=(5, 5), pady=(10, 10))
        self.all_btns["stop"] = ui_elem.create_button(
            self.root,
            text="Stop",
            image=ui_elem.load_image(file="assets\\stop.png", size=16),
            command=stop_wem_audio,
            disabled=True,
        )
        self.all_btns["stop"].grid(row=1, column=3, padx=(5, 10), pady=(10, 10))
        top_wem_sep = ttk.Separator(
            self.root,
            orient=tk.HORIZONTAL,
        )
        top_wem_sep.grid(
            row=2, column=0, columnspan=8, sticky=tk.NSEW, padx=(5, 5), pady=(5, 5)
        )
        self.wem_tree = ui_elem.create_tree(
            self.root,
            columns=[
                "id",
                "orig_wem",
                "repl_wem",
            ],
            headings=["ID", "Original Wem", "Replacement Wem"],
        )
        self.wem_tree.grid(
            row=4, column=0, columnspan=4, sticky=tk.NSEW, padx=(10, 0), pady=(10, 10)
        )

        scrollbar = ttk.Scrollbar(
            self.root, orient=tk.VERTICAL, command=self.wem_tree.yview
        )
        self.wem_tree.configure(yscroll=scrollbar.set)
        self.wem_tree.bind("<<TreeviewSelect>>", self.enable_play_repl_button)
        scrollbar.grid(row=4, column=4, sticky=tk.NS, padx=(0, 10), pady=(10, 10))
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
            for item in self.wem_tree.get_children():
                self.wem_tree.delete(item)
            self.bnkwizard = BNKWizard()
            for btn_name, btn in self.all_btns.items():
                if btn_name != "playr":
                    btn["state"] = tk.NORMAL
            self.bnkwizard.read_bnk(src_bnkfile, True)
            for itr, wem_id in enumerate(self.bnkwizard.wem_array.wem_ids):
                self.wem_tree.insert(
                    "",
                    tk.END,
                    values=(
                        wem_id,
                        str(itr + 1).zfill(len(str(self.bnkwizard.wem_array.wem_count)))
                        + ".bnk",
                        "",
                    ),
                )

    def save_wem(self):
        """Save wem to file"""
        if self.wem_tree.focus() != "":
            sel_wem_data = self.wem_tree.item(self.wem_tree.focus())
            sel_id = sel_wem_data["values"][0]
            if sel_id in self.bnkwizard.wem_array.wem_ids:
                wem_data = self.bnkwizard.wem_array.get_wem(sel_id)
                wem_filename = filedialog.asksaveasfilename(
                    filetypes=[
                        ("wem Audio", ".wem"),
                        ("wav Audio", ".wav"),
                    ],
                    initialfile=str(wem_data.wem_id),
                    defaultextension=".wem",
                )
                res = 0
                if wem_filename != "" and wem_filename.endswith((".wem", ".wav")):
                    res = save_wem_to_file(wem_data.data, wem_filename)
                if res:
                    messagebox.showinfo("BNK Wizard", "File saved!")
                else:
                    messagebox.showerror("BNK Wizard", "Error saving file!")
            else:
                messagebox.showerror("BNK Wizard", "Wrong filename given!")

    def enable_play_repl_button(self, event):
        """Enable replacement play button"""
        if event:
            if self.wem_tree.focus() != "":
                sel_wem_data = self.wem_tree.item(self.wem_tree.focus())["values"]
                sel_id = sel_wem_data[0]
                if sel_id in self.bnkwizard.wem_array.rep_wem_ids:
                    self.all_btns["playr"]["state"] = tk.NORMAL
                else:
                    self.all_btns["playr"]["state"] = tk.DISABLED

    def play_audio(self, repl=False):
        """Play selected audio"""
        if self.wem_tree.focus() != "":
            sel_wem_data = self.wem_tree.item(self.wem_tree.focus())
            sel_id = sel_wem_data["values"][0]
            if sel_id in self.bnkwizard.wem_array.wem_ids:
                wem_data = self.bnkwizard.wem_array.get_wem(sel_id, repl)
                play_wem_audio(wem_data)

    def add_wem_replacement(self):
        """Edit the selected wem"""
        if self.wem_tree.focus() != "":
            sel_wem_data = self.wem_tree.item(self.wem_tree.focus())["values"]
            sel_id = sel_wem_data[0]
            if sel_id in self.bnkwizard.wem_array.wem_ids:
                new_wemfile = filedialog.askopenfilename(
                    filetypes=[("Audio Files", ".wem .wav .mp3 .ogg")]
                )
                if new_wemfile != "":
                    self.bnkwizard.wem_array.make_replacement(sel_id, new_wemfile)
                    new_wem_data = list(sel_wem_data)
                    new_wem_data[2] = os.path.basename(new_wemfile)
                    print(tuple(new_wem_data))
                    self.wem_tree.item(
                        self.wem_tree.focus(), values=tuple(new_wem_data)
                    )
                    self.all_btns["playr"]["state"] = tk.NORMAL

    def remove_wem_replacement(self):
        """Remove replacment wem"""
        if self.wem_tree.focus() != "":
            sel_wem_data = self.wem_tree.item(self.wem_tree.focus())["values"]
            sel_id = sel_wem_data[0]
            if sel_id in self.bnkwizard.wem_array.rep_wem_ids:
                self.bnkwizard.wem_array.remove_replacement(sel_id)
                new_wem_data = list(sel_wem_data)
                new_wem_data[2] = ""
                sel_id = sel_wem_data[0]
                self.wem_tree.item(self.wem_tree.focus(), values=tuple(new_wem_data))
                self.all_btns["playr"]["state"] = tk.DISABLED

    def write_new_bnk(self):
        """Write the Base BNK file"""
        dst_bnkfile = filedialog.asksaveasfilename(
            defaultextension=".bnk", filetypes=[("WWise Bank Files", ".bnk")]
        )
        if dst_bnkfile != "":
            self.bnkwizard.write_bnk(dst_bnkfile, True)
            messagebox.showinfo("BNK Wizard", "File Saved!")
