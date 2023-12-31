import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import time

def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text().strip()
    else:
        return None

main_url = "https://www.joyceproject.com/index.php?chapter=nestor&notes=1"
response = requests.get(main_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.find(id='frame')

    if body:
        links = body.find_all('a')
        links_content = []

        folder_name = "text_files_2"
        os.makedirs(folder_name, exist_ok=True)

        for link in links:
            link_text = link.get_text()
            link_url = link.get('href')
            absolute_url = urljoin(main_url, link_url)
            links_content.append((link_text, absolute_url))
            linked_page_content = scrape_page(absolute_url)
            if linked_page_content:
                print(f"Content of {link_text}: ")
                print(linked_page_content)
                print()

                # remove multiple whitespace characters
                cleaned_content = re.sub(r'\s+', ' ', linked_page_content)

                filename = re.sub(r'[^\w.-]', '_', link_text)[:200].replace('__', '_') + ".txt"
                file_path = os.path.join(folder_name, filename)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)

                # pause between requests
                time.sleep(1)

        scraped_content = body.get_text().strip()
        print("Main Page Content: ")
        print(scraped_content)

        # remove multiple whitespace characters
        cleaned_content = re.sub(r'\s+', ' ', scraped_content)

        main_content_file = os.path.join(folder_name, "main_page.txt")
        with open(main_content_file, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        print("main page content saved.")

        print("\nLinks content:")
        for link_text, link_url in links_content:
            print(f"\nContent of {link_text} (Linked page: {link_url}): ")
            linked_page_content = scrape_page(link_url)
            if linked_page_content:
                print(linked_page_content)

                # remove multiple whitespace characters
                cleaned_content = re.sub(r'\s+', ' ', linked_page_content)

                filename = re.sub(r'[^\w.-]', '_', link_text)[:200].replace('__', '_') + ".txt"
                file_path = os.path.join(folder_name, filename)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)

                # pause between requests
                time.sleep(1)

    else:
        print("no body tag found in HTML.")
else:
    print("failed to retrieve web page.")
