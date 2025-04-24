import unittest

from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
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


class TestExtractMarkdownImage(unittest.TestCase):
    def test_extract_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "![dog](dog.jpg) and ![cat](cat.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("dog", "dog.jpg"), ("cat", "cat.png")])

    def test_image_with_spaces(self):
        text = "![cute dog](dog image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("cute dog", "dog image.jpg")])

    def test_no_images(self):
        text = "No images here!"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_malformed_image_does_not_match(self):
        text = "![no closing parenthesis](url"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])


class TestExtractMarkdownLink(unittest.TestCase):
    def test_extract_single_link(self):
        text = "Click [here](https://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("here", "https://example.com")])

    def test_extract_multiple_links(self):
        text = "[Google](https://google.com) and [GitHub](https://github.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("Google", "https://google.com"), ("GitHub", "https://github.com")])

    def test_link_with_spaces(self):
        text = "[my site](http://my site.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("my site", "http://my site.com")])

    def test_link_does_not_match_image(self):
        text = "This is an image: ![alt](img.png) and a [link](site.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "site.com")])

    def test_malformed_link_does_not_match(self):
        text = "[broken](missing"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])


class TestSplitNodesImages(unittest.TestCase):
    def test_single_image_node(self):
        input_nodes = [TextNode("This is an image ![cat](cat.png)", TextType.NORMAL)]
        result = split_nodes_image(input_nodes)
        expected = [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("cat", TextType.IMG, "cat.png")
        ]
        self.assertEqual(result, expected)

    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_with_no_match(self):
        input_nodes = [TextNode("No image here", TextType.NORMAL)]
        result = split_nodes_image(input_nodes)
        self.assertEqual(result, input_nodes)

    def test_mixed_image_and_text(self):
        input_nodes = [
            TextNode("Before image ", TextType.NORMAL),
            TextNode("![pic](pic.jpg) then more", TextType.NORMAL)
        ]
        result = split_nodes_image(input_nodes)
        expected = [
            TextNode("Before image ", TextType.NORMAL),
            TextNode("pic", TextType.IMG, "pic.jpg"),
            TextNode(" then more", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)


class TestSplitNodesLinks(unittest.TestCase):
    def test_single_link_node(self):
        input_nodes = [TextNode("Click [here](https://example.com)", TextType.NORMAL)]
        result = split_nodes_link(input_nodes)
        expected = [
            TextNode("Click ", TextType.NORMAL),
            TextNode("here", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        input_nodes = [TextNode("[a](1.com) and [b](2.com)", TextType.NORMAL)]
        result = split_nodes_link(input_nodes)
        expected = [
            TextNode("a", TextType.LINK, "1.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("b", TextType.LINK, "2.com")
        ]
        self.assertEqual(result, expected)

    def test_link_with_no_match(self):
        input_nodes = [TextNode("Just text", TextType.NORMAL)]
        result = split_nodes_link(input_nodes)
        self.assertEqual(result, input_nodes)

    def test_mixed_links(self):
        input_nodes = [
            TextNode("start ", TextType.NORMAL),
            TextNode("[click](url.com) end", TextType.NORMAL)
        ]
        result = split_nodes_link(input_nodes)
        expected = [
            TextNode("start ", TextType.NORMAL),
            TextNode("click", TextType.LINK, "url.com"),
            TextNode(" end", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text(self):
        result = text_to_textnodes("Just plain text.")
        expected = [TextNode("Just plain text.", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        result = text_to_textnodes("This is **bold**.")
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        result = text_to_textnodes("This is _italic_.")
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        result = text_to_textnodes("Here is `code`.")
        expected = [
            TextNode("Here is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_link_text(self):
        result = text_to_textnodes("Go to [Google](https://google.com).")
        expected = [
            TextNode("Go to ", TextType.NORMAL),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_image_text(self):
        result = text_to_textnodes("Look at ![dog](dog.png).")
        expected = [
            TextNode("Look at ", TextType.NORMAL),
            TextNode("dog", TextType.IMG, "dog.png"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_mixed_markdown(self):
        result = text_to_textnodes("**bold** and _italic_ and `code`")
        expected = [
            TextNode("", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_all_combined(self):
        text = "See ![img](img.jpg), then **bold**, _italic_, `code`, and [link](url.com)."
        result = text_to_textnodes(text)
        expected = [
            TextNode("See ", TextType.NORMAL),
            TextNode("img", TextType.IMG, "img.jpg"),
            TextNode(", then ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(", and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "url.com"),
            TextNode(".", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)


    def test_empty_string(self):
        result = text_to_textnodes("")
        expected = []
        self.assertEqual(result, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_blank_input(self):
        md = ""
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_only_whitespace_input(self):
        md = "     \n\n   \n"
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_newlines_only(self):
        md = "\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_block_with_inner_leading_spaces(self):
        md = " Line one\n  Line two\n   Line three"
        expected = ["Line one\nLine two\nLine three"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_single_paragraph(self):
        md = "This is a single paragraph with no line breaks."
        expected = ["This is a single paragraph with no line breaks."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_paragraph_with_newlines(self):
        md = "This is a paragraph\nthat continues on a new line\nwith some spacing."
        expected = ["This is a paragraph\nthat continues on a new line\nwith some spacing."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_multiple_paragraphs(self):
        md = "This is paragraph one.\n\nThis is paragraph two."
        expected = ["This is paragraph one.", "This is paragraph two."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_trailing_spaces_and_newlines(self):
        md = " This is indented. \n\n Second paragraph. \n\n   "
        expected = ["This is indented.", "Second paragraph."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_list_block(self):
        md = "- item 1\n - item 2\n- item 3"
        expected = ["- item 1\n- item 2\n- item 3"]
        self.assertEqual(markdown_to_blocks(md), expected)


if __name__ == "__main__":
    unittest.main()