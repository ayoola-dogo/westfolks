from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from contextmanager_change_dir import change_dir  
import os
import time
import shutil


class MyHandler(FileSystemEventHandler):

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def on_modified(self, event):
        with change_dir(self.source):
            for file in os.listdir():
                src = file
                shutil.copy(src, os.path.join(self.destination, src))
        print(os.getcwd())


def automate_copy(source, destination):
    event_handler = MyHandler(source, destination)
    observer = Observer()
    observer.schedule(event_handler, source, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
