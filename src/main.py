from textnode import TextType, TextNode

def main():
    dummy = TextNode("This is an image", TextType.IMG, "![alt text for image](url/of/image.jpg)")

    print(dummy)

if __name__ == "__main__":
    main()