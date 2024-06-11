import os
import shutil
import mimetypes
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import psutil


class FileOrganizerHandler(FileSystemEventHandler):
    def __init__(self, folders_to_track):
        self.folders_to_track = folders_to_track

    def on_modified(self, event):
        """
        Callback method triggered when a modification event is detected in the monitored folders.

        Args:
            event (FileSystemEvent): The event parameter passed by the watchdog library.
        """
        for folder_to_track in self.folders_to_track:
            for filename in os.listdir(folder_to_track):
                src = os.path.join(folder_to_track, filename)
                if os.path.isfile(src):
                    self.organize_file(src)

    def organize_file(self, src):
        mime_type, _ = mimetypes.guess_type(src)
        if mime_type:
            if "pdf" in mime_type:
                self.move_file(src, "PDFs")
            elif "image" in mime_type:
                self.move_file(src, "Images")
            elif "html" in mime_type:
                self.move_file(src, "HTMLs")
            elif "executable" in mime_type:
                self.move_file(src, "Executables")
            else:
                self.move_file(src, "Others")
        else:
            self.move_file(src, "Others")

    def move_file(self, src, folder_name):
        downloads_folder = get_downloads_folder()
        dest_folder = os.path.join(downloads_folder, folder_name)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(src, os.path.join(dest_folder, os.path.basename(src)))


def get_downloads_folder():
    home = str(Path.home())
    return os.path.join(home, "Downloads")


def get_desktop_folder():
    home = str(Path.home())
    onedrive_path = os.path.join(home, "OneDrive", "Desktop")
    if os.path.exists(onedrive_path):
        return onedrive_path
    return os.path.join(home, "Desktop")


def start_observer(folders_to_track):
    for folder in folders_to_track:
        if not os.path.exists(folder):
            raise FileNotFoundError(f"The folder {folder} does not exist.")

    event_handler = FileOrganizerHandler(folders_to_track)
    observer = Observer()
    for folder in folders_to_track:
        observer.schedule(event_handler, folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def is_browser_open():
    browser_processes = [
        "chrome.exe",
        "firefox.exe",
        "msedge.exe",
        "safari.exe",
        "Arc.exe",
    ]  # Add other browser executables as needed
    for process in psutil.process_iter(["name"]):
        if process.info["name"] in browser_processes:
            return True
    return False


def monitor_browsers_and_start():
    already_running = False
    while True:
        if is_browser_open():
            if not already_running:
                print("Browser detected. Starting file organizer.")
                folders_to_track = [get_downloads_folder(), get_desktop_folder()]
                print(f"Monitoring folders: {folders_to_track}")
                start_observer(folders_to_track)
                already_running = True
        else:
            if already_running:
                print("No browser detected. Stopping file organizer.")
                # Handle stopping the observer if needed
                already_running = False
        time.sleep(5)


if __name__ == "__main__":
    monitor_browsers_and_start()
