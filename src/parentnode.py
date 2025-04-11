from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children: list[HTMLNode], props = None):
        if tag == None:
            raise ValueError("A tag must be provided")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == "":
            raise ValueError("Tag cannot be empty")
        if len(self.children) == 0:
            raise ValueError("A ParentNode must have at least a children node")
        text = ""
        for child in self.children:
            text += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{text}</{self.tag}>"
    
