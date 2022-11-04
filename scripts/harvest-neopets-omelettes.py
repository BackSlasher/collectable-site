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

class Item(NamedTuple):
    name: str
    img_url: str
    rarity: int

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

urls = [
    'https://items.jellyneo.net/search/?scat[]=22',
]

def parse_args():
    parser = argparse.ArgumentParser(description='Get some eggs')
    parser.add_argument('--output-csv', type=argparse.FileType('w'), required=False)
    parser.add_argument('--output-json', type=argparse.FileType('w'), required=False)
    parser.add_argument('--image-directory', type=str, required=True)
    parser.add_argument('url', type=str, nargs='+')

    return parser.parse_args()

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
    item = [Item(
        link.text,
        get_image_url(url, link),
        get_rarity(url, link),
    ) for link in links]
    return item

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

def download_images(images_dir, items):
    for item in items:
        extension = item.img_url.split('.')[-1]
        filename = os.path.join(images_dir, item.name + '.' + extension)
        r = get_url(item.img_url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        

def write_csv(file, items):
    outer = csv.writer(file)
    outer.writerow(['name', 'url', 'rarity'])
    for item in items:
        outer.writerow(item)

def write_json(file, items):
    out = json.dumps(items)
    file.write(out)

def main():
    args = parse_args()

    stuff=[]
    for url in urls:
        stuff.extend(process_url(url))

    if args.output_csv:
        write_csv(args.output_csv, stuff)
    if args.output_json:
        write_json(args.output_json, stuff)
        
    download_images(args.image_directory, stuff)


main()
# write_csv(stuff)
