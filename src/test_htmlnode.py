import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_except(self):
        self.assertRaises(ValueError, HTMLNode)

    def test_props01(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"" )

    def test_props02(self):
        node = HTMLNode("a", "Google")
        self.assertEqual(node.props_to_html(), "" )

        
if __name__ == "__main__":
    unittest.main()
