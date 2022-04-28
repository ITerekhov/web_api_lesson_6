import random
from pathlib import Path

import requests


images_dir = 'media/'
Path(images_dir).mkdir(parents=True, exist_ok=True)


def download_image(image_url, download_path, params=None):
    response = requests.get(image_url, params=params)
    response.raise_for_status()
    with open(str(download_path), 'wb') as file:
        file.write(response.content)


def fetch_comics_by_id(id):
    url = f'https://xkcd.com/{id}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    comics_info = response.json()
    img_url = comics_info['img']
    img_path = Path(f"{images_dir}/{comics_info['title']}.png")
    download_image(img_url, img_path)
    return img_path, comics_info['alt']


def fetch_random_comics():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_comics_num = response.json()['num']
    comics_id = random.randint(1, last_comics_num)
    return fetch_comics_by_id(comics_id)
