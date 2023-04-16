import argparse
import img2pdf
import os
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tempfile import TemporaryDirectory


def download_images(url, download_dir):
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)

    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    image_container = soup.find('div', class_='bild_normal')
    images = image_container.find_all('img')

    for idx, image in enumerate(images):
        image_url = image['src']
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        _, ext = os.path.splitext(filename)
        img_result = requests.get(image['src'])
        dest_filename = f'{idx + 1:03d}{ext}'

        with open(os.path.join(download_dir, dest_filename), 'wb') as f:
            f.write(img_result.content)


def convert_to_pdf(download_dir, output_path):
    images = [os.path.join(download_dir, file) for file in os.listdir(download_dir)]
    images = sorted(images)
    with open(output_path, 'wb') as f:
        f.write(img2pdf.convert(images))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('output')
    args = parser.parse_args()

    tempdir = TemporaryDirectory()

    download_dir = tempdir.name
    download_images(args.url, download_dir)
    convert_to_pdf(download_dir, args.output)

    tempdir.cleanup()


if __name__ == '__main__':
    main()
