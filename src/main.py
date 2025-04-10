from textnode import TEXT_TYPE_STRING, TextType, TextNode

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(text_node)

main()