from textnode import TextNode, TextType, TEXT_TYPE_STRING
from leafnode import LeafNode, text_node_to_html_node
from parentnode import ParentNode
from htmlnode import HTMLNode
import re
from enum import Enum
import os
from pathlib import Path


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING_1 = 1
    HEADING_2 = 2
    HEADING_3 = 3
    HEADING_4 = 4
    HEADING_5 = 5
    HEADING_6 = 6
    CODE = 7
    QUOTE = 8
    UNORDERED_LIST = 9
    ORDERED_LIST = 10

def split_nodes(old_nodes: list[TextNode], delim: str, text_type: TextType)-> list[TextNode]:
    delta = len(delim)
    if delta == 0:
        raise ValueError("The delimiter must by non empty string")
    new_nodes = []
    for node in old_nodes:
        #print(node)
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        delim_count = node.text.count(delim)
        if delim_count <= 1:
            new_nodes.append(node)
            continue
        text = node.text
        for index in range(int(delim_count/2.0)):
            delim_begin = text.index(delim)
            #print(f"delim_begin: {delim_begin}")
            delim_end = text[delim_begin + delta:].index(delim) + delim_begin + delta
            #print(f"delim_end {delim_end}")
            if delim_begin != 0:
                new_nodes.append(TextNode(text[0:delim_begin], TextType.NORMAL))
            if delim_begin != (delim_end - delta):
                new_nodes.append(TextNode(text[delim_begin+delta: delim_end], text_type))
            text = text[delim_end + delta:]
        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.NORMAL))
    #print(new_nodes)
    return new_nodes

def extract_markdown_images(text: str):
    ans = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return ans

def extract_markdown_links(text: str):
    ans = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return ans

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if len(old_nodes) == 0:
        return new_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        images_list = extract_markdown_images(node.text)

        if len(images_list) == 0:
            new_nodes.append(node)
            continue

        node_text = node.text
        for text, url in images_list:
            text_index = node_text.find("![" + text + "]")
            if text_index != 0:
                new_nodes.append(TextNode(node_text[0:text_index],TextType.NORMAL))
            new_nodes.append(TextNode(text,TextType.IMAGE,url))
            url_end_index = node_text.find("(" + url +")") + len(url) + 2
            node_text = node_text[url_end_index:]
        
        if len(node_text)!=0:
            new_nodes.append(TextNode(node_text,TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    if len(old_nodes) == 0:
        return new_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        links_list = extract_markdown_links(node.text)

        if len(links_list) == 0:
            new_nodes.append(node)
            continue

        node_text = node.text
        for text, url in links_list:
            text_index = node_text.find("[" + text + "]")
            if text_index != 0:
                new_nodes.append(TextNode(node_text[0:text_index],TextType.NORMAL))
            new_nodes.append(TextNode(text,TextType.LINK,url))
            url_end_index = node_text.find("(" + url +")") + len(url) + 2
            node_text = node_text[url_end_index:]
        
        if len(node_text)!=0:
            new_nodes.append(TextNode(node_text,TextType.NORMAL))
    return new_nodes

def text_to_textnodes(MDtext: str) -> list[TextNode]:
    if len(MDtext) == 0:
        return []
    nodes_list = [TextNode(MDtext, TextType.NORMAL)]
    nodes_list = split_nodes(nodes_list, "**", TextType.BOLD)
    nodes_list = split_nodes(nodes_list, "_", TextType.ITALIC)
    nodes_list = split_nodes(nodes_list, "`", TextType.CODE)
    nodes_list = split_nodes_image(nodes_list)
    nodes_list = split_nodes_link(nodes_list)
    return nodes_list


def markdown_to_blocks(markdown: str) -> list[str]:
    print(f"MDText:\n\n{markdown}")
    blocks_list = markdown.split("\n\n")
    clean_block_list = []
    for block in blocks_list:
        x = block.strip()
        if len(x) !=0:
            clean_block_list.append(x)
    
    print("Bloques:\n")
    print(clean_block_list)
    return clean_block_list

def block_to_block_type(MDBlock: str) -> BlockType:
    match MDBlock[0]:
        case "#":
            if MDBlock.find("###### ") == 0:
                return BlockType.HEADING_6
            elif MDBlock.find("##### ") == 0:
                return BlockType.HEADING_5
            elif MDBlock.find("#### ") == 0:
                return BlockType.HEADING_4
            elif MDBlock.find("### ") == 0:
                return BlockType.HEADING_3
            elif MDBlock.find("## ") == 0:
                return BlockType.HEADING_2
            elif MDBlock.find("# ") == 0:
                return BlockType.HEADING_1
            else:
                return BlockType.PARAGRAPH
        case "`":
            n = len(MDBlock)
            if MDBlock[0:3]=="```" and MDBlock[n-3:n]=="```" and len(MDBlock)>6:
                return BlockType.CODE
            return BlockType.PARAGRAPH
        case ">":
            lines = MDBlock.split("\n")
            for line in lines:
                if line[0:2] != "> ":
                    if line[0] == ">" and len(line) == 1:
                        continue
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        case "-":
            lines = MDBlock.split("\n")
            for line in lines:
                if line[0:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case "*":
            lines = MDBlock.split("\n")
            for line in lines:
                if line[0:2] != "* ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case "1":
            lines = MDBlock.split("\n")
            counter = 1
            for line in lines:
                if line[0:3] != f"{counter}. ":
                    return BlockType.PARAGRAPH
                counter += 1
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

def make_parent_node(block: str, tag: str) -> ParentNode:
    nodes_list = text_to_textnodes(block)
    children = []
    for node in nodes_list:
        children.append(text_node_to_html_node(node))                
    return ParentNode(tag, children)

def make_parent_node_block_list(block: str, tag:str)->ParentNode:
    lines = block.split("\n")
    html_nodes_list = []
    for line in lines:
        space_index = line.find(" ")
        html_nodes_list.append(make_parent_node(line[space_index:].strip(), "li"))
    return ParentNode(tag, html_nodes_list)

def markdown_to_html_node(md_doc: str) -> HTMLNode:
    md_blocks = markdown_to_blocks(md_doc)
    html_node_list = []
    for block in md_blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:    
                html_node_list.append(make_parent_node(block, "p"))
            case BlockType.HEADING_1:                               
                html_node_list.append(make_parent_node(block[2:].strip(), "h1"))
            case BlockType.HEADING_2:
                html_node_list.append(make_parent_node(block[3:].strip(), "h2"))
            case BlockType.HEADING_3:
                html_node_list.append(make_parent_node(block[4:].strip(), "h3"))
            case BlockType.HEADING_4:
                html_node_list.append(make_parent_node(block[5:].strip(), "h4"))
            case BlockType.HEADING_5:
                html_node_list.append(make_parent_node(block[6:].strip(), "h5"))
            case BlockType.HEADING_6:
                html_node_list.append(make_parent_node(block[7:].strip(), "h6"))
            case BlockType.CODE:
                html_node_list.append(ParentNode("pre",[LeafNode("code", block[3:-3].strip() + "\n")]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_block = []
                for line in lines:
                    new_block.append(line[2:])                
                html_node_list.append(make_parent_node("\n".join(new_block), "blockquote"))
            case BlockType.UNORDERED_LIST:
                html_node_list.append(make_parent_node_block_list(block, "ul"))
            case BlockType.ORDERED_LIST:
                html_node_list.append(make_parent_node_block_list(block, "ol"))
    node = ParentNode("div", html_node_list)
    print(f"HTML Text: {node.to_html()}")
    return node 

def extract_title(md_doc: str) -> str:
    lines = md_doc.split("\n")
    for line in lines:
        striped_line = line.strip()
        if striped_line[0:2] == "# ":
            return striped_line[2:].strip()    
    raise ValueError("No level 1 heading found")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        md_doc = file.read()
    
    with open(template_path) as file:
        template_doc = file.read()

    content = markdown_to_html_node(md_doc).to_html()

    title = extract_title(md_doc)

    html_doc = template_doc.replace("{{ Title }}", title)
    html_doc = html_doc.replace("{{ Content }}", content)

    output_file = Path(dest_path)
    output_file.parent.mkdir(exist_ok=True, parents=True)

    with open(output_file, "w") as file:
        file.write(html_doc)

def get_all_files_path(dir_path)-> list[str]:
    files_list = []

    files_current_dir = os.listdir(dir_path)
    for file_name in files_current_dir:
        if os.path.isdir(dir_path + "/" + file_name) == True:
            files_list += get_all_files_path(dir_path + "/" + file_name)
        else:
            files_list.append(dir_path + "/" + file_name)

    return files_list
    

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if os.path.isdir(dir_path_content) == False:
        raise Exception("The path to the contect directory is not a directory")
    content_files_list = get_all_files_path(dir_path_content)
    content_dir_length = len(dir_path_content)
    for content_file  in content_files_list:
        tot_length = len(content_file)
        dest_file = dest_dir_path + content_file[content_dir_length:tot_length-2] + "html"
        generate_page(content_file, template_path, dest_file)
