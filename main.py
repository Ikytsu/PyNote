import customtkinter
import tkinter
import sys
from tkinter import filedialog
from tkinter import messagebox
import configparser
import os
import integrated_language
import json

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.title("Pynote")
        self.minsize(300, 200)
        self.grid_columnconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.widgets = []

        
        self.config_folder = 'config'
        self.setting_file = os.path.join(self.config_folder, "settings.ini")
        self.translation_folder = os.path.join(self.config_folder, "translations")

        self.languages_dict = dict()

        self.get_languages_dict()

        if os.path.exists(self.setting_file):
            config = configparser.ConfigParser()
            config.read(self.setting_file)

            try:
                self.language = config.get('Settings', 'language')
                if not self.language in list(self.languages_dict.keys()):
                    raise ValueError
                self.default_path = config.get('Settings', 'path')
                self.update_warning = config.getboolean('Settings', 'updatewarning')
                self.main_gui()
            except:
                with open(self.setting_file, "w"):
                    pass
                self.warn(self.get_translation("warn.title.incorrect_settings"), self.get_translation("warn.description.incorrect_settings"))
                self.setup_gui(1)
        else:
            open(self.setting_file, "w").close()
            self.setup_gui(1)
    
    def get_languages_dict(self):
        translation_files = [
            f for f in os.listdir(self.translation_folder)
            if os.path.isfile(os.path.join(self.translation_folder, f)) and f.endswith('.json')
        ]
        
        if translation_files:
            for file in translation_files:
                with open(os.path.join(self.translation_folder, file), 'r') as file:
                    data = json.load(file)
                self.languages_dict[file.name] = data
        self.languages_dict["English"] = integrated_language.english_data

    def get_translation(self, key):
        try:
            language_data = self.languages_dict.get(self.language)
            keys = key.split(".")
            
            result = language_data
            for key_part in keys:
                result = result[key_part]
        except:
            language_data = self.languages_dict.get("English")
            keys = key.split(".")
            
            result = language_data
            for key_part in keys:
                result = result[key_part]
        return result
    
    def warn(self, title: str, message: str):
        messagebox.showwarning(title, message)
    
    def main_gui(self):
        self.text_label = customtkinter.CTkLabel(self, text=self.get_translation("maingui.title"),  font=("Arial", 18))
        self.text_label.grid(row=1, column=0, sticky="nsew")
        self.widgets.append(self.text_label)

    def setup_gui(self, step: int):
        def Next_Button(option: int):
            info = None
            if option == 2:
                for widget in self.widgets:
                    if isinstance(widget, customtkinter.StringVar) and widget.get() == "":
                        self.warn(self.get_translation("warn.title.incorrect_option"), self.get_translation("warn.description.incorrect_option2"))
                        return
            for widget in self.widgets:
                if isinstance(widget, customtkinter.CTkComboBox):
                    info = widget.get()
                elif isinstance(widget, customtkinter.CTkTextbox):
                    info = widget.get("1.0", "end-1c")
                elif isinstance(widget, customtkinter.BooleanVar) or isinstance(widget, customtkinter.StringVar):    
                    info = widget.get()
                if not isinstance(widget, customtkinter.BooleanVar) and not isinstance(widget, customtkinter.StringVar):
                    widget.destroy()
            if option == 1:
                config = configparser.ConfigParser()
                config.read(self.setting_file)
                config.add_section("Settings")
                config.set("Settings", "language", str(info))
                with open(self.setting_file, "w") as configfile:
                    config.write(configfile)
            elif option == 2:
                config = configparser.ConfigParser()
                config.read(self.setting_file)
                config.set("Settings", "path", str(info))
                with open(self.setting_file, "w") as configfile:
                    config.write(configfile)
            elif option == 3:
                config = configparser.ConfigParser()
                config.read(self.setting_file)
                config.set("Settings", "updatewarning", str(info))
                with open(self.setting_file, "w") as configfile:
                    config.write(configfile)
            self.widgets.clear()
            if option != 3: self.setup_gui(option + 1)
            else:  self.main_gui()   
        self.button = customtkinter.CTkButton(self, text=self.get_translation("setup.button"), command=lambda: Next_Button(option=step))
        self.button.grid(row=2, column=0, sticky="se")
        self.widgets.append(self.button)
        if step == 1:
            def on_combobox_change(event):
                self.language = self.combobox.get()
                self.text_label.configure(text = self.get_translation("setup.option1.text_label"))
                self.button.configure(text=self.get_translation("setup.button"))
            self.text_label = customtkinter.CTkLabel(self, text="Choose your language:",  font=("Arial", 18))
            self.text_label.grid(row=1, column=0, sticky="nsew")
            self.widgets.append(self.text_label)
            self.combobox = customtkinter.CTkComboBox(master=self, values=list(self.languages_dict.keys()), state="readonly", command=on_combobox_change)
            self.combobox.grid(row=2, column=0, sticky="n")
            self.combobox.set("English")
            self.widgets.append(self.combobox)
        elif step == 2:
            def Choose_Directory():
                folder_path = filedialog.askdirectory()
                if folder_path:

                    self.text_label2.configure(text= self.get_translation("setup.option2.text_label2_selected") + ' ' + folder_path)
                    self.selected_var.set(folder_path)

            
            self.text_label = customtkinter.CTkLabel(self, text=self.get_translation("setup.option2.text_label"),  font=("Arial", 18))
            self.text_label.grid(row=1, column=0, sticky="nsew")
            self.widgets.append(self.text_label)
            self.selected_var = customtkinter.StringVar()
            self.selected_var.set("")
            self.widgets.append(self.selected_var)
            self.select_button = customtkinter.CTkButton(self, text=self.get_translation("setup.option2.select_button"), command=Choose_Directory)
            self.select_button.grid(row=2, column=0, sticky="n")
            self.widgets.append(self.select_button)
            self.text_label2 = customtkinter.CTkLabel(self, text=self.get_translation("setup.option2.text_label2_notselected"),  font=("Arial", 18))
            self.text_label2.grid(row=2, column=0)
            self.widgets.append(self.text_label2)

        elif step == 3:
            self.text_label = customtkinter.CTkLabel(self, text=self.get_translation("setup.option3.text_label"),  font=("Arial", 18))
            self.text_label.grid(row=1, column=0, sticky="nsew")
            self.widgets.append(self.text_label)
            self.check_var = customtkinter.BooleanVar()
            self.checkbox = customtkinter.CTkCheckBox(self, text="", variable=self.check_var)
            self.widgets.append(self.check_var)
            self.checkbox.grid(row=2, column=0, sticky="n")
            self.widgets.append(self.checkbox)


            
    
app = App()
app.mainloop()
