
class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        if value == None and children == None:
            raise ValueError("A leat, each HTMLNode need to either, a value or a children, or both")
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None:
            return ""
        prop_list = []
        for key, val in self.props.items():
            prop_list.append(f"{key}=\"{val}\"")
        return " " + " ".join(prop_list)
    
    def __repr__(self):
        return f"HTMLNode( tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props})"

