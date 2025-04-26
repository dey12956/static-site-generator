from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    elif all([line.startswith(">") for line in lines]):
        return BlockType.QUOTE

    elif all([line.startswith("- ") for line in lines]):
        return BlockType.UL

    elif all([line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)]):
        return BlockType.OL
    else:
        return BlockType.PARAGRAPH


