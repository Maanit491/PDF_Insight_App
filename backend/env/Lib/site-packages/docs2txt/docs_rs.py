"""Main module."""

from pathlib import Path

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from tqdm import tqdm

console = Console()


def extract_items(base_url):
    # Get the HTML content of the page
    with console.status("Loading Modules from Docs...", spinner="aesthetic"):
        response = requests.get(base_url)

        # If request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the section with id "main-content"
            section = soup.find(id="main-content")

            # Create an empty dictionary to hold the data
            data = {}

            h2s = section.find_all("h2")
            # Iterate over the h2 elements in the section
            for h2 in h2s:
                # Get the name of the category (structs, enums, etc.)
                category = h2.get_text().lower()
                data[category] = {}

                # Get the ul that immediately follows the h2
                ul = h2.find_next_sibling('ul')

                # Iterate over the li elements in the ul
                for li in ul.find_all('li'):
                    # Get the <a> element in the li
                    a = li.find('a')

                    # Get the name and href of the item
                    name = a.get_text()
                    href = a.get('href')

                    # Add the item to the data dictionary
                    data[category][name] = href

            return data

        else:
            raise requests.exceptions.RequestException(
                f"Unable to reach the website. HTTP status code: {response.status_code}")


def extract_text_from_page(base_url, href):
    # Get the HTML content of the page
    page_url = base_url + href
    response = requests.get(page_url)

    # If request was successful
    if response.status_code == 200:

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the section with id "main-content"
        section = soup.find(id="main-content")

        if section:
            # Extract the text
            text = section.get_text()
            return text

        else:
            return "Section with id 'main-content' was not found."

    else:
        return f"Unable to reach the website. HTTP status code: {response.status_code}"


def loop_through_items(base_url, data):
    master_text = ""
    for category, items in data.items():
        for name, href in tqdm(items.items(), desc=f"Extracting {category}"):
            text = extract_text_from_page(base_url, href)
            master_text += f'{text}\n\n'
    master_text = master_text[:-4]
    return master_text


def get_crate_name(base_url):
    split_url = base_url.split("/")
    crate_name = split_url[3]
    return crate_name


def write_to_file(base_url, master_text, output_dir: Path):
    crate_name = get_crate_name(base_url)
    save_path = output_dir / f"{crate_name}.txt"
    save_path.write_text(master_text, encoding="utf-8")
    return save_path


def main(base_url, output_dir: Path) -> Path:
    data = extract_items(base_url)
    master_text = loop_through_items(base_url, data)
    save_path = write_to_file(base_url, master_text, output_dir)
    return save_path


if __name__ == '__main__':
    main(base_url="https://docs.rs/redb/1.0.4/redb/", output_dir=Path("~/docs2txt/"))
