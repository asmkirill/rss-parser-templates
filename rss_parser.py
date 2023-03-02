from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import xml.etree.ElementTree as ET
import html
import re
import unicodedata


# Function that processes the text data by converting HTML entities to their corresponding characters,
# normalizing the text, and removing any non-ASCII characters.

def re_esc_ch(text):
    if text is not None:
        text = html.unescape(text)
        text = text.replace('\xa0', ' ')
        text = unicodedata.normalize('NFKC', text)
        text = re.sub(r'[^\x00-\x7F]+|\s+', ' ', re.sub(r'<.*?>', '', text)).strip()
    return text


def rss_parser(xml, limit=2, json=False):

"""
    The xml.etree.ElementTree library is a standard Python library for working with XML data.
    Using an alias "js" help avoid naming conflicts with "json" module in parameter (argument).
"""

    import json as js
    root = ET.fromstring(xml)

    channel_list = []
    channel = root.find("channel")
    categories_ch_list = []
    for category in channel.findall("category"):
        categories_ch_list.append(category.text)
    channel_list.append({
        "title": re_esc_ch(channel.find("title").text) if channel.find("title") is not None else "",
        "link": channel.find("link").text if channel.find("link") is not None else "",
        "lastBuildDate": channel.find("lastBuildDate").text if channel.find("lastBuildDate") is not None else "",
        "pubDate": channel.find("pubDate").text if channel.find("pubDate") is not None else "",
        "language": channel.find("language").text if channel.find("language") is not None else "",
        "category": categories_ch_list,
        "managinEditor": channel.find("managinEditor").text if channel.find("managinEditor") is not None else "",
        "description": re_esc_ch(channel.find("description").text) if channel.find("description") is not None else "",
    })


"""
    An alternative way to parse is use the BeautifulSoup library instead of the ET.
    It is an external library that !!! needs to be installed separately!!! 
"""

from bs4 import BeautifulSoup

    soup = BeautifulSoup(xml, 'xml')
    url = soup.find('link').text
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'xml')
    channel = soup.findAll("channel")
    channel_list = []


# Design the output for JSON format by creating dictionaries and lists
# for the channel and items data. Use a counter to limit the number of news to be printed

    if json:
        counter = 0
        items_list = []
        for item in root.findall(".//item"):
            if counter == limit:
                break
            item_dict = {}
            title_elem = item.find("title")
            if title_elem is not None:
                item_dict["title"] = re_esc_ch(title_elem.text)
            author_elem = item.find("author")
            if author_elem is not None:
                item_dict["author"] = re_esc_ch(author_elem.text)
            pubdate_elem = item.find("pubDate")
            ...

"""
    It returns the JSON representation of output_dict using the dumps method from the json module. 
    The indent parameter format the output JSON string with indentation for improved readability.
"""
        output_dict["items"] = items_list
        return js.dumps(output_dict, indent=2)


# The resulting output_list contains the extracted data elements from the XML feed,
# which can be printed or otherwise in CONSOLE output format.

    else:
        tree = ET.fromstring(xml)
        channel = tree.find('channel')
        output_list = []
        output_list.append(f"Feed: {channel.find('title').text}"
                           ) if channel.find("title") is not None else ""
        output_list.append(f"Link: {channel.find('link').text}"
                           ) if channel.find("link") is not None else ""
        ...

        counter_console = 0
        for item in channel.findall('item'):
            if counter_console == limit:
                break
            try:
                title = item.find('title').text
                output_list.append(f"Title: {title}") if channel.find("title") is not None else ""
            except:
                ""
            try:
                author = item.find('author').text
                output_list.append(f"Author: {author}") if channel.find("author") is not None else ""
            except:
                ""
            ...

            counter_console += 1
        return output_list



# Function allows for checking the parser with two different output formats: JSON and console.
# Choose the limit of news to be displayed, and set the format parameter (json=False will output in console format).

def main():
    url = "https://news.un.org/feed/subscribe/en/news/region/europe/feed/rss.xml"

    response = requests.get(url)
    xml = response.text

        # For JSON output:

    ress = rss_parser(xml, limit=2, json=True)
    print(ress)

        # For CONSOLE output:

    print("\n".join(rss_parser(xml)))

if __name__ == "__main__":
    main()

