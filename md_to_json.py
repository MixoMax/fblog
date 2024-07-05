import json
from markdown import Markdown
import bs4
import time

def convert_markdown_to_json(markdown_file_path: str) -> dict:
    """
    Convert markdown file to a structured JSON object

    example output:
    [
        {
            "tag": "h1",
            "text": "Title"
        },
        {
            "tag": "p",
            "text": "This is a paragraph"
        },
        {
            "tag": "div",
            "content": [
                {
                    "tag": "p",
                    "text": "This is a paragraph inside a div"
                },
                {
                    "tag": "p",
                    "text": "This is another paragraph inside a div"
                }
            ]
        },
        {
            "tag": "a",
            "text": "Link",
            "href": "http://example.com"
        },
        {
            "tag": "img",
            "src": "http://example.com/image.jpg",
            "alt": "Image"
        },
        {
            "tag": "code",
            "text": "print("Hello, World!")"
        },
        {
            "tag": "ul",
            "content": [
                {
                    "tag": "li",
                    "text": "Item 1"
                },
                {
                    "tag": "li",
                    "text": "Item 2"
                }
            ]
        }
    ]
    """

    md = Markdown()
    with open(markdown_file_path, "r", encoding="utf-8") as file:
        html = md.convert(file.read())
    
    soup = bs4.BeautifulSoup(html, "html.parser")
    
    
    return convert_soup_to_json(soup)

def convert_soup_to_json(soup: bs4.BeautifulSoup) -> dict:
    # Convert BeautifulSoup object to JSON

    json_data = []
    for element in soup:
        if element.name:
            json_data.append(convert_element_to_json(element))
    return json_data

def convert_element_to_json(element: bs4.Tag) -> dict:
    # Convert BeautifulSoup element to JSON

    json_element = {
        "tag": element.name
    }

    # get all html attributes
    for attr in element.attrs:
        json_element[attr] = element[attr]
    
    # get text content
    if element.text:
        json_element["text"] = element.text
    
    # get child elements
    if element.contents:
        json_element["content"] = convert_soup_to_json(element)
    
    return json_element


