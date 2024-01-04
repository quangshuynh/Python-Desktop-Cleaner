"""
Downloads Folder Cleaner
author: Quang Huynh
01/04/24
"""

from os import rename, scandir
from os.path import exists, join, splitext
from shutil import move
from time import sleep

import logging

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Folders
source_dir = "/Users/user/Downloads"
dest_dir_img = "/Users/user/Pictures/Downloaded Photos"
dest_dir_vid = "Users/user/Videos/Downloaded Videos"
dest_dir_sfx = "Users/user/Music/Downloaded Sounds"
dest_dir_music = "Users/user/Music/Downloaded Sounds/Downloaded Music"
dest_dir_doc = "Users/user/Documents/Downloaded Documents"

# Supported extension types

# Images
img_ext = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw",
           ".arw", ".cr2", ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k",
           ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]

# Videos
vid_ext = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov",
           ".qt", ".flv", ".swf", ".avchd"]

# Audio
audio_ext = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]

# Documents
doc_ext = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]


def make_unique(dest, name):
    """
    Checks if a file exists and renames file until it is unique
    :param dest: Destination folder
    :param name: Name of file
    :return: A unique name for file
    """
    filename, extension = splitext(name)
    counter = 1
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1
    return name


def move_file(dest, entry, name):
    """
    Moves a file from a source directory to destination
    :param dest: Destination directory
    :param entry: Source directory
    :param name: File name
    """
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        """
        Called when a file or directory is modified
        :param event: FileSystemEvent object representing the modification event
        """
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_audio_files(entry, name)
                self.check_video_files(entry, name)
                self.check_image_files(entry, name)
                self.check_document_files(entry, name)

    def check_audio_files(self, entry, name):
        """
        Check if given file is an audio file and move it based on size and content
        :param entry: DirEntry object representing the file
        :param name: Name of the file
        """
        for audio_extension in audio_ext:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                if entry.stat().st_size < 10000000 or "SFX" in name:  # < 10 MB
                    dest = dest_dir_sfx  # Moves if file is less than 10 MB
                else:
                    dest = dest_dir_music # Moves if file is more than 10 MB
                move_file(dest, entry, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, entry, name):
        """
        Check if given file is a video file and move it based on extension name
        :param entry: DirEntry object representing the file
        :param name: Name of the file
        """
        for video_extension in vid_ext:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file(dest_dir_vid, entry, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, entry, name):
        """
        Check if given file is an image file and move it based on extension name
        :param entry: DirEntry object representing the file
        :param name: Name of the file
        """
        for image_extension in img_ext:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file(dest_dir_img, entry, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, entry, name):
        """
        Check if given file is a document file and move it based on extension name
        :param entry: DirEntry object representing the file
        :param name: Name of the file
        """
        for documents_extension in doc_ext:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file(dest_dir_doc, entry, name)
                logging.info(f"Moved document file: {name}")


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
