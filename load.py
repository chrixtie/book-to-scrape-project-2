import csv
import os

def save_to_csv(category, book_data):
    os.makedirs("output/csv", exist_ok=True)
    file_path = f"output/csv/{category}.csv"

    file_exists = os.path.isfile(file_path)

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=book_data.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(book_data)
