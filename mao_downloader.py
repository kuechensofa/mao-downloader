import argparse
import os
import requests
import subprocess

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tempfile import TemporaryDirectory
from PIL import Image
from math import floor


PAPER_WIDTHS = {
    'a3': 16.54,
    'a4': 11.69,
    'a5': 8.268,
    'a6': 5.827
}


def download_images(url, download_dir):
    if not os.path.isdir(download_dir):
        os.mkdir(download_dir)

    result = requests.get(url)
    soup = BeautifulSoup(result.content, 'html.parser')
    image_container = soup.find('div', class_='bild_normal')
    images = image_container.find_all('img')

    for image in images:
        image_url = image['src']
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        img_result = requests.get(image['src'])

        with open(os.path.join(download_dir, filename), 'wb') as f:
            f.write(img_result.content)


def get_dpi(download_dir, paper_format):
    max_width = 0

    for file in os.listdir(download_dir):
        image = Image.open(os.path.join(download_dir, file))
        width, height = image.size
        longest_side = max(width, height)

        if longest_side > max_width:
            max_width = longest_side

    dpi = max_width / PAPER_WIDTHS[paper_format]
    return dpi


def convert_to_pnm(download_dir, pnm_dir):
    if not os.path.isdir(pnm_dir):
        os.mkdir(pnm_dir)

    for file in os.listdir(download_dir):
        name, ext = os.path.splitext(file)
        pnm_name = name + '.pnm'
        subprocess.run(['convert', os.path.join(download_dir, file), os.path.join(pnm_dir, pnm_name)])


def convert_to_pdf(pnm_dir, output_path, dpi=300.0):
    subprocess.run(['convert', '-density', str(floor(dpi)), os.path.join(pnm_dir, '*.pnm'), output_path])


def compress_pdf(original_pdf, compressed_pdf):
    subprocess.run(['gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4', '-dPDFSETTINGS=/ebook',
                    '-dNOPAUSE', '-dQUIET', '-dBATCH', f'-sOutputFile={compressed_pdf}', original_pdf])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('output')
    parser.add_argument('--format', choices=['a3', 'a4', 'a5', 'a6'], default='a4')
    args = parser.parse_args()

    tempdir = TemporaryDirectory()

    download_dir = os.path.join(tempdir.name, 'download')
    download_images(args.url, download_dir)

    image_dpi = get_dpi(download_dir, args.format)

    pnm_dir = os.path.join(tempdir.name, 'pnm')
    convert_to_pnm(download_dir, pnm_dir)

    temp_pdf_path = os.path.join(tempdir.name, 'download.pdf')
    convert_to_pdf(pnm_dir, temp_pdf_path, image_dpi)
    compress_pdf(temp_pdf_path, args.output)

    tempdir.cleanup()


if __name__ == '__main__':
    main()
