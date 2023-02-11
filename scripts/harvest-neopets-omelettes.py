from base import Item, ItemFetcher, main

import os.path
import re
import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
import csv
from typing import NamedTuple
import json

import argparse

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

urls = [
    'https://items.jellyneo.net/search/?scat[]=22',
]

def get_url(url):
    return requests.get(url, headers=headers)

def get_soup(url):
    req = get_url(url)
    return BeautifulSoup(req.text, "html.parser")

def get_rarity(url, item):
    item_link = urljoin(url, item['href'])
    soup = get_soup(item_link)
    rarity_label = soup.find('h3', text='Rarity')
    rarity_p = rarity_label.parent.find('p')
    rarity = list(rarity_p.stripped_strings)[0]
    rarity = int(re.sub('^r', '', rarity))
    return rarity

def get_image_url(url, item):
    src = item.parent.find('img')['src']
    return urljoin(url, src)

def collect_items(url, soup):
    req = requests.get(url, headers=headers)
    links = soup.find_all('a')
    links = [l for l in links if 'Omelette' in l.text]
    links = [l for l in links if '/3' not in l.text]
    items = [Item(
        name = link.text,
        image_blob = get_url(get_image_url(url, link)).content,
        rarity = get_rarity(url, link),
        info = '',
    ) for link in links]
    return items

def process_url(url):
    soup = get_soup(url)
    items = collect_items(url, soup)
    next_page_link = soup.find("a", text="»")
    if next_page_link['href']:
        items.extend(
            process_url(
                urljoin(url, next_page_link['href'])
            )
        )
    return items

class OmeletteFetcher(ItemFetcher):
    def get_items(self):
        stuff=[]
        for url in urls:
            stuff.extend(process_url(url))
        return stuff

main(OmeletteFetcher)
