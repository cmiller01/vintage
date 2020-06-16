import requests
from bs4 import BeautifulSoup
import uuid
import os.path
import time

BRANDS = [
    "Sansui",
    "Pioneer",
    "Marantz",
    "Sony",
    "Yamaha",
    "Fisher",
    "Kenwood",
    "Technics",
    "Yamaha",
]


def get_receiver_url(brand):
    return f"https://www.hifiengine.com/database/hifi_database.php?model_type=rec&make={brand}"


def save_text(text, brand, directory):
    fname = os.path.join(directory, brand + "-" + str(uuid.uuid4()) + ".html")
    with open(fname, "w") as f:
        f.write(text)


def get_next_url(text):
    soup = BeautifulSoup(text,"html.parser")
    links = soup.find("div", "center").find_all("a")
    for l in links:
        if l.text == "Next page ››":
            return "https://www.hifiengine.com" + l['href']
    return None


def get_receivers(brand, directory):
    url = get_receiver_url(brand)
    count = 0
    while url:
        if count > 15:
            raise Exception("oops too many requests")
        print(f"getting {url}")
        data = requests.get(url)
        if data.ok:
            print(f"saving data")
            save_text(data.text, brand, directory)
            url = get_next_url(data.text)
            print(f"getting next url {url}")
            time.sleep(2.5)
            count += 1


if __name__ == "__main__":
    for brand in BRANDS:
        get_receivers(brand, "./data/specs")
