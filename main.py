import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time
import os
import re

BASE_URL = "https://books.toscrape.com/"

def get_soup(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def scrape_book(book_url):
    soup = get_soup(book_url)

    title = soup.find("h1").get_text(strip=True)

    table = soup.find("table", class_="table-striped")
    info = {row.find("th").get_text(strip=True): row.find("td").get_text(strip=True) 
            for row in table.find_all("tr")}

    upc = info.get("UPC", "")
    price_excl = info.get("Price (excl. tax)", "")
    price_incl = info.get("Price (incl. tax)", "")
    availability = info.get("Availability", "")
    qty_match = re.search(r"\((\d+) available\)", availability)
    quantity = qty_match.group(1) if qty_match else availability

    description = ""
    desc_div = soup.find("div", id="product_description")
    if desc_div:
        p = desc_div.find_next_sibling("p")
        description = p.get_text(strip=True) if p else ""

    category = ""
    breadcrumb = soup.find("ul", class_="breadcrumb")
    if breadcrumb:
        crumbs = breadcrumb.find_all("li")
        if len(crumbs) >= 3:
            category = crumbs[-2].get_text(strip=True)


    rating = ""
    rating_p = soup.find("p", class_=re.compile("star-rating"))
    if rating_p:
        for c in rating_p.get("class", []):
            if c != "star-rating":
                rating = c
    img_tag = soup.find("div", class_="item active").find("img")
    image_url = ""
    if img_tag and img_tag.has_attr("src"):
        image_url = urljoin(book_url, img_tag["src"])

    return {
        "product_page_url": book_url,
        "universal_product_code": upc,
        "book_title": title,
        "price_including_tax": price_incl,
        "price_excluding_tax": price_excl,
        "quantity_available": quantity,
        "product_description": description,
        "category": category,
        "review_rating": rating,
        "image_url": image_url,
    }

def download_image(image_url, save_path):
    try:
        resp = requests.get(image_url, stream=True, timeout=10)
        resp.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to download image {image_url}: {e}")

def get_all_categories():
    soup = get_soup(BASE_URL)
    side = soup.find("div", class_="side_categories")
    categories = {}
    for a in side.find_all("a"):
        name = a.get_text(strip=True)
        href = a.get("href")
        full_url = urljoin(BASE_URL, href)
        categories[name] = full_url
    return categories

def scrape_category(cat_name, cat_url):
    books = []
    next_page = cat_url
    safe_cat = re.sub(r"[^A-Za-z0-9_]", "_", cat_name)

    while next_page:
        print("Scraping", cat_name, next_page)
        soup = get_soup(next_page)
        for art in soup.find_all("article", class_="product_pod"):
            a = art.find("h3").find("a")
            href = a.get("href")
            book_url = urljoin(next_page, href)
            book_data = scrape_book(book_url)
            books.append(book_data)

            img_url = book_data["image_url"]
            if img_url:
                cat_folder = os.path.join("images", safe_cat)
                os.makedirs(cat_folder, exist_ok=True)
                img_filename = f"{book_data['universal_product_code']}.jpg"
                img_path = os.path.join(cat_folder, img_filename)
                download_image(img_url, img_path)

            time.sleep(0.5)  

        nxt = soup.find("li", class_="next")
        if nxt and nxt.find("a"):
            next_href = nxt.find("a")["href"]
            next_page = urljoin(next_page, next_href)
        else:
            next_page = None

        time.sleep(1) 
    return books

def save_books_to_csv(books, cat_name, output_folder="category_data"):
    if not books:
        return
    os.makedirs(output_folder, exist_ok=True)
    safe_name = re.sub(r"[^A-Za-z0-9_]", "_", cat_name)
    filename = os.path.join(output_folder, f"{safe_name}.csv")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        for b in books:
            writer.writerow(b)
    print(f"Saved {len(books)} books to {filename}")

def main():
    categories = get_all_categories()
    categories.pop("Books", None)
    for name, url in categories.items():
        books = scrape_category(name, url)
        save_books_to_csv(books, name)

if __name__ == "__main__":
    main()
