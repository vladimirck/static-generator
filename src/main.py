from textnode import TEXT_TYPE_STRING, TextType, TextNode
from mdparser import *
import os
import shutil

STATIC_DIR = "static"
PUBLIC_DIR = "public"


def _logpath( path, names):
    print(f"Folder being copying from {path}:")
    for file in names:
        print("\t" + os.path.join(path, file))
    return []



def main():
    if os.path.exists("test") == True:
        print(f"Removing the folder {PUBLIC_DIR}:")
        shutil.rmtree(PUBLIC_DIR)
        
    shutil.copytree(STATIC_DIR, PUBLIC_DIR, ignore=_logpath)

    generate_pages_recursive("content", "template.html", "public")


    print(get_all_files_path("content"))

main()