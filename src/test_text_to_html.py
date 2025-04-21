import unittest

from text_to_html import text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType

class TestTextToHTML(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Google", TextType.LINK, url="https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_img(self):
        node = TextNode("Cat", TextType.IMG, url="cat.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "cat.jpg", "alt": "Cat"})

    def test_invalid_text_type_raises(self):
        class FakeTextType:
            pass
        tn = TextNode("Bad", FakeTextType)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(tn)
        self.assertIn("invalid TextType", str(context.exception))

if __name__ == "__main__":
    unittest.main()