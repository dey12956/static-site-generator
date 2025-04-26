from cp_dirtree import cp_dirtree
from generate_page import generate_pages_recursive

def main():
    cp_dirtree("./static", "./public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()