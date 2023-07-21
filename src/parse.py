from bs4 import BeautifulSoup, Comment
import re
import requests
import json
import PyPDF2
import io

def process_soup(url: str, soup) -> tuple:
    # Figure out the base url
    base_url = url.split('/')[0] + '//' + url.split('/')[2]
    # Remove scripts, meta and styles
    for script in soup(["script", "style", "meta"]):
        script.decompose()
    # Replace relative links with absolute links
    for link in soup.find_all('a'):
        href = link.attrs.get('href', '')
        if href.startswith('#'):
            link.decompose()
        elif href.startswith('/') or href.startswith('./'):
            link.attrs['href'] = base_url + href
    # Remove all attributes that are not href, src
    for tag in soup.find_all(True):
        tag.attrs = {key: value for key, value in tag.attrs.items() if key in ['href', 'src']}
    # Remove all links that refer to js, php, css, etc. in a and link tags
    for tag in soup.find_all(['a', 'link']):
        if not tag.attrs:
            continue
        href = tag.attrs.get('href', '')
        if href and href.endswith(('.js', '.php', '.css', '.html', '.htm')):
            tag.decompose()
    # Remove head
    for head in soup.find_all('head'):
        head.decompose()
    # Remove hidden elements
    for tag in soup.find_all(lambda tag: 'style' in tag.attrs and ('display: none' in tag['style'] or 'visibility: hidden' in tag['style'])):
        #print("Removing hidden element", tag) # TODO: Test
        tag.decompose()
    # Remove elements with only links that have no children
    for tag in soup.find_all(lambda tag: tag.name == 'p' and all(x.name == 'a' for x in tag.children)):
        #print("Removing element with only links", tag) # TODO: Test
        if tag.parent:
            tag.parent.decompose()
        #tag.decompose()
    # Remove comments
    comments = soup.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    # TODO: Tables
    # Unwrap all divs
    for div in soup.find_all('div'):
        div.unwrap()
    # Remove empty spans, labels, etc.
    action_performed = True
    while action_performed:
        action_performed = False
        for element in soup.find_all(['span', 'label', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if not element.text.strip():
                element.decompose()
                action_performed = True
    return soup

def soup_to_markdown(soup):
    elements = []
    for element in soup.find_all(recursive=False):
        elements.append(element_to_markdown(element))
    md = '\n\n'.join(elements)
    # Post-processing
    # Remove multiple newlines
    md = re.sub(r'\n+', '\n\n', md)
    # Remove multiple spaces
    md = re.sub(r' +', ' ', md)
    # Remove empty paragraphs
    md = re.sub(r'^\s+$', '', md, flags=re.MULTILINE)
    # Remove empty headers
    md = re.sub(r'^#+\s+$', '', md, flags=re.MULTILINE)
    # Remove newlines between list items
    md = re.sub(r'\n\* ', '\n* ', md)
    # Remove the first space of the line if there is only one
    md = re.sub(r'^\s+', '', md, flags=re.MULTILINE)
    # Remove trailing spaces
    md = re.sub(r'\s+$', '', md, flags=re.MULTILINE)
    # Remove empty links
    md = re.sub(r'^\[\]\(\)\s+$', '', md, flags=re.MULTILINE)
    return md

def element_to_markdown(element):
    tag = element.name
    markdown = ''

    if tag is None:
        # Base case: if the element is a NavigableString, just return its text
        return element.strip()

    if re.match(r'h\d', tag):
        markdown = '\n\n' + '#' * int(tag[1]) + ' ' + element.text.strip() + '\n\n'

    elif tag == 'a':
        markdown = '[' + element.text.strip() + '](' + element.attrs.get('href', '') + ') '

    elif tag == 'p':
        markdown = '\n\n' + ' '.join(element_to_markdown(child) if child.name else child for child in element.children).strip() + '\n\n'

    elif tag in ['ul', 'ol']:
        list_items = [element_to_markdown(child) for child in element.children if child.name]
        # remove empty list items
        list_items = [item for item in list_items if item.strip() != '*']
        markdown = '\n'.join(list_items).strip() + '\n'

    elif tag == 'li':
        markdown_item = ' '.join(element_to_markdown(child) if child.name else child for child in element.children).strip()
        # only add to markdown if the list item is not empty
        if markdown_item:
            markdown = '* ' + markdown_item + '\n'

    elif tag == 'span' and 'table-placeholder' in element.attrs.get('class', []):
        markdown = f'\n<!-- TABLE PLACEHOLDER {element.attrs.get("id", "")} -->\n'

    elif tag == 'img':
        markdown = f'![{element.attrs.get("alt", "")}]({element.attrs.get("src", "")})\n'

    else:
        # If the tag is none of the above, just process its children
        markdown = ' '.join(element_to_markdown(child) if child.name else child for child in element.children).strip()

    return markdown

def html_to_readable_text(response):
    url = response.url
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    soup = process_soup(url, soup)
    return soup_to_markdown(soup)

def json_to_readable_text(response):
    data = response.json()
    string = json.dumps(data, indent=0)
    # Remove all whitespace
    string = re.sub(r'\s+', '', string)
    # Remove quotes to reduce number of tokens
    string = re.sub(r'"', '', string)
    return string

def pdf_to_readable_text(response):
    stream = io.BytesIO(response.content)
    reader = PyPDF2.PdfReader(stream)
    pages = reader.pages
    num_pages = len(pages)
    string = f"PDF file with {num_pages} pages found. Metadata: {reader.metadata} Content:\n"
    for i, page in enumerate(pages):
        string += f"Page ({i+1}/{num_pages}):\n"
        string += page.extract_text ()
    return string

def plain_text_to_readable_text(response):
    return response.text

def csv_to_readable_text(response):
    return response.text

def parse_response(response):
    # Parse the response depending on the content type
    content_type = response.headers['Content-Type']
    if 'application/pdf' in content_type:
        return pdf_to_readable_text(response)
    elif 'text/html' in content_type:
        return html_to_readable_text(response)
    elif 'application/json' in content_type:
        return json_to_readable_text(response)
    elif 'text/plain' in content_type:
        return plain_text_to_readable_text(response)
    #elif 'application/msword' in content_type:
    #    return "Word document found"
    #elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
    #    return "Word document found"
    #elif 'application/vnd.ms-excel' in content_type:
    #    return "Excel document found"
    #elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
    #    return "Excel document found"
    #elif 'application/rtf' in content_type:
    #    return "RTF document found"
    elif 'text/csv' in content_type:
        return csv_to_readable_text(response)
    else:
        return f"{content_type} found at {response.url}. This file type is not supported and cannot be converted into readable text."

if __name__ == "__main__":
    import requests
    url = "https://openai.com/pricing"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    #with open("C:/users/i551984/Downloads/test_html.html", "r") as file:
    #    soup = BeautifulSoup(file.read(), 'html.parser')
    #    url = "https://en.wikipedia.org/wiki/Table_(information)"
    soup = process_soup(url, soup)
    soup_intermediate = soup.prettify()
    with open("test_intermediate.html", "w", encoding="utf-8") as file:
        file.write(soup_intermediate)

    md = soup_to_markdown(soup)
    #from IPython.display import Markdown, display
    #print(md)
    with open("test.md", "w", encoding="utf-8") as file:
        file.write(md)
    
    #orig = soup_to_markdown_orig(soup)
    #print(orig)
    #with open("test_orig.md", "w", encoding="utf-8") as file:
    #    file.write(orig)