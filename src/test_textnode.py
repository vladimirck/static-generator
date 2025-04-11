import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        #print(f"testing if {node1} and {node2} are equal")
        self.assertEqual(node1, node2)

    def test_neq_01(self):
        node1 = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.BOLD)
        #print(f"testing if {node1} and {node2} are NOT equal")
        self.assertNotEqual(node1, node2)

    def test_neq_02(self):
        node1 = TextNode("This is a text node ", TextType.NORMAL)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        #print(f"testing if {node1} and {node2} are NOT equal")
        self.assertNotEqual(node1, node2)

    def test_url_none(self):
        node1=TextNode("Text",TextType.LINK, None)
        node2=TextNode("Text",TextType.LINK)
        self.assertEqual(node1,node2)

if __name__ == "__main__":
    unittest.main()