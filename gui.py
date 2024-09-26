import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import webbrowser
import json
import os
from file_organizer import monitor_browsers_and_start

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("600x660")
        self.resizable(False, False)


        self.icon_path = 'images/icon.ico'
        self.iconbitmap(self.icon_path)

        self.folders_to_track = []
        self.formats_to_organize = {
            "PDFs": ["pdf"],
            "Images": ["image"],
            "Web Files": ["html"],
            "Text Files": ["text", "csv", "sql"],
            "Spreadsheets": ["spreadsheet"],
            "Presentations": ["presentation"],
            "Audio": ["audio"],
            "Videos": ["video"],
            "Fonts": ["font"],
            "Archives": ["compressed", "zip", "rar", "7z"],
            "Executables": ["executable", "msi", "exe"],
            "Scripts": ["script", "javascript"],
            "Word Documents": ["word"]
        }
        self.selected_formats = {key: tk.BooleanVar(value=True) for key in self.formats_to_organize.keys()}

        self.create_widgets()
        self.load_preferences()

        self.file_organizer_thread = None  # Thread object to hold the file organizer process

    def create_widgets(self):
        self.style = ttk.Style(self)

        tk.Label(self, text="Tracked Folders", font=("Helvetica", 14, "bold")).pack(pady=10)

        self.folder_frame = ttk.Frame(self)
        self.folder_frame.pack(pady=10, fill="x", padx=20)

        self.folder_listbox = tk.Listbox(self.folder_frame, height=5)
        self.folder_listbox.pack(side="left", fill="x", expand=True)

        self.add_folder_button = ttk.Button(self.folder_frame, text="Add Folder", command=self.add_folder)
        self.add_folder_button.pack(side="top", padx=5)

        self.remove_folder_button = ttk.Button(self.folder_frame, text="Remove Folder", command=self.remove_folder)
        self.remove_folder_button.pack(side="bottom", padx=5)

        tk.Label(self, text="Formats", font=("Helvetica", 14, "bold")).pack(pady=10)

        self.format_frame = ttk.Frame(self)
        self.format_frame.pack(pady=10, fill="x", padx=20)

        row, col = 0, 0
        for format_group in self.formats_to_organize.keys():
            chk = ttk.Checkbutton(self.format_frame, text=format_group, variable=self.selected_formats[format_group])
            chk.grid(row=row, column=col, sticky='w', padx=10, pady=5)
            col += 1
            if col == 2:
                col = 0
                row += 1

        self.remember_var = tk.BooleanVar(value=True)

        remember_check = ttk.Checkbutton(self, text="Remember Folders", variable=self.remember_var)
        remember_check.pack(pady=10)

        self.start_button = ttk.Button(self, text="Start Organizer", command=self.start_organizer)
        self.start_button.pack(pady=20)

        self.stop_button = ttk.Button(self, text="Stop Organizer", command=self.stop_organizer, state=tk.DISABLED)
        self.stop_button.pack(pady=0)

        github_watermark = tk.Button(self, text="Github", relief='flat', font=("Helvetica", 8), fg="blue", borderwidth=0, command= lambda: webbrowser.open("https://www.github.com/specialspicy"))
        github_watermark.pack(side="bottom", anchor="se", padx=10, pady=0) 

        name_watermark = tk.Label(self, text="Houman Hafez", font=("Helvetica", 8), anchor="se")
        name_watermark.pack(side="bottom", anchor="se", padx=10, pady=0)



    def add_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folders_to_track.append(folder_path)
            self.folder_listbox.insert(tk.END, folder_path)

    def remove_folder(self):
        selected = self.folder_listbox.curselection()
        if selected:
            folder_path = self.folder_listbox.get(selected)
            self.folders_to_track.remove(folder_path)
            self.folder_listbox.delete(selected)

    def start_organizer(self):
        if not self.folders_to_track:
            messagebox.showerror("Error", "Please add at least one folder to track.")
            return
        formats_to_organize = {k: v for k, v in self.formats_to_organize.items() if self.selected_formats[k].get()}
        if self.remember_var.get():
            self.save_preferences()

        # Start file organizer in a separate thread
        self.file_organizer_thread = threading.Thread(target=self.monitor_and_start, args=(formats_to_organize,), daemon=True)
        self.file_organizer_thread.start()

        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        messagebox.showinfo("Info", "File Organizer started. Monitoring for browser and organizing files in background.")

    def monitor_and_start(self, formats_to_organize):
        monitor_browsers_and_start(self.folders_to_track, formats_to_organize)

    def stop_organizer(self):
        if self.file_organizer_thread and self.file_organizer_thread.is_alive():
            self.file_organizer_thread.join(timeout=1)
            if self.file_organizer_thread.is_alive():
                messagebox.showwarning("Warning", "File organizer thread did not stop gracefully.")
        else:
            messagebox.showinfo("Info", "File Organizer is not running.")

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        if hasattr(self, "stop_button"):
            self.stop_button.pack_forget()  # Remove the Stop button from view
        self.start_button = ttk.Button(self, text="Start Organizer", command=self.start_organizer)
        self.start_button.pack(pady=20)

    def load_preferences(self):
        if os.path.exists("preferences.json"):
            with open("preferences.json", "r") as file:
                data = json.load(file)
                self.folders_to_track = data.get("folders_to_track", [])
                for folder in self.folders_to_track:
                    self.folder_listbox.insert(tk.END, folder)

    def save_preferences(self):
        data = {
            "folders_to_track": self.folders_to_track
        }
        with open("preferences.json", "w") as file:
            json.dump(data, file)

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
