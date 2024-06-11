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
    """
    FileOrganizerHandler is a class responsible for handling file system events and organizing files accordingly.

    Attributes:
        folders_to_track (list): A list of folders to monitor for file system events.
    """
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
                if os.path.isfile(src) and not self.is_system_file(src):
                    self.organize_file(src)

    def is_system_file(self, file_path):
        """
        Checks if the given file path is a system file.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file is a system file, False otherwise.
        """
        return os.path.basename(file_path).lower() == "desktop.ini"

    def organize_file(self, src):
        """
        Organizes the given file based on its MIME type.

        Args:
            src (str): The path of the file to organize.
        """
        mime_type, _ = mimetypes.guess_type(src)
        if mime_type:
            if "pdf" in mime_type:
                self.move_file(src, "PDFs")
            elif "image" in mime_type:
                self.move_file(src, "Images")
            elif "html" in mime_type in mime_type:
                self.move_file(src, "Web Files")
            elif "text" in mime_type or "csv" in mime_type or "sql" in mime_type:
                self.move_file(src, "Text Files")
            elif "spreadsheet" in mime_type:
                self.move_file(src, "Spreadsheets")
            elif "presentation" in mime_type:
                self.move_file(src, "Presentations")
            elif "audio" in mime_type:
                self.move_file(src, "Audio")
            elif "video" in mime_type:
                self.move_file(src, "Videos")
            elif "font" in mime_type:
                self.move_file(src, "Fonts")
            elif "compressed" in mime_type or "zip" in mime_type or "rar" in mime_type or "7z" in mime_type:
                self.move_file(src, "Archives")
            elif "executable" in mime_type or "msi" in mime_type or src.endswith(".exe"):
                self.move_file(src, "Executables")
            elif "script" in mime_type or "javascript" in mime_type:
                self.move_file(src, "Scripts")
            elif "word" in mime_type :
                self.move_file(src, "Word Documents")
            else:
                self.move_file(src, "Others")
        else:
            self.move_file(src, "Others")

    def move_file(self, src, folder_name):
        """
        Moves the file to the specified folder.

        Args:
            src (str): The path of the file to move.
            folder_name (str): The name of the destination folder.
        """
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
        """
        Generates a unique filename to avoid overwriting existing files.

        Args:
            dest_folder (str): The path of the destination folder.
            basename (str): The base name of the file.

        Returns:
            str: A unique filename.
        """
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
    """
    Retrieves the path of the user's Downloads folder.

    Returns:
        str: The path of the Downloads folder.
    """
    home = str(Path.home())
    return os.path.join(home, 'Downloads')

def get_desktop_folder():
    """
    Retrieves the path of the user's Desktop folder.

    Returns:
        str: The path of the Desktop folder.
    """
    home = str(Path.home())
    onedrive_path = os.path.join(home, 'OneDrive', 'Desktop')
    if os.path.exists(onedrive_path):
        return onedrive_path
    return os.path.join(home, 'Desktop')

def start_observer(folders_to_track):
    """
    Starts monitoring the specified folders for file system events.

    Args:
        folders_to_track (list): A list of folders to monitor.
    """
    for folder in folders_to_track:
        if not os.path.exists(folder):
            print(f"Error: The folder '{folder}' does not exist.")
            return

    event_handler = FileOrganizerHandler(folders_to_track)
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
    """
    Checks if any browser process is currently running. If you are using any other browsers, add the process name into the dictionary

    Returns:
        str or None: The name of the detected browser process, or None if no browser is found.
    """
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

def monitor_browsers_and_start():
    """
    Monitors browser processes and starts the file organizer when a browser is detected.
    """
    already_running = False
    while True:
        browser_name = is_browser_open()
        if browser_name:
            if not already_running:
                print(f"{browser_name} detected. Starting File Organizer.")
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
