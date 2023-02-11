# Collectables site

Visit once a day, add a random item to your collection.  
Everything is clientside, no server processing needed.  
Your collection is kept in the browser.  

## How to roll your own
1. Create a data directory.
   It should contain:
    1. an `items.json` file, with a JSON list of items. Each item should have the fields:
        1. name
        2. rarity: the higher the number, the rarer the item is
        3. info: trivia about the item
    2. an `images` directory, that should contain an image for each filename.
      No file extension (i.e. `Clay Omelette` and not `Clay Omelette.gif`)
2. Create an index.html file.
   It should have the following components:
    1. a "today" div for displaying the item we have today
    1. a "collection" div for showing off your collection
    1. a script reference to jquery
    1. a script reference to `collections.js`
    1. calling `initCollection` once the page loads
      It needs a dict with the following:
        1. `sourceDir`: where the `items.json` and `images` directory live
        2. `todayDiv`: jQuery selector for the div for today's item
        3. `collectionDiv`: jQuery select for the div for the collection
3. Host it on some webserver 
And you're good to go!

## Examples for data
I created `scripts/base.py` to easily create the data directory.  
To build a new collection, you'll need to:
1. Create a Python file and extend `ItemFetcher`
1. Implement `get_items` and return a list of `Item`
1. Instansiate the object with `destination_directory` and call `process()`.

You can check an example in `scripts/harvest-neopets-omelettes.py`