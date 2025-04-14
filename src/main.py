from textnode import TEXT_TYPE_STRING, TextType, TextNode
from mdparser import *
import os
import shutil
import sys

STATIC_DIR = "static"
PUBLIC_DIR = "docs"
CONTENT_DIR = "content"


def _logpath( path, names):
    print(f"Folder being copying from {path}:")
    for file in names:
        print("\t" + os.path.join(path, file))
    return []



def main():

    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    if os.path.exists(PUBLIC_DIR) == True:
        print(f"Removing the folder {PUBLIC_DIR}:")
        shutil.rmtree(PUBLIC_DIR)
        
    shutil.copytree(STATIC_DIR, PUBLIC_DIR, ignore=_logpath)

    generate_pages_recursive(CONTENT_DIR, "template.html", PUBLIC_DIR, basepath)

    print (sys.argv)

main()