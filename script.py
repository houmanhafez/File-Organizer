import os
import shutil
import mimetypes
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class FileOrganizerHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track):
        self.folder_to_track = folder_to_track

    def on_modified(self, event):
        """
        Callback method triggered when a modification event is detected in the monitored folder.
        
        Args:
            event (FileSystemEvent): The event parameter passed by the watchdog library.
        """
        for filename in os.listdir(self.folder_to_track):
            src = os.path.join(self.folder_to_track, filename)
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
            elif "executables" in mime_type:
                self.move_file(src, "Executables")
            else:
                self.move_file(src, "Others")
        else:
            self.move_file(src, "Others")

    def move_file(self, src, folder_name):
        dest_folder = os.path.join(self.folder_to_track, folder_name)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(src, os.path.join(dest_folder, os.path.basename(src)))

def get_downloads_folder():
    home = str(Path.home())
    if os.name == 'nt':  
    # Windows
        downloads_folder = os.path.join(home, 'Downloads')
    # macOS/Linux
    else:  
        downloads_folder = os.path.join(home, 'Downloads')
    return downloads_folder

def start_observer(folder_to_track):
    event_handler = FileOrganizerHandler(folder_to_track)
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    folder_to_track = get_downloads_folder()
    print(f"Monitoring folder: {folder_to_track}")
    start_observer(folder_to_track)
