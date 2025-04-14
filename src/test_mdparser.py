import unittest
from mdparser import *

class TestMDParser(unittest.TestCase):

    def test_split_nodes01(self):
        output = split_nodes([TextNode("I like to use **bold** fonts for emphasis", TextType.NORMAL)], "**" , TextType.BOLD)
        expected =[TextNode("I like to use ", TextType.NORMAL),
                   TextNode("bold", TextType.BOLD),
                   TextNode(" fonts for emphasis", TextType.NORMAL)]
        self.assertEqual(output, expected)
    
    def test_split_nodes02(self):
        output = split_nodes([TextNode("I like to use _italic fonts_ for emphasis", TextType.NORMAL)], "_" , TextType.ITALIC)
        expected =[TextNode("I like to use ", TextType.NORMAL),
                   TextNode("italic fonts", TextType.ITALIC),
                   TextNode(" for emphasis", TextType.NORMAL)]
        self.assertEqual(output, expected)

    def test_split_nodes03(self):
        output = split_nodes([TextNode("I like to use _italic fonts_ for _emphasis", TextType.NORMAL)], "_" , TextType.ITALIC)
        expected =[TextNode("I like to use ", TextType.NORMAL),
                   TextNode("italic fonts", TextType.ITALIC),
                   TextNode(" for _emphasis", TextType.NORMAL)]
        self.assertEqual(output, expected)

    def test_split_nodes04(self):
        output = split_nodes([TextNode("I like to use _italic fonts_ for _emphasis.", TextType.NORMAL),
                              TextNode("This is a bold move", TextType.BOLD),
                              TextNode("**This is another bold move**, incomplete **bold fonts.", TextType.NORMAL)], "_" , TextType.ITALIC)
        expected =[TextNode("I like to use ", TextType.NORMAL),
                   TextNode("italic fonts", TextType.ITALIC),
                   TextNode(" for _emphasis.", TextType.NORMAL),
                   TextNode("This is a bold move", TextType.BOLD),
                   TextNode("**This is another bold move**, incomplete **bold fonts.", TextType.NORMAL)]
        self.assertEqual(output, expected)

    def test_split_nodes05(self):
        output = split_nodes([TextNode("I like to use _italic fonts_ for _emphasis.", TextType.NORMAL),
                              TextNode("This is a bold move", TextType.BOLD),
                              TextNode("**This is another bold move**, incomplete **bold fonts.", TextType.NORMAL)], "**" , TextType.BOLD)
        
        expected =[TextNode("I like to use _italic fonts_ for _emphasis.", TextType.NORMAL),
                   TextNode("This is a bold move", TextType.BOLD),
                   TextNode("This is another bold move", TextType.BOLD),
                   TextNode(", incomplete **bold fonts.", TextType.NORMAL)]
        self.assertEqual(output, expected)

    def test_split_nodes06(self):
        output = split_nodes([TextNode("I like to use _italic fonts_ for _emphasis.", TextType.NORMAL),
                              TextNode("This is a bold move", TextType.BOLD),
                              TextNode("**This is another bold move**, incomplete **bold fonts.**", TextType.NORMAL)], "**" , TextType.BOLD)
        
        expected =[TextNode("I like to use _italic fonts_ for _emphasis.", TextType.NORMAL),
                   TextNode("This is a bold move", TextType.BOLD),
                   TextNode("This is another bold move", TextType.BOLD),
                   TextNode(", incomplete ", TextType.NORMAL),
                   TextNode("bold fonts.", TextType.BOLD)]
        self.assertEqual(output, expected)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_single_image(self):
        # Test case provided by the user
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_multiple_images(self):
        # Test with several images mixed with text
        text = "Here's ![img1](url1.jpg). And another ![image 2](url2.png)! Finally, ![img3](path/to/img3.gif)."
        expected = [
            ("img1", "url1.jpg"),
            ("image 2", "url2.png"),
            ("img3", "path/to/img3.gif"),
        ]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_no_images(self):
        # Test text without any markdown images
        text = "This is plain text. No images here. Maybe a [link](url), but not an image."
        expected = []
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_empty_string(self):
        # Test with an empty input string
        text = ""
        expected = []
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_image_at_start_and_end(self):
        # Test images appearing at the very beginning and end
        text = "![start](start.png) Some text in the middle ![end](end.gif)"
        expected = [("start", "start.png"), ("end", "end.gif")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_empty_alt_text(self):
        # Test image link with empty alt text
        text = "An image without alt text: ![](empty_alt.svg)"
        expected = [("", "empty_alt.svg")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_empty_url(self):
        # Test image link with empty URL (less common, but valid syntax)
        text = "An image with an empty URL: ![empty url]()"
        expected = [("empty url", "")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_mixed_content_with_regular_links(self):
        # Test ensuring regular links are not extracted
        text = "Here is ![an image](image.jpg) and here is [a link](link.html). Another ![image2](img2.png)."
        expected = [("an image", "image.jpg"), ("image2", "img2.png")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_url_with_special_chars(self):
        # Test a URL containing common special characters
        text = "Image with complex URL: ![complex](http://example.com/img-file_name.jpg?size=large#fragment)"
        expected = [("complex", "http://example.com/img-file_name.jpg?size=large#fragment")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_alt_text_with_special_chars(self):
         # Test alt text containing spaces and punctuation
         text = "Image with complex alt text: ![My Great Image! (v2)](complex_alt.png)"
         expected = [("My Great Image! (v2)", "complex_alt.png")]
         self.assertListEqual(expected, extract_markdown_images(text))
    
    def test_single_link(self):
        """Tests a single standard link."""
        text = "Visit [Google](https://www.google.com) for search."
        expected = [("Google", "https://www.google.com")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_multiple_links(self):
        """Tests multiple links in the text."""
        text = "Check out [Example](http://example.com) and [Another Page](page2.html)."
        expected = [("Example", "http://example.com"), ("Another Page", "page2.html")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_no_links(self):
        """Tests text with no Markdown links."""
        text = "This text has no links, maybe some **bold** text."
        expected = []
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_empty_string(self):
        """Tests an empty input string."""
        text = ""
        expected = []
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_link_at_start_and_end(self):
        """Tests links at the very beginning and end of the text."""
        text = "[Start Link](start.url) some text [End Link](end.url)"
        expected = [("Start Link", "start.url"), ("End Link", "end.url")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_empty_link_text(self):
        """Tests a link with empty link text: [](url)."""
        text = "An empty link text: [](link.html)"
        expected = [("", "link.html")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_empty_url(self):
        """Tests a link with an empty URL: [text]()."""
        text = "A link with no URL: [No Where]()"
        expected = [("No Where", "")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_mixed_content_with_images(self):
        """IMPORTANT: Tests that image links ![alt](url) are ignored."""
        text = "Here is [a real link](link.com) and here is ![an image](image.png). Another [link 2](link2.net)."
        expected = [("a real link", "link.com"), ("link 2", "link2.net")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_url_with_special_chars(self):
        """Tests a URL with common special characters."""
        text = "Link with complex URL: [Docs](https://docs.example.com/search?q=test&page=2#results)"
        expected = [("Docs", "https://docs.example.com/search?q=test&page=2#results")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_link_text_with_special_chars(self):
        """Tests link text with spaces and punctuation."""
        text = "Link with complex text: [Click Here! (Important)](important.html)"
        expected = [("Click Here! (Important)", "important.html")]
        self.assertListEqual(expected, extract_markdown_links(text))
 
        #def test_link_with_nested_brackets_simple(self):
        #    """Tests link text containing brackets (basic case)."""
            # Behavior might depend on regex greediness. Non-greedy (.*?) is used.
        #    text = "Link with [nested brackets] inside: [See [Section 2]](section2.html)"
        #    expected = [("See [Section 2]", "section2.html")]
            # Note: More complex nesting might require more advanced parsing.
        #    self.assertListEqual(expected, extract_markdown_links(text))

    
    def test_link_inside_formatting(self):
        """Tests links enclosed in other Markdown formatting like bold/italics."""
        text = "A **[bold link](bold.url)** and an *[italic link](italic.url)*."
        expected = [("bold link", "bold.url"), ("italic link", "italic.url")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_no_match_for_malformed_syntax(self):
        """Tests that malformed link syntax is not matched."""
        text = "Malformed: [link(url) or [link]url)"
        expected = []
        self.assertListEqual(expected, extract_markdown_links(text))

    """
        def test_extract_markdown_url(self):
            matches = extract_markdown_url(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
            )
            self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    """

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    # Test original proporcionado para referencia
    def test_split_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    # Test: Nodo sin imágenes
    def test_split_no_images(self):
        node = TextNode("This is just plain text without images.", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just plain text without images.", TextType.NORMAL),
            ],
            new_nodes,
        )

    # Test: Nodo que contiene solo una imagen
    def test_split_image_only(self):
        node = TextNode("![only image](https://example.com/image.jpg)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("only image", TextType.IMAGE, "https://example.com/image.jpg"),
            ],
            new_nodes,
        )

    # Test: Imagen al inicio del texto
    def test_split_image_at_start(self):
        node = TextNode("![start image](start.png) followed by text.", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start image", TextType.IMAGE, "start.png"),
                TextNode(" followed by text.", TextType.NORMAL),
            ],
            new_nodes,
        )

    # Test: Imagen al final del texto
    def test_split_image_at_end(self):
        node = TextNode("Text precedes ![end image](end.png)", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text precedes ", TextType.NORMAL),
                TextNode("end image", TextType.IMAGE, "end.png"),
            ],
            new_nodes,
        )

    # Test: Múltiples nodos, algunos con imágenes y otros no
    def test_split_multiple_nodes_mixed(self):
        nodes = [
            TextNode("This is the first node. ", TextType.NORMAL),
            TextNode("Second node with ![img1](1.jpg). ", TextType.NORMAL),
            TextNode("Third node is plain.", TextType.NORMAL),
            TextNode("Fourth with ![img2](2.png) and ![img3](3.gif) images.", TextType.NORMAL),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is the first node. ", TextType.NORMAL),
                TextNode("Second node with ", TextType.NORMAL),
                TextNode("img1", TextType.IMAGE, "1.jpg"),
                TextNode(". ", TextType.NORMAL),
                TextNode("Third node is plain.", TextType.NORMAL),
                TextNode("Fourth with ", TextType.NORMAL),
                TextNode("img2", TextType.IMAGE, "2.png"),
                TextNode(" and ", TextType.NORMAL),
                TextNode("img3", TextType.IMAGE, "3.gif"),
                TextNode(" images.", TextType.NORMAL),
            ],
            new_nodes,
        )

    # Test: Imágenes adyacentes sin texto intermedio
    def test_split_adjacent_images(self):
        node = TextNode("Text ![img1](1.png)![img2](2.png) more text", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text ", TextType.NORMAL),
                TextNode("img1", TextType.IMAGE, "1.png"),
                TextNode("img2", TextType.IMAGE, "2.png"),
                TextNode(" more text", TextType.NORMAL),
            ],
            new_nodes,
        )

    # Test: Lista de nodos vacía como entrada
    def test_split_empty_input_list(self):
        nodes = []
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual([], new_nodes)

    # Test: Nodo con texto vacío (aunque podría ser un caso raro)
    def test_split_empty_text_node(self):
        node = TextNode("", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        # Dependiendo de la implementación, podría devolver una lista vacía
        # o una lista con el nodo original si no se encuentra nada que dividir.
        # Asumiremos que devuelve el nodo original si no hay imágenes.
        self.assertListEqual(
             [TextNode("", TextType.NORMAL)],
             new_nodes
        )
        # Alternativa si se espera una lista vacía para nodos vacíos:
        # self.assertListEqual([], new_nodes)


    # Test: Nodos que no son de tipo NORMAL (deberían pasarse sin modificar)
    # Asumiendo que split_nodes_image solo procesa nodos TextType.NORMAL
    def test_split_ignores_non_normal_nodes(self):
        # Suponiendo que tienes otros tipos como BOLD
        nodes = [
            TextNode("Some bold text", TextType.BOLD),
            TextNode("Normal text with ![an image](image.png) inside.", TextType.NORMAL),
            TextNode("Another bold text", TextType.BOLD),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Some bold text", TextType.BOLD),
                TextNode("Normal text with ", TextType.NORMAL),
                TextNode("an image", TextType.IMAGE, "image.png"),
                TextNode(" inside.", TextType.NORMAL),
                TextNode("Another bold text", TextType.BOLD),
            ],
            new_nodes,
        )
    
    def test_split_single_node_multiple_links(self):
        """Prueba dividir un solo nodo con múltiples enlaces."""
        node = TextNode(
            "Visita [Google](https://google.com) y también [Bing](https://bing.com) para buscar.",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Visita ", TextType.NORMAL),
            TextNode("Google", TextType.LINK, "https://google.com"),
            TextNode(" y también ", TextType.NORMAL),
            TextNode("Bing", TextType.LINK, "https://bing.com"),
            TextNode(" para buscar.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_node_no_links(self):
        """Prueba un nodo que no contiene sintaxis de enlace."""
        node = TextNode("Este nodo no tiene enlaces.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Este nodo no tiene enlaces.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_node_only_link(self):
        """Prueba un nodo que contiene solo sintaxis de enlace."""
        node = TextNode("[SoloUnEnlace](https://ejemplo.com)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("SoloUnEnlace", TextType.LINK, "https://ejemplo.com"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_start(self):
        """Prueba un nodo donde la sintaxis de enlace está al principio."""
        node = TextNode("[EnlaceInicial](inicio.html) seguido de texto.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("EnlaceInicial", TextType.LINK, "inicio.html"),
            TextNode(" seguido de texto.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_at_end(self):
        """Prueba un nodo donde la sintaxis de enlace está al final."""
        node = TextNode("Texto que precede a [EnlaceFinal](fin.php)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Texto que precede a ", TextType.NORMAL),
            TextNode("EnlaceFinal", TextType.LINK, "fin.php"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_multiple_nodes_mixed_content(self):
        """Prueba dividir una lista con múltiples nodos, mezclados con/sin enlaces."""
        nodes = [
            TextNode("Primer nodo, texto plano. ", TextType.NORMAL),
            TextNode("Segundo con [enlace1](url1.com). ", TextType.NORMAL),
            TextNode("Tercero plano.", TextType.NORMAL),
            TextNode("Cuarto [enlace2](url2.net)[enlace3](url3.org) adyacentes.", TextType.NORMAL),
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Primer nodo, texto plano. ", TextType.NORMAL),
            TextNode("Segundo con ", TextType.NORMAL),
            TextNode("enlace1", TextType.LINK, "url1.com"),
            TextNode(". ", TextType.NORMAL),
            TextNode("Tercero plano.", TextType.NORMAL),
            TextNode("Cuarto ", TextType.NORMAL),
            TextNode("enlace2", TextType.LINK, "url2.net"),
            TextNode("enlace3", TextType.LINK, "url3.org"),
            TextNode(" adyacentes.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_adjacent_links_no_text_between(self):
        """Prueba un nodo con dos enlaces directamente uno al lado del otro."""
        node = TextNode("Texto [link1](1.html)[link2](2.html) Más texto", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Texto ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "1.html"),
            TextNode("link2", TextType.LINK, "2.html"),
            TextNode(" Más texto", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_empty_input_list(self):
        """Prueba llamar la función con una lista vacía."""
        nodes = []
        new_nodes = split_nodes_link(nodes)
        expected = []
        self.assertListEqual(expected, new_nodes)

    def test_split_ignores_non_normal_nodes(self):
        """Prueba que los nodos que no son de tipo NORMAL se pasan sin cambios."""
        nodes = [
            TextNode("Esto es negrita", TextType.BOLD),
            TextNode("Texto normal con [un enlace](enlace.com).", TextType.NORMAL),
            TextNode("ya_es_un_enlace", TextType.LINK, "existente.org"), # Nodo que ya es LINK
        ]
        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode("Esto es negrita", TextType.BOLD),
            TextNode("Texto normal con ", TextType.NORMAL),
            TextNode("un enlace", TextType.LINK, "enlace.com"),
            TextNode(".", TextType.NORMAL),
            TextNode("ya_es_un_enlace", TextType.LINK, "existente.org"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_link_with_empty_text(self):
        """Prueba dividir un enlace con texto vacío (menos común)."""
        node = TextNode("Enlace con texto vacío: [](destino.html)", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Enlace con texto vacío: ", TextType.NORMAL),
            TextNode("", TextType.LINK, "destino.html"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_does_not_split_images(self):
        """Prueba que la sintaxis de imagen no se confunda con un enlace."""
        node = TextNode("Esto es ![una imagen](img.png), no un enlace.", TextType.NORMAL)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Esto es ![una imagen](img.png), no un enlace.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, new_nodes)


    def test_example_provided(self):
        """Prueba el ejemplo completo proporcionado en la descripción."""
        md_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, nodes)

    def test_plain_text(self):
        """Prueba con texto sin ningún formato Markdown."""
        md_text = "Just some plain text without any special formatting."
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("Just some plain text without any special formatting.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_bold(self):
        """Prueba con texto que solo contiene negrita."""
        md_text = "**bold text**"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_italic(self):
        """Prueba con texto que solo contiene cursiva."""
        md_text = "_italic text_"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_code(self):
        """Prueba con texto que solo contiene código."""
        md_text = "`code here`"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("code here", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_image(self):
        """Prueba con texto que solo contiene una imagen."""
        md_text = "![alt text](image.png)"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("alt text", TextType.IMAGE, "image.png"),
        ]
        self.assertListEqual(expected, nodes)

    def test_only_link(self):
        """Prueba con texto que solo contiene un enlace."""
        md_text = "[link text](https://example.com)"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("link text", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(expected, nodes)

    def test_bold_and_italic(self):
        """Prueba una combinación de negrita y cursiva con texto normal."""
        md_text = "Normal **bold part** normal _italic part_ end."
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("Normal ", TextType.NORMAL),
            TextNode("bold part", TextType.BOLD),
            TextNode(" normal ", TextType.NORMAL),
            TextNode("italic part", TextType.ITALIC),
            TextNode(" end.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, nodes)

    def test_text_with_image_and_link(self):
        """Prueba texto normal mezclado con imagen y enlace."""
        md_text = "Check out ![this image](img.jpg) and [this link](page.html)."
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("Check out ", TextType.NORMAL),
            TextNode("this image", TextType.IMAGE, "img.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("this link", TextType.LINK, "page.html"),
            TextNode(".", TextType.NORMAL),
        ]
        self.assertListEqual(expected, nodes)

    def test_markdown_at_start(self):
        """Prueba cuando un elemento Markdown está al inicio del texto."""
        md_text = "**Start bold** then normal text."
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("Start bold", TextType.BOLD),
            TextNode(" then normal text.", TextType.NORMAL),
        ]
        self.assertListEqual(expected, nodes)

    def test_markdown_at_end(self):
        """Prueba cuando un elemento Markdown está al final del texto."""
        md_text = "Normal text ends with `code`"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("Normal text ends with ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        self.assertListEqual(expected, nodes)

    def test_adjacent_markdown(self):
        """Prueba elementos Markdown uno directamente después del otro."""
        md_text = "Adjacent **bold**_italic_`code`[link](url)![img](img_url)"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("Adjacent ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("link", TextType.LINK, "url"),
            TextNode("img", TextType.IMAGE, "img_url"),
        ]
        self.assertListEqual(expected, nodes)

    def test_empty_string(self):
        """Prueba con una cadena de entrada vacía."""
        md_text = ""
        nodes = text_to_textnodes(md_text)
        expected = [] # Una cadena vacía no debería producir nodos
        self.assertListEqual(expected, nodes)

    def test_string_with_only_spaces(self):
        """Prueba con una cadena que solo contiene espacios."""
        md_text = "   "
        nodes = text_to_textnodes(md_text)
        # Se espera que los espacios se traten como texto normal
        expected = [TextNode("   ", TextType.NORMAL)]
        self.assertListEqual(expected, nodes)

    #def test_delimiters_without_content(self):
    #    """Prueba delimitadores sin contenido dentro (deberían tratarse como texto normal)."""
        # Nota: El comportamiento exacto aquí puede depender de la implementación deseada.
        # Esta prueba asume que los delimitadores vacíos o sin cerrar se tratan como texto literal.
    #    md_text = "Text with **** empty bold and __ empty italic and `` empty code."
    #    nodes = text_to_textnodes(md_text)
    #    expected = [
    #        TextNode("Text with **** empty bold and __ empty italic and `` empty code.", TextType.NORMAL),
    #    ]
    #    self.assertListEqual(expected, nodes)

    def test_image_and_link_distinction(self):
        """Asegura que los enlaces y las imágenes se distinguen correctamente."""
        md_text = "[not an image](link.url) and ![not a link](image.url)"
        nodes = text_to_textnodes(md_text)
        expected = [
            TextNode("not an image", TextType.LINK, "link.url"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("not a link", TextType.IMAGE, "image.url"),
        ]
        self.assertListEqual(expected, nodes)




    def test_example_provided(self):
        """Prueba el ejemplo proporcionado en la descripción."""
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        # La implementación debe eliminar el espacio inicial/final implícito por los """
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(expected, blocks)

    def test_multiple_blank_lines(self):
        """Prueba la división con múltiples líneas en blanco entre bloques."""
        md = """
Block 1



Block 2


Block 3
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "Block 1",
            "Block 2",
            "Block 3",
        ]
        self.assertListEqual(expected, blocks)

    def test_no_blank_lines(self):
        """Prueba texto sin líneas en blanco (debería ser un solo bloque)."""
        md = """Line 1
Line 2
Line 3 is part of the same block."""
        blocks = markdown_to_blocks(md)
        expected = [
            "Line 1\nLine 2\nLine 3 is part of the same block."
        ]
        self.assertListEqual(expected, blocks)

    def test_leading_trailing_whitespace_input(self):
        """Prueba con espacios en blanco al inicio y final del texto de entrada."""
        md = """   
Leading space block.

Middle block.

Trailing space block.   
"""
        # La función debe eliminar los espacios alrededor de los bloques.
        blocks = markdown_to_blocks(md)
        expected = [
            "Leading space block.",
            "Middle block.",
            "Trailing space block.",
        ]
        self.assertListEqual(expected, blocks)

    def test_whitespace_within_blocks(self):
        """
        Prueba que los espacios/tabulaciones DENTRO de un bloque se conserven,
        pero los que rodean al bloque completo sean eliminados.
        """
        md = """
        Block with   spaces.

          Indented block line 1
          Indented block line 2
        
        """ # Espacios extra al inicio y final de este bloque
        blocks = markdown_to_blocks(md)
        expected = [
            "Block with   spaces.",
            # El indentado interno se conserva, pero no los espacios que rodeaban
            # a este bloque en la cadena original md.
            "Indented block line 1\n          Indented block line 2"
        ]
        self.assertListEqual(expected, blocks)

    def test_explicit_block_stripping(self):
        """
        Prueba explícitamente que los espacios al inicio/final de un bloque
        sean eliminados.
        """
        md = """   Block 1 content   

  \t Block 2 line 1
Block 2 line 2 \t\n\n\t Block 3 \t"""
        blocks = markdown_to_blocks(md)
        expected = [
            "Block 1 content", # Espacios eliminados
            "Block 2 line 1\nBlock 2 line 2", # Espacios/tabs eliminados al inicio/final
            "Block 3" # Espacios/tabs eliminados
        ]
        self.assertListEqual(expected, blocks)


    def test_empty_string_input(self):
        """Prueba con una cadena de entrada vacía."""
        md = ""
        blocks = markdown_to_blocks(md)
        expected = []
        self.assertListEqual(expected, blocks)

    def test_whitespace_only_input(self):
        """Prueba con una cadena que solo contiene espacios y saltos de línea."""
        md = """   

\t\t
  
"""
        blocks = markdown_to_blocks(md)
        expected = [] # No hay contenido real, solo espacios en blanco
        self.assertListEqual(expected, blocks)

    def test_single_block_no_newlines(self):
        """Prueba con un solo bloque sin saltos de línea internos."""
        md = "   Just one single block surrounded by spaces.   "
        blocks = markdown_to_blocks(md)
        expected = ["Just one single block surrounded by spaces."] # Espacios eliminados
        self.assertListEqual(expected, blocks)

    def test_single_block_with_newlines(self):
        """
        Prueba con un solo bloque que contiene saltos de línea internos
        y espacios al inicio/final.
        """
        md = " \nLine one\nLine two\nStill the same block. \t"
        blocks = markdown_to_blocks(md)
        # El \n inicial y el \t final deben ser eliminados por strip()
        expected = ["Line one\nLine two\nStill the same block."]
        self.assertListEqual(expected, blocks)



    """Suite de tests para la función block_to_block_type."""

    def test_heading_1(self):
        """Prueba la identificación de un encabezado H1."""
        block = "# Heading 1"
        self.assertEqual(BlockType.HEADING_1, block_to_block_type(block))

    def test_heading_6(self):
        """Prueba la identificación de un encabezado H6."""
        block = "###### Heading 6"
        self.assertEqual(BlockType.HEADING_6, block_to_block_type(block))

    def test_heading_invalid_level(self):
        """Prueba que más de 6 '#' no se considera encabezado."""
        block = "####### Not a Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_heading_no_space(self):
        """Prueba que '#' sin espacio después no es un encabezado."""
        block = "#NoSpaceHeading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_code_block(self):
        """Prueba la identificación de un bloque de código."""
        block = "```\ndef main():\n    print('hello')\n```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_code_block_incomplete(self):
        """Prueba un bloque que parece código pero no cierra (debería ser párrafo)."""
        # Asumiendo que la función recibe el bloque tal cual.
        # Si markdown_to_blocks garantiza bloques válidos, este test podría no aplicar.
        block = "```\nprint('oops')"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_quote_block_single_line(self):
        """Prueba la identificación de una cita de una línea."""
        block = "> This is a quote."
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_quote_block_multi_line_with_one_empty(self):
        """Prueba la identificación de una cita de una línea."""
        block = """> A fist line\n> A second line\n>\n> Last line."""
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_quote_block_multi_line(self):
        """Prueba la identificación de una cita de múltiples líneas."""
        block = "> First line.\n> Second line.\n> Third line."
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_quote_block_mixed(self):
        """Prueba un bloque donde no todas las líneas son citas (debería ser párrafo)."""
        block = "> First line is quote.\nSecond line is not."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_unordered_list_asterisk(self):
        """Prueba lista no ordenada con '*'."""
        block = "* Item 1\n* Item 2"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_unordered_list_dash(self):
        """Prueba lista no ordenada con '-'."""
        block = "- Item A\n- Item B"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_unordered_list_mixed_markers(self):
        """Prueba lista no ordenada con marcadores mixtos (debería ser párrafo)."""
        block = "* Item 1\n- Item B"
        # Según reglas estrictas donde todas las líneas deben coincidir, esto sería párrafo.
        # Si se permite mezcla, el test debería esperar UNORDERED_LIST. Asumimos estricto.
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_unordered_list_invalid_line(self):
        """Prueba lista no ordenada donde una línea no coincide (debería ser párrafo)."""
        block = "* Item 1\nThis is not a list item\n* Item 3"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_ordered_list(self):
        """Prueba una lista ordenada válida."""
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ordered_list_single_item(self):
        """Prueba una lista ordenada con un solo elemento."""
        block = "1. Only item"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ordered_list_incorrect_start(self):
        """Prueba una lista ordenada que no empieza en 1 (debería ser párrafo)."""
        block = "2. Starts at two\n3. Continues"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_ordered_list_incorrect_sequence(self):
        """Prueba una lista ordenada con secuencia incorrecta (debería ser párrafo)."""
        block = "1. First\n3. Third (skipped second)"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_ordered_list_invalid_line(self):
        """Prueba lista ordenada donde una línea no coincide (debería ser párrafo)."""
        block = "1. First\nThis is not an item\n2. Second"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_paragraph_simple(self):
        """Prueba un párrafo simple."""
        block = "This is just a plain paragraph."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_paragraph_with_inline_markdown(self):
        """Prueba un párrafo con formato Markdown inline."""
        block = "This paragraph has **bold** and _italic_ text."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_paragraph_resembling_list(self):
        """Prueba texto que parece lista pero no sigue las reglas."""
        block = "1- Not an ordered list.\n*Not an unordered list either."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_paragraph_resembling_quote(self):
        """Prueba texto que parece cita pero no sigue las reglas."""
        block = ">This is not a quote (no space)."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))



    """Suite de tests para la conversión de Markdown a HTML."""

    def test_paragraphs(self):
        """Prueba la conversión de párrafos simples y con formato inline."""
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Asume que el nodo raíz es un div que envuelve los bloques
        expected_html = "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(expected_html, html)

    def test_headings(self):
        """Prueba la conversión de diferentes niveles de encabezados."""
        md = """
# Heading 1

Some text.

## Heading 2 with _italic_

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><h1>Heading 1</h1><p>Some text.</p><h2>Heading 2 with <i>italic</i></h2><h6>Heading 6</h6></div>"
        self.assertEqual(expected_html, html)

    def test_code_block(self):
        """Prueba la conversión de bloques de código."""
        md = """
Paragraph before.

```
def hello():
  print("Hello, world!")
```

Paragraph after.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # El contenido dentro de <pre><code> debe preservar espacios y saltos de línea
        # y no procesar Markdown inline.
        expected_html = '<div><p>Paragraph before.</p><pre><code>def hello():\n  print("Hello, world!")\n</code></pre><p>Paragraph after.</p></div>'
        self.assertEqual(expected_html, html)

    def test_quote_block(self):
        """Prueba la conversión de bloques de cita."""
        md = """
> This is a quote.
> It spans **multiple** lines.

Followed by a paragraph.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Las citas a menudo se envuelven en <p> dentro de <blockquote> si la implementación lo hace.
        # Asumiremos aquí una conversión directa del contenido.
        expected_html = "<div><blockquote>This is a quote.\nIt spans <b>multiple</b> lines.</blockquote><p>Followed by a paragraph.</p></div>"
        # Alternativa si cada línea de la cita va en un <p>:
        # expected_html = "<div><blockquote><p>This is a quote.</p><p>It spans <b>multiple</b> lines.</p></blockquote><p>Followed by a paragraph.</p></div>"
        self.assertEqual(expected_html, html)

    def test_unordered_list(self):
        """Prueba la conversión de listas no ordenadas."""
        md = """
* Item 1
* Item 2 with `code`
* Item 3

Alternatively:

- Dash Item 1
- Dash Item 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = "<div><ul><li>Item 1</li><li>Item 2 with <code>code</code></li><li>Item 3</li></ul><p>Alternatively:</p><ul><li>Dash Item 1</li><li>Dash Item 2</li></ul></div>"
        self.assertEqual(expected_html, html)

    def test_ordered_list(self):
        """Prueba la conversión de listas ordenadas."""
        md = """
1. First item
2. Second item with a [link](https://example.com)
3. Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = '<div><ol><li>First item</li><li>Second item with a <a href="https://example.com">link</a></li><li>Third item</li></ol></div>'
        self.assertEqual(expected_html, html)

    def test_mixed_content(self):
        """Prueba una mezcla de varios tipos de bloques."""
        md = """
# Document Title

Introduction paragraph with ![alt text](image.png).

> A quote block.

## Section

* Point 1
* Point 2

1. Step 1
2. Step 2

```
Final code snippet
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Nota: La representación de <img> requiere manejo de etiquetas auto-cerradas.
        # La implementación simple de to_html() arriba no lo haría bien.
        # Asumimos una implementación correcta para la expectativa.
        expected_html = ('<div><h1>Document Title</h1>'
                         '<p>Introduction paragraph with <img src="image.png" alt="alt text">.</p>'
                         '<blockquote>A quote block.</blockquote>'
                         '<h2>Section</h2>'
                         '<ul><li>Point 1</li><li>Point 2</li></ul>'
                         '<ol><li>Step 1</li><li>Step 2</li></ol>'
                         '<pre><code>Final code snippet\n</code></pre>'
                         '</div>')
        self.maxDiff = None
        self.assertEqual(expected_html, html)

    def test_simple_h1(self):
        """Prueba un encabezado H1 simple."""
        md = "# Hello"
        expected = "Hello"
        self.assertEqual(expected, extract_title(md))

    def test_h1_with_leading_trailing_spaces_line(self):
        """Prueba un H1 con espacios antes y después en la línea."""
        md = "\n\t# Hello \t"
        expected = "Hello"
        self.assertEqual(expected, extract_title(md))

    def test_h1_with_leading_trailing_spaces_title(self):
        """Prueba un H1 con espacios extra alrededor del texto del título."""
        md = "#   Hello World   "
        expected = "Hello World"
        self.assertEqual(expected, extract_title(md))

    def test_h1_buried_in_text(self):
        """Prueba un H1 que no está en la primera línea."""
        md = "Some introductory text.\n\n# The Actual Title\n\nMore text."
        expected = "The Actual Title"
        self.assertEqual(expected, extract_title(md))

    def test_multiple_h1_returns_first(self):
        """Prueba que devuelve el primer H1 si hay varios."""
        md = "Text\n# First Title\nMore text\n# Second Title"
        expected = "First Title"
        self.assertEqual(expected, extract_title(md))

    def test_empty_title_h1(self):
        """Prueba un H1 válido pero sin texto (solo '# ')."""
        md = "# "
        with self.assertRaisesRegex(ValueError, "No level 1 heading found"):
            extract_title(md)

    def test_h2_raises_error(self):
        """Prueba que un H2 (##) no es detectado y lanza ValueError."""
        md = "## Not an H1 Title"
        # Verifica que la función extract_title(md) lanza un ValueError
        with self.assertRaisesRegex(ValueError, "No level 1 heading found"):
            extract_title(md)
            
    def test_h3_raises_error(self):
        """Prueba que un H3 (###) no es detectado y lanza ValueError."""
        md = "### Not an H1 Title"
        with self.assertRaisesRegex(ValueError, "No level 1 heading found"):
            extract_title(md)

    def test_no_headings_raises_error(self):
        """Prueba que texto sin ningún encabezado lanza ValueError."""
        md = "This is just plain text.\nNo headings here."
        with self.assertRaisesRegex(ValueError, "No level 1 heading found"):
            extract_title(md)

    def test_text_starting_with_hash_but_not_h1_raises_error(self):
        """Prueba texto que empieza con # pero no es H1 (falta espacio)."""
        md = "#NotATitle\nSome other text"
        with self.assertRaisesRegex(ValueError, "No level 1 heading found"):
            extract_title(md)
            
    def test_empty_string_raises_error(self):
        """Prueba que un string vacío lanza ValueError."""
        md = ""
        with self.assertRaisesRegex(ValueError, "No level 1 heading found"):
            extract_title(md)

    def test_only_whitespace_string_raises_error(self):
        """Prueba que un string con solo espacios/saltos de línea lanza ValueError."""
        md = "\n  \t \n"
        with self.assertRaisesRegex(ValueError, "No level 1 heading found"):
            extract_title(md)
            
    def test_h1_followed_by_h2(self):
        """Prueba que encuentra el H1 incluso si hay otros encabezados después."""
        md = "Intro\n# The Main Title\n## A Subtitle\nMore text."
        expected = "The Main Title"
        self.assertEqual(expected, extract_title(md))
