import unittest

from markdown_parser import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        input_nodes = [TextNode("This is **bold** text", TextType.NORMAL)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        input_nodes = [TextNode("**A** and **B**", TextType.NORMAL)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("", TextType.NORMAL),
            TextNode("A", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("B", TextType.BOLD),
            TextNode("", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_mixed_nodes(self):
        input_nodes = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and **strong**", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("strong", TextType.BOLD),
            TextNode("", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises(self):
        input_nodes = [TextNode("This is **broken", TextType.NORMAL)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertIn("invalid markdown syntax", str(context.exception))

    def test_non_normal_node_unchanged(self):
        input_nodes = [TextNode("This is code", TextType.CODE)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertEqual(result, input_nodes)

    def test_empty_string(self):
        input_nodes = [TextNode("", TextType.NORMAL)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("", TextType.NORMAL)])

    def test_delimiter_only_string(self):
        input_nodes = [TextNode("****", TextType.NORMAL)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [TextNode("", TextType.NORMAL), TextNode("", TextType.BOLD), TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_delimiter_with_spaces(self):
        input_nodes = [TextNode(" ** spaced ** ", TextType.NORMAL)]
        result = split_nodes_delimiter(input_nodes, "**", TextType.BOLD)
        expected = [
            TextNode(" ", TextType.NORMAL),
            TextNode(" spaced ", TextType.BOLD),
            TextNode(" ", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)