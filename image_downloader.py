import os
import requests

def download_image(image_url, category, filename):
    folder_path = os.path.join("images", category)
    os.makedirs(folder_path, exist_ok=True)

    image_path = os.path.join(folder_path, filename)

    response = requests.get(image_url)
    with open(image_path, "wb") as file:
        file.write(response.content)

    return image_path
