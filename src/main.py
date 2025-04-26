from cp_dirtree import cp_dirtree
from generate_page import generate_pages_recursive
import sys

def main():
    basepath = sys.argv[0]
    if not sys.argv[0]:
        basepath = "/"
    cp_dirtree("./static", "./docs")
    generate_pages_recursive(basepath, "template.html", "docs")

if __name__ == "__main__":
    main()