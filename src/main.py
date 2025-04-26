from textnode import TextType, TextNode
from cp_dirtree import cp_dirtree


def main():
    cp_dirtree("./static", "./public")


if __name__ == "__main__":
    main()