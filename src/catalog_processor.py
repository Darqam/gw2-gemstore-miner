import re
import sqlite3
import json
from datetime import datetime

import requests

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

FOLDER_NAME = "gw2cache-{0400000B-482B-25B7-0800-00042B48B725}"
TODAY = datetime.strptime("2021-02-02T00:00:00Z", DATETIME_FORMAT)

WIN_USER = "Sutgon"
URL_BASE_1 = f"C:\\Users\\{WIN_USER}\\AppData\\Local\\Temp\\"
URL_BASE_2 = "\\user\\Local Storage\\https_gemstore-fra-live.ncplatform.net_0.localstorage"
PATH = URL_BASE_1 + FOLDER_NAME + URL_BASE_2

new_names = [
  "Noble Aurochs Jackal Skin",
  "Hammer of the Three Realms Skin",
  "Infused Samurai Package",
  "Infused Blades Package",
  "Infused Samurai Outfit",
  ]


def get_catalog_url():
    # high ID ensures we always get the latest build
    r = requests.get("https://gemstore-live.ncplatform.net/?buildid=999999999999999999999")
    # regex searches up the catalog url from the source of the page, pretty, right?
    return re.search('(?<=src=").+catalog.+(?="\\sdefer)', r.text).group()


def get_catalog_object():
    r = requests.get(get_catalog_url())
    # get rid of trash at start
    search = re.compile("(?<=gemstoreCatalog\\s=\\s).+(?!.)", re.DOTALL)
    text = re.search(search, r.text).group()
    return json.loads(text)


def to_datetime(string):
    return datetime.strptime(string, DATETIME_FORMAT)


def get_local_gemstore_data():
    conn = sqlite3.connect(PATH)
    c = conn.cursor()
    c.execute("SELECT cast(value as varchar) FROM ItemTable")  # cast because data is in hex
    return c.fetchall()  # list of tuples of strings


data = get_local_gemstore_data()

dict_data = None
dict_data_time = None

for row_t in data:
    row = row_t[0]  # get str from tuple
    if len(row) > 30:  # quick and dirty way of filtering out the time rows
        itemized = json.loads(row)
        update = to_datetime(itemized["last_update"])
        if dict_data_time is None or update > dict_data_time:
            dict_data_time = update
            dict_data = itemized

items = dict_data["items"]
new_items = []

for _, item in items.items():
    if "start" in item.keys() and to_datetime(item["start"]) > TODAY:
        new_items.append(item)

new_items.sort(key=lambda x: to_datetime(x["start"]), reverse=True)
catalog = get_catalog_object()
new_formatted_items = []
name_to_hash = {}
for item in new_items:
    name = catalog[item["gem_store_item_id"]]["name"]
    name_to_hash[name] = item["gem_store_item_id"]
    start = to_datetime(item["start"]).strftime("%d %b")
    end = "N/A"
    if "end" in item.keys():
        end = to_datetime(item["end"]).strftime("%d %b")
    new_formatted_items.append((name, start, end))

print("|name|start|end|")
print("|:-|:-:|:-:|")
for item in new_formatted_items:
    print("|" + item[0] + "|" + item[1] + "|" + item[2] + "|")

print("""
&#x200B;

Images:

|name|icon|banner|
|:-|:-:|:-:|""")

url = "https://services.staticwars.com/gw2/img/content/"
large = "_large.png"
splash = "_splash.jpg"
for item in new_names:
    idy = catalog[name_to_hash[item]]["imageHash"]
    print("|" + item + "|[clicky](" + url + idy + large + ")|[clicky](" + url + idy + splash + ")|")
