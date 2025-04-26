from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(f"invalid markdown syntax: {delimiter} not closed")
        elif node.text_type == TextType.NORMAL:
            text_lst = node.text.split(delimiter)
            for i in range(len(text_lst)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(text_lst[i], TextType.NORMAL))
                else:
                    new_nodes.append(TextNode(text_lst[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        img_lst = extract_markdown_images(node.text)
        text = node.text
        for image_alt, image_link in img_lst:
            split_str = f"![{image_alt}]({image_link})"
            if split_str not in text:
                continue
            sections = text.split(split_str, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(image_alt, TextType.IMG, image_link))
            text = sections[1]
        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        link_lst = extract_markdown_links(node.text)
        text = node.text
        for link_text, url in link_lst:
            split_str = f"[{link_text}]({url})"
            if split_str not in text:
                continue
            sections = text.split(split_str, 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            text = sections[1]
        if text:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes


def text_to_textnodes(text):
    textnode_lst = [TextNode(text, TextType.NORMAL)]
    after_img_and_link = split_nodes_image(split_nodes_link(textnode_lst))
    after_bold = split_nodes_delimiter(after_img_and_link, "**", TextType.BOLD)
    after_italic = split_nodes_delimiter(after_bold, '_', TextType.ITALIC)
    after_code = split_nodes_delimiter(after_italic, '`', TextType.CODE)
    return after_code


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        lines = block.strip().splitlines()
        cleaned_lines = [line.strip() for line in lines]
        cleaned_block ="\n".join(cleaned_lines)
        if cleaned_block:
            blocks.append(cleaned_block)
    return blocks


def extract_title(markdown):
    lines = markdown.split("\n")
    if not any([line.startswith("# ") for line in lines]):
        raise Exception("No title")
    for line in lines:
        if line.startswith("# "):
            return line.strip("# ")