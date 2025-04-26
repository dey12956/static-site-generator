from cp_dirtree import cp_dirtree
from generate_page import generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    cp_dirtree("./static", "./docs")
    generate_pages_recursive(basepath, "template.html", "docs")

if __name__ == "__main__":
    main()