from extract import get_category_links, get_book_links, extract_book_data
from transform import sanitize_title
from image_downloader import download_image
from load import save_to_csv

def main():
    categories = get_category_links()

    for category, category_url in categories.items():
        print(f"Processing category: {category}")

        book_links = get_book_links(category_url)

        for book_url in book_links:
            extracted = extract_book_data(book_url)

            sanitized_title = sanitize_title(extracted["title"])
            image_filename = f"{extracted['upc']}_{sanitized_title}.jpg"

            image_path = download_image(
                extracted["image_url"],
                extracted["category"],
                image_filename
            )

            book_record = {
                "product_page_url": extracted["product_page_url"],
                "upc": extracted["upc"],
                "title": extracted["title"],
                "category": extracted["category"],
                "image_path": image_path
            }

            save_to_csv(extracted["category"], book_record)

if __name__ == "__main__":
    main()
