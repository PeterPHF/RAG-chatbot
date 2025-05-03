import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import os
import json
from tqdm import tqdm

def crawl_website(start_url, max_pages=100, delay=(1, 3), output_json='data/raw/gfg_raw.json'):
    visited = set()
    to_visit = {start_url}
    base_domain = start_url.split('/')[2]
    collected_pages = []

    pbar = tqdm(total=max_pages, desc="Crawling raw pages")

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop()

        try:
            time.sleep(random.uniform(*delay))
            response = requests.get(current_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            main_content = (
                soup.find('article') or
                soup.find('div', class_='text') or
                soup.find('div', class_='content') or
                soup.find('div', class_='entry-content') or
                soup.find('div', {'id': 'main'}) or
                soup.find('div')
            )

            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                collected_pages.append({
                    'url': current_url,
                    'title': soup.title.string if soup.title else '',
                    'content': text
                })

            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(href.startswith(s) for s in ['mailto:', 'tel:', 'javascript:']):
                    continue
                absolute_url = urljoin(current_url, href)
                if (absolute_url.split('/')[2] == base_domain and
                    absolute_url not in visited and
                    absolute_url not in to_visit and
                    '#' not in absolute_url):
                    to_visit.add(absolute_url)

            visited.add(current_url)
            pbar.update(1)

        except Exception as e:
            tqdm.write(f"Error at {current_url}: {e}")
            continue

    pbar.close()

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(collected_pages, f, indent=2, ensure_ascii=False)

    print(f" Saved {len(collected_pages)} raw pages to {output_json}")

if __name__ == "__main__":
    crawl_website(
        start_url='https://www.geeksforgeeks.org/python-programming-language/',
        max_pages=200,
        delay=(1, 3),
        output_json='../../data/raw/gfg_raw.json'
    )
