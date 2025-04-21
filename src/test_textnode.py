import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.CODE) 
        node2 = TextNode("This is a text node", TextType.IMG)
        self.assertNotEqual(node, node2)

    def test_init(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.bootdev.com")
        self.assertEqual("This is a text node", node.text)
        self.assertEqual(TextType.BOLD, node.text_type)
        self.assertEqual("www.bootdev.com", node.url)

    def test_repr(self):
        node = TextNode("code", TextType.CODE) 
        self.assertEqual("TextNode(code, code, None)", repr(node))

    def test_textnode_repr_with_url(self):
        node = TextNode("link", TextType.LINK, "http://example.com")
        self.assertEqual(repr(node), "TextNode(link, link, http://example.com)")

if __name__ == "__main__":
    unittest.main()