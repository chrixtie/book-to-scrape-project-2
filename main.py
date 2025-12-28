# book_scraper.py
import requests
from bs4 import BeautifulSoup
import csv

def scrape_book_data(url):
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract book information
        product_page_url = url
        book_title = soup.find('div', class_='product_main').h1.text.strip()
        upc = soup.find('th', text='UPC').find_next_sibling('td').text.strip()
        price_including_tax = soup.find('th', text='Price (incl. tax)').find_next_sibling('td').text.strip()
        price_excluding_tax = soup.find('th', text='Price (excl. tax)').find_next_sibling('td').text.strip()
        availability_text = soup.find('th', text='Availability').find_next_sibling('td').text.strip()
        quantity_available = ''.join([c for c in availability_text if c.isdigit()]) or "0"

        # Description
        description_tag = soup.find('div', id='product_description')
        if description_tag:
            product_description = description_tag.find_next('p').text.strip()
        else:
            product_description = "No description available."

        # Category
        category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text.strip()

        # Review rating
        rating_tag = soup.find('p', class_='star-rating')
        review_rating = rating_tag['class'][1] if rating_tag else "No rating"

        # Image URL (make absolute)
        image_url = soup.find('div', class_='item active').img['src']
        image_url = "https://books.toscrape.com/" + image_url.replace('../', '')

        # Return all data as a dictionary
        return {
            "product_page_url": product_page_url,
            "universal_product_code": upc,
            "book_title": book_title,
            "price_including_tax": price_including_tax,
            "price_excluding_tax": price_excluding_tax,
            "quantity_available": quantity_available,
            "product_description": product_description,
            "category": category,
            "review_rating": review_rating,
            "image_url": image_url
        }

    except Exception as e:
        print(f"❌ Error scraping book: {e}")
        return None


def save_to_csv(data, filename="book_data.csv"):
    """Write the scraped data to a CSV file."""
    if not data:
        print("⚠️ No data to save.")
        return

    fieldnames = [
        "product_page_url", "universal_product_code", "book_title",
        "price_including_tax", "price_excluding_tax", "quantity_available",
        "product_description", "category", "review_rating", "image_url"
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)


if __name__ == "__main__":
    # Example single book URL from Books to Scrape
    book_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    print("🔍 Scraping book data...")

    book_data = scrape_book_data(book_url)
    save_to_csv(book_data)

 
