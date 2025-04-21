import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode(tag="p", value="Hello", children=["child1"], props={"class": "text"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, ["child1"])
        self.assertEqual(node.props, {"class": "text"})

    
    def test_props_to_html(self):
        node = HTMLNode(props = {
            "href": "https://www.google.com",
            "target": "_blank",
            })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode()
        node.props = None
        with self.assertRaises(TypeError):
            node.props_to_html()

    def test_to_html_raises(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("div", "content", [], {"style": "color:red;"})
        expected = "TextNode(tag: div, value: content, children: [], props:{'style': 'color:red;'})"
        self.assertEqual(repr(node), expected)


class TestLeafNode(unittest.TestCase):
    def test_init_sets_attributes(self):
        node = LeafNode("p", "hello", {"class": "bold"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "bold"})
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "plain text")
        self.assertEqual(node.to_html(), "plain text")

    def test_leaf_to_html_value_none(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_with_props(self):
        node = LeafNode("span", "styled", {"class": "highlight", "id": "x1"})
        html = node.to_html()
        self.assertIn("<span", html)
        self.assertIn('class="highlight"', html)
        self.assertIn('id="x1"', html)
        self.assertIn(">styled</span>", html)


class TestParentNode(unittest.TestCase):
    def test_init(self):
        children = [LeafNode(None, "Hello")]
        node = ParentNode("div", children, {"id": "main"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {"id": "main"})
        self.assertIsNone(node.value)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        node = ParentNode("span", [LeafNode(None, "Text")], {"class": "highlight"})
        result = node.to_html()
        self.assertIn('<span class="highlight">', result)
        self.assertIn("Text", result)
        self.assertIn("</span>", result)

    def test_to_html_multiple_children(self):
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, " and "),
            LeafNode("i", "Italic")
        ]
        node = ParentNode("p", children)
        self.assertEqual(node.to_html(), "<p><b>Bold</b> and <i>Italic</i></p>")

    def test_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode(None, "hi")]).to_html()

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()



if __name__ == "__main__":
    unittest.main()