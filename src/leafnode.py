from htmlnode import HTMLNode
from textnode import TextNode, TextType

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag == None:
            return self.value
        if self.value == "" or self.value == None:
            return f"<{self.tag}{self.props_to_html()}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

def text_node_to_html_node(text_node: TextNode)-> LeafNode:
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text,None)
        case TextType.BOLD:
            return LeafNode("b",text_node.text,None)
        case TextType.ITALIC:
            return LeafNode("i",text_node.text,None)
        case TextType.CODE:
            return LeafNode("code",text_node.text,None)
        case TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url, "alt":text_node.text})
