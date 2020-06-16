import bs4
import requests
import vintage.models as models
import re
import datetime as dt
import time
from decimal import Decimal
import csv


def process_product(tag: bs4.element.Tag) -> models.GoodwillItem:
    try:
        title_str = tag.find("div", "title").text
        title_str = title_str.split("Bids: ")
        bids = 0
        if len(title_str) > 1:
            bids = int(title_str[1].strip())
        title = title_str[0].strip()
        item_number = tag.find("div", "product-number").contents[1]
        price_str = tag.find("div", "price").text.replace("Buy It Now", "").strip()
        price = Decimal(re.sub(r"[^\d.]", "", price_str))
        end_date_str = tag.find("div", "timer countdown product-countdown").get(
            "data-countdown"
        )
        end_date = dt.datetime.strptime(end_date_str, "%m/%d/%Y %I:%M:%S %p")
        return models.GoodwillItem(
            title=title,
            item_number=item_number,
            price=price,
            end_date=end_date,
            bids=bids,
        )
    except Exception as e:
        print(f"could not create GoodwillItem due to {e} for tag {tag}")
        return None


def get_receiver_url(page: int, days=30) -> str:
    return f"https://www.shopgoodwill.com/Listings?t=&sg=&c=401&s=&lp=0&hp=999999&sbn=False&spo=False&snpo=False&socs=False&sd=False&sca=True&cadb={days}&scs=False&sis=False&col=4&p={page}&ps=40&desc=true&ss=0&UseBuyerPrefs=true"


def get_receivers(days=30):
    items = []
    page = 1
    while True:
        print(f"length items {len(items)}, page {page}\n")
        response = requests.get(get_receiver_url(page))
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("span", "data-container")
        if not products:
            break
        items += list(map(process_product, products))
        page += 1
        time.sleep(2)
    return items


def write_receivers(items, filename='receivers.csv'):
    with open(filename, "w") as csvfile:
        fieldnames = ["title", "item_number", "price", "end_date", "bids"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in items:
            if i:
                writer.writerow(i.__dict__)
