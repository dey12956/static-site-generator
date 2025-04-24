import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):

    def test_heading_levels(self):
        for i in range(1, 7):
            with self.subTest(i=i):
                self.assertEqual(
                    block_to_block_type("#" * i + " Heading"),
                    BlockType.HEADING
                )

    def test_code_block(self):
        block = "```\ndef foo():\n    return bar\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Another quote line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UL)

    def test_ordered_list_block(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.OL)

    def test_paragraph_block(self):
        block = "This is a paragraph\nwith multiple lines\nbut not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_list_should_be_paragraph(self):
        block = "1. First\n- Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_partial_ordered_list_should_be_paragraph(self):
        block = "1. First\n2. Second\nThird"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_partial_ul_should_be_paragraph(self):
        block = "- First\nSecond"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_single_line_quote_without_marker(self):
        block = "This is > not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_missing_closing(self):
        block = "```\ndef foo():\n    pass"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()