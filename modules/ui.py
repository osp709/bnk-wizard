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
        self.all_btns["playr"] = ui_elem.create_button(
            self.root,
            text="Play(O)",
            image=ui_elem.load_image(file="assets\\play.png", size=16),
            command=lambda: self.play_audio(False),
            disabled=True,
        )
        self.all_btns["playo"] = ui_elem.create_button(
            self.root,
            text="Play(R)",
            image=ui_elem.load_image(file="assets\\play.png", size=16),
            command=lambda: self.play_audio(False),
            disabled=True,
        )
        self.all_btns["playo"].grid(row=0, column=2, padx=(5, 5), pady=(10, 10))
        self.all_btns["playr"] = ui_elem.create_button(
            self.root,
            text="Play Repl",
            image=ui_elem.load_image(file="assets\\play.png", size=16),
            command=lambda: self.play_audio(False),
            disabled=True,
        )
        self.all_btns["playr"].grid(row=0, column=3, padx=(5, 5), pady=(10, 10))
        self.all_btns["stop"] = ui_elem.create_button(
            self.root,
            text="Stop",
            image=ui_elem.load_image(file="assets\\stop.png", size=16),
            command=stop_wem_audio,
            disabled=True,
        )
        self.all_btns["stop"].grid(row=0, column=4, padx=(5, 5), pady=(10, 10))
        self.all_btns["save"] = ui_elem.create_button(
            self.root,
            text="Save",
            image=ui_elem.load_image(file="assets\\save.png", size=16),
            command=self.save_wem,
            disabled=True,
        )
        self.all_btns["save"].grid(row=0, column=5, padx=(5, 5), pady=(10, 10))
        self.all_btns["replace"] = ui_elem.create_button(
            self.root,
            text="Replace",
            image=ui_elem.load_image(file="assets\\replace.png", size=16),
            command=self.add_wem_replacement,
            disabled=True,
        )
        self.all_btns["replace"].grid(row=0, column=6, padx=(5, 5), pady=(10, 10))
        self.all_btns["remove"] = ui_elem.create_button(
            self.root,
            text="Undo",
            image=ui_elem.load_image(file="assets\\clear.png", size=16),
            command=self.remove_wem_replacement,
            disabled=True,
        )
        self.all_btns["remove"].grid(row=0, column=7, padx=(5, 10), pady=(10, 10))
        top_wem_sep = ttk.Separator(
            self.root,
            orient=tk.HORIZONTAL,
        )
        top_wem_sep.grid(
            row=1, column=0, columnspan=8, sticky=tk.NSEW, padx=(5, 5), pady=(5, 5)
        )

        self.wem_id_list = ui_elem.create_combobox(
            self.root, self.bnkwizard.wem_array.wem_ids
        )
        self.wem_id_list.grid(
            row=2, column=0, columnspan=4, sticky=tk.EW, padx=(10, 10), pady=(10, 10)
        )
        self.wem_id_list.set("All Id List")
        self.rep_wem_id_list = ui_elem.create_combobox(
            self.root, list(self.bnkwizard.wem_array.rep_wem_ids)
        )
        self.rep_wem_id_list.grid(
            row=2, column=4, columnspan=8, sticky=tk.EW, padx=(10, 10), pady=(10, 10)
        )
        self.rep_wem_id_list.set("Replaced Id List")
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
            row=3, column=0, columnspan=8, sticky=tk.EW, padx=(10, 10), pady=(10, 10)
        )
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
            for btn_name, btn in self.all_btns.items():
                if btn_name != "playr":
                    btn["state"] = tk.NORMAL
            self.bnkwizard.read_bnk(src_bnkfile, True)
            self.wem_id_list["values"] = self.bnkwizard.wem_array.wem_ids
            self.wem_id_list.set(self.bnkwizard.wem_array.wem_ids[0])
            self.rep_wem_id_list.set("")

    def save_wem(self):
        """Save wem to file"""

        sel_id = int(self.wem_id_list.get()) if self.wem_id_list.get() else -1
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

    def play_audio(self, repl=False):
        """Play selected audio"""
        sel_id = int(self.wem_id_list.get()) if self.wem_id_list.get() else -1
        if sel_id in self.bnkwizard.wem_array.wem_ids:
            wem_data = self.bnkwizard.wem_array.get_wem(sel_id, repl)
            play_wem_audio(wem_data)

    def add_wem_replacement(self):
        """Edit the selected wem"""
        wem_id = int(self.wem_id_list.get()) if self.wem_id_list.get() else -1
        if wem_id in self.bnkwizard.wem_array.wem_ids:
            new_wemfile = filedialog.askopenfilename(
                filetypes=[("Audio Files", ".wem .wav .mp3 .ogg")]
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
            self.bnkwizard.write_bnk(dst_bnkfile, True)
            messagebox.showinfo("BNK Wizard", "File Saved!")
