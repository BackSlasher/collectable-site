// https://stackoverflow.com/a/47593316
function cyrb128(str) {
    let h1 = 1779033703, h2 = 3144134277,
        h3 = 1013904242, h4 = 2773480762;
    for (let i = 0, k; i < str.length; i++) {
        k = str.charCodeAt(i);
        h1 = h2 ^ Math.imul(h1 ^ k, 597399067);
        h2 = h3 ^ Math.imul(h2 ^ k, 2869860233);
        h3 = h4 ^ Math.imul(h3 ^ k, 951274213);
        h4 = h1 ^ Math.imul(h4 ^ k, 2716044179);
    }
    h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067);
    h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
    h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213);
    h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
    return [(h1^h2^h3^h4)>>>0, (h2^h1)>>>0, (h3^h1)>>>0, (h4^h1)>>>0];
}

function sfc32(a, b, c, d) {
    return function() {
      a >>>= 0; b >>>= 0; c >>>= 0; d >>>= 0;
      var t = (a + b) | 0;
      a = b ^ b >>> 9;
      b = c + (c << 3) | 0;
      c = (c << 21 | c >>> 11);
      d = d + 1 | 0;
      t = t + d | 0;
      c = c + t | 0;
      return (t >>> 0) / 4294967296;
    }
}

function getToday() {
  const now = new Date();
  const today = new Date(now.toDateString());
  return today;
}

function weightedRandom(items) {
  const arrDeep = items.map(item => {
    const odds = (100 / item.rarity) * 100;
    const oddsInt = Math.floor(odds);
    return [...Array(oddsInt).keys()].map(n => item);
  });
  const arrFlat = [].concat(...arrDeep);
  const rand1 = cyrb128(getToday());
  const rand2 = sfc32(rand1[0], rand1[1], rand1[2], rand1[3])();
  const element = arrFlat[Math.floor(rand2 * arrFlat.length)];
  return element;
}

async function getItems(sourceDir) {
  const dat = await fetch('data/omelettes/items.json');
  const j = await dat.json();
  const items = j.map(i => {
    return ({
      name: i.name,
      image: (`${sourceDir}/images/${i.name}`),
      rarity: i.rarity,
    })
  });
  const todaysItem = weightedRandom(items);
  return {
    items,
    todaysItem,
  };
}

function canCollectToday() {
  const lastCollected = localStorage.getItem('lastCollected');
  if (lastCollected == null) {
    return true;
  }
  const today = getToday();
  return today > lastCollected;
}

function updateToday(todayDiv, todaysItem) {
  todayDiv.find("img").attr("src", todaysItem.image);
  todayDiv.find(".title").text(todaysItem.name);
}

// TODO read everything aside from the name from items
function updateCollection(collectionDiv, items) {
  const collection = JSON.parse(localStorage.getItem('collection') || '[]');
  // Clean everything
  collectionDiv.find("div.gallery").remove();
  // Build
  const divs = collection.map(i => {
    const item = items.find(ii => ii.name == i.name);
    const newDiv = $("<div class='gallery'><img /><div class='desc'><div class='title'></div><div class='date'></div></div></div>");
    newDiv.find("img").attr("src", item.image);
    newDiv.find("div.title").text(item.name);
    newDiv.find("div.date").text("Collected on " + new Date(i.collectedAt).toDateString());
    return newDiv;
  });
  // Append all divs
  divs.forEach(d => collectionDiv.append(d));
}

function collect(button, todaysItem, collectionDiv, items) {
  console.log("fffff");
  // Add item to collection
  // TODO move collection getting to a differen item
  let collection = JSON.parse(localStorage.getItem('collection') || '[]');
  const item = todaysItem;
  if (item == null) {
    console.log("item is null");
    return;
  }
  item.collectedAt = getToday();
  collection.push(item);
  localStorage.setItem('collection', JSON.stringify(collection));
  updateCollection(collectionDiv, items);
  // Update last collected
  localStorage.setItem('lastCollected', getToday());
  button.attr("disabled", true);
}

function updateCollectButton(todayDiv, todaysItem, collectionDiv, items) {
  // Find collect button
  const button = todayDiv.find("button.collect");
  // Enable / disable based on canCollectToday()
  const isEnabled = canCollectToday();
  button.attr("disabled", !isEnabled);
  button.click(function() {collect(button, todaysItem, collectionDiv,items)});
}

async function initCollection(settings) {
  const {sourceDir} = settings;
  const todayDiv = $(settings.todayDiv);
  const collectionDiv = $(settings.collectionDiv);

  const items = await getItems(sourceDir);
  const collection = JSON.parse(localStorage.getItem('collection') || '[]');

  updateToday(todayDiv, items.todaysItem);
  updateCollection(collectionDiv, items.items);
  updateCollectButton(todayDiv, items.todaysItem, collectionDiv, items.items);
}
