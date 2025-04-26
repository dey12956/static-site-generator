from htmlnode import HTMLNode, LeafNode, ParentNode
from blocktype import block_to_block_type, BlockType
from markdown_parser import markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node


def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_block_node = block_to_html_node(block, block_type)
        if block_type in [BlockType.HEADING, BlockType.QUOTE, BlockType.PARAGRAPH]:
            html_block_node.children = text_to_children(html_block_node.value)
        elif block_type == BlockType.CODE:
            text_node = TextNode(html_block_node.value, TextType.CODE)
            html_block_node.children = [text_node_to_html_node(text_node)]
        else:
            new_children = []
            for li in html_block_node.children:
                li.children = text_to_children(li.value)
                finalized_li = finalize_node(li)
                new_children.append(finalized_li)
            html_block_node.children = new_children
        nodes.append(finalize_node(html_block_node))
    return ParentNode("div", nodes)        


def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.HEADING:
            heading_level = block.count("#", 0, 6)
            text = block.lstrip("# ")
            return HTMLNode(f"h{heading_level}", text)
        case BlockType.CODE:
            lines = block.splitlines()
            text = "\n".join(lines[1:-1])
            text += "\n"
            return HTMLNode("pre", text)
        case BlockType.QUOTE:
            text = block.lstrip("> ")
            return HTMLNode("blockquote", text)
        case BlockType.UL:
            li = []
            lines = block.split("\n")
            for line in lines:
                line = line.lstrip("- ")
                li.append(HTMLNode("li", line))
            return HTMLNode("ul", None, li)
        case BlockType.OL:
            li = []
            lines = block.split("\n")
            for line in lines:
                line= line.lstrip("1234567890. ")
                li.append(HTMLNode("li", line))
            return HTMLNode("ol", None, li)
        case BlockType.PARAGRAPH:
            return HTMLNode("p", block.replace("\n", " "))


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_children = []
    for text_node in text_nodes:
        html_children.append(text_node_to_html_node(text_node))
    return html_children


def finalize_node(HTMLNode):
    if HTMLNode.children != None:
        return ParentNode(HTMLNode.tag, HTMLNode.children, HTMLNode.props)
    else:
        return LeafNode(HTMLNode.tag, HTMLNode.value, HTMLNode.props)