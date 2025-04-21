from textnode import TextNode, TextType

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