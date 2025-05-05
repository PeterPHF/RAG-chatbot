import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import os
import json
from tqdm import tqdm

def crawl_topic(start_url, topics, max_pages=100, delay=(1, 3), output_json='data/raw/gfg_topic_raw.json'):
    """
    Crawl a website but only collect pages that match specific topics
    
    Args:
        start_url: Starting URL for crawling
        topics: List of topics to look for in page content
        max_pages: Maximum number of pages to crawl
        delay: Range of delay between requests in seconds
        output_json: Path to save the collected data
    """
    visited = set()
    to_visit = {start_url}
    base_domain = start_url.split('/')[2]
    collected_pages = []
    
    # Convert topics to lowercase for case-insensitive matching
    topics_lower = [topic.lower() for topic in topics]
    
    pbar = tqdm(total=max_pages, desc="Crawling topic-specific pages")

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop()

        try:
            time.sleep(random.uniform(*delay))
            response = requests.get(current_url, 
                                 headers={'User-Agent': 'Mozilla/5.0'}, 
                                 timeout=10)

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Try different selectors for main content
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
                text_lower = text.lower()
                
                # Check if page content contains any of our target topics
                if any(topic in text_lower for topic in topics_lower):
                    collected_pages.append({
                        'url': current_url,
                        'title': soup.title.string if soup.title else '',
                        'content': text,
                        'matched_topics': [topic for topic in topics if topic.lower() in text_lower]
                    })

            # Find links to follow - modified to prioritize topic-relevant links
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Skip non-http links
                if any(href.startswith(s) for s in ['mailto:', 'tel:', 'javascript:']):
                    continue
                
                # Check if link text suggests it's about our topics
                link_text = link.get_text().lower()
                topic_relevant = any(topic in link_text for topic in topics_lower)
                
                absolute_url = urljoin(current_url, href)
                
                if (absolute_url.split('/')[2] == base_domain and
                    absolute_url not in visited and
                    absolute_url not in to_visit and
                    '#' not in absolute_url):
                    
                    # Prioritize topic-relevant links by adding them first
                    if topic_relevant:
                        to_visit.add(absolute_url)
                    else:
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

    print(f"\nSaved {len(collected_pages)} pages about target topics to {output_json}")
    if collected_pages:
        print("Topics found:")
        for page in collected_pages[:5]:  # Show first 5 as sample
            print(f"- {page['url']} (Topics: {', '.join(page['matched_topics'])})")

if __name__ == "__main__":
    # Define your target topics
    TARGET_TOPICS = [
        "machine learning",
        "deep learning",
        "neural network",
        "natural language processing",
        "computer vision",
        "reinforcement learning",
        "data science",
        "artificial intelligence",
        "AI"
    ]
    
    crawl_topic(
        start_url='https://www.geeksforgeeks.org/machine-learning/',
        topics=TARGET_TOPICS,
        max_pages=200,
        delay=(1, 3),
        output_json='data/raw/gfg_ai_raw.json'
    )