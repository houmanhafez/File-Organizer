import os
import shutil
import mimetypes
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import psutil
import errno

class FileOrganizerHandler(FileSystemEventHandler):
    def __init__(self, folders_to_track, formats_to_organize):
        self.folders_to_track = folders_to_track
        self.formats_to_organize = formats_to_organize

    def on_modified(self, event):
        for folder_to_track in self.folders_to_track:
            for filename in os.listdir(folder_to_track):
                src = os.path.join(folder_to_track, filename)
                if os.path.isfile(src) and not self.is_system_file(src):
                    self.organize_file(src)

    def is_system_file(self, file_path):
        return os.path.basename(file_path).lower() == "desktop.ini"

    def organize_file(self, src):
        mime_type, _ = mimetypes.guess_type(src)
        if mime_type:
            for format_group, extensions in self.formats_to_organize.items():
                if any(ext in mime_type for ext in extensions):
                    self.move_file(src, format_group)
                    return
            self.move_file(src, "Others")
        else:
            self.move_file(src, "Others")

    def move_file(self, src, folder_name):
        downloads_folder = get_downloads_folder()
        dest_folder = os.path.join(downloads_folder, folder_name)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        basename = os.path.basename(src)
        dest = os.path.join(dest_folder, basename)

        if os.path.exists(dest):
            dest = self.get_unique_filename(dest_folder, basename)

        try:
            shutil.move(src, dest)
        except PermissionError as e:
            if e.errno == errno.EACCES:
                print(f"Permission denied for file {src}. Please close the file and try again.")
                return
            else:
                raise

    def get_unique_filename(self, dest_folder, basename):
        name, ext = os.path.splitext(basename)
        counter = 1
        new_name = f"{name} ({counter}){ext}"
        new_dest = os.path.join(dest_folder, new_name)
        while os.path.exists(new_dest):
            counter += 1
            new_name = f"{name} ({counter}){ext}"
            new_dest = os.path.join(dest_folder, new_name)
        return new_dest

def get_downloads_folder():
    home = str(Path.home())
    return os.path.join(home, 'Downloads')

def get_desktop_folder():
    home = str(Path.home())
    onedrive_path = os.path.join(home, 'OneDrive', 'Desktop')
    if os.path.exists(onedrive_path):
        return onedrive_path
    return os.path.join(home, 'Desktop')

def start_observer(folders_to_track, formats_to_organize):
    for folder in folders_to_track:
        if not os.path.exists(folder):
            print(f"Error: The folder '{folder}' does not exist.")
            return

    event_handler = FileOrganizerHandler(folders_to_track, formats_to_organize)
    observer = Observer()
    for folder in folders_to_track:
        observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    try:
        print("File organizer started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
        print("File organizer stopped.")

def is_browser_open():
    browser_processes = {
        "chrome.exe": "Google Chrome",
        "firefox.exe": "Mozilla Firefox",
        "msedge.exe": "Microsoft Edge",
        "safari.exe": "Safari",
        "Arc.exe": "Arc",
    }
    for process in psutil.process_iter(['name']):
        if process.info['name'] in browser_processes:
            return browser_processes[process.info['name']]
    return None

def monitor_browsers_and_start(folders_to_track, formats_to_organize):
    already_running = False
    while True:
        browser_name = is_browser_open()
        if browser_name:
            if not already_running:
                print(f"{browser_name} detected. Starting File Organizer.")
                start_observer(folders_to_track, formats_to_organize)
                already_running = True
        else:
            if already_running:
                print("No browser detected. Stopping file organizer.")
                already_running = False
        time.sleep(5)
