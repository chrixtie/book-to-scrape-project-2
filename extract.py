import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

def get_category_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    categories = {}
    for link in soup.select(".side_categories ul li ul li a"):
        name = link.text.strip().lower().replace(" ", "-")
        url = urljoin(BASE_URL, link["href"])
        categories[name] = url

    return categories


def get_book_links(category_url):
    book_links = []

    while category_url:
        response = requests.get(category_url)
        soup = BeautifulSoup(response.content, "html.parser")

        for book in soup.select("h3 a"):
            book_links.append(urljoin(category_url, book["href"]))

        next_button = soup.select_one("li.next a")
        category_url = urljoin(category_url, next_button["href"]) if next_button else None

    return book_links


def extract_book_data(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.find("h1").text.strip()
    upc = soup.find("th", string="UPC").find_next_sibling("td").text.strip()
    image_url = urljoin(book_url, soup.find("img")["src"])
    category = soup.select("ul.breadcrumb li a")[2].text.strip().lower().replace(" ", "-")

    return {
        "title": title,
        "upc": upc,
        "image_url": image_url,
        "category": category,
        "product_page_url": book_url
    }
