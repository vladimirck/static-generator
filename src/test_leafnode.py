import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_exception(self):
        self.assertRaises(ValueError, LeafNode, None, None, None)

    def test_to_html01(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html02(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
