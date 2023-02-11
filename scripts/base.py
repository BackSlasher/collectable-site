from abc import ABC, abstractmethod
import os
import os.path
import json
import requests

from typing import NamedTuple, List
# import magic

class Item(NamedTuple):
    name: str
    image_blob: bytes
    rarity: int
    info: str

    def as_dict(self):
        return {
            'name': self.name,
            'rarity': self.rarity,
            'info': self.info,
        }

    def save_image(self, parent_directory):
        # TODO support extension using magic?
        dest = os.path.join(parent_directory, self.name)
        with open(dest, 'wb') as f:
            f.write(self.image_blob)


def write_items(items: List[Item], parent_directory: str):
    json_file = os.path.join(parent_directory, "items.json")

    item_list = [item.as_dict() for item in items]
    with open(json_file, "w") as f:
        json.dump(item_list, f)

    image_directory = os.path.join(parent_directory, "images")
    if not os.path.exists(image_directory):
        os.mkdir(image_directory)
    for item in items:
        item.save_image(image_directory)


class ItemFetcher(ABC):

    def __init__(self, destination_directory: str):
        self.destination_directory = destination_directory

    @abstractmethod
    def get_items(self):
        pass

    def process(self):
        items = self.get_items()
        write_items(items, self.destination_directory)
