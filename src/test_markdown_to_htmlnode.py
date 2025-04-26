import unittest
from markdown_to_htmlnode import markdown_to_blocks, markdown_to_html_node, block_to_html_node, text_to_children, finalize_node
from blocktype import block_to_block_type, BlockType

class TestTextNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        markdown = "# Heading One"
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertIn("Heading One", node.to_html())

    def test_blockquote(self):
        markdown = "> This is a quote"
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "blockquote")
        self.assertIn("This is a quote", node.to_html())

    def test_unordered_list(self):
        markdown = "- Item one\n- Item two\n- Item three"
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 1)
        ul = node.children[0]
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(len(ul.children), 3)
        self.assertTrue(all(li.tag == "li" for li in ul.children))
        self.assertIn("Item one", node.to_html())
        self.assertIn("Item two", node.to_html())
        self.assertIn("Item three", node.to_html())

    def test_ordered_list(self):
        markdown = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 1)
        ol = node.children[0]
        self.assertEqual(ol.tag, "ol")
        self.assertEqual(len(ol.children), 3)
        self.assertTrue(all(li.tag == "li" for li in ol.children))
        self.assertIn("First", node.to_html())
        self.assertIn("Second", node.to_html())
        self.assertIn("Third", node.to_html())

    def test_mixed_content(self):
        markdown = "# Heading\n\nParagraph text.\n\n- List item one\n- List item two"
        node = markdown_to_html_node(markdown)
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "ul")
        self.assertIn("Heading", node.to_html())
        self.assertIn("Paragraph text.", node.to_html())
        self.assertIn("List item one", node.to_html())
        self.assertIn("List item two", node.to_html())

    def test_inline_formatting(self):
        markdown = "This is **bold** and _italic_ and `code`."
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code</code>", html)

    def test_complex_document(self):
        markdown = "# Title\n\n> A quote\n\nParagraph with **bold** and _italic_.\n\n```\ncode block\n```"
        node = markdown_to_html_node(markdown)
        html = node.to_html()
        self.assertIn("<h1>", html)
        self.assertIn("<blockquote>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<code>code block\n</code>", html)