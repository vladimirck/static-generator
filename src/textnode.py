from enum import Enum

class TextType(Enum):
    NORMAL = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5

TEXT_TYPE_STRING = {
    TextType.NORMAL: "normal texto",
    TextType.BOLD: "bold text",
    TextType.ITALIC: "italic text",
    TextType.CODE: "code text",
    TextType.LINK: "URL address",
    TextType.IMAGE: "image URL"
}

class TextNode:
    def __init__(self, text, text_type, url):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {TEXT_TYPE_STRING[self.text_type]}, {self.url})"
    


    
