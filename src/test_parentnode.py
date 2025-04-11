import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren1(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren2(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node1 = ParentNode("span", [grandchild_node])
        child_node2 = LeafNode("a","Nice Text", {"href":"google.com"})
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><a href=\"google.com\">Nice Text</a></div>",
        )

    def test_constructor_exception01(self):
        self.assertRaises(ValueError, ParentNode, "div", None)

    def test_constructor_exception02(self):
        child1 = LeafNode("a", "Nice Text", {"href":"google.com"})
        self.assertRaises(ValueError, ParentNode, None, [child1])

    def test_constructor_exception03(self):
        child1 = LeafNode("a", "Nice Text", {"href":"google.com"})
        self.assertRaises(ValueError, ParentNode, None, [child1])

    def test_to_html_exception(self):
        child1 = LeafNode("a", "Nice Text", {"href":"google.com"})
        node = ParentNode("", [child1])
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()
