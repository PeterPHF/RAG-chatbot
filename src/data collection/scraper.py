import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import random
import json
from tqdm import tqdm  # For progress bar

def crawl_entire_website(start_url, max_pages=100, delay=(1, 3)):
    """
    Crawl an entire website collecting all content
    :param start_url: Starting URL (e.g., 'https://www.geeksforgeeks.org')
    :param max_pages: Maximum pages to crawl
    :param delay: Tuple of (min_delay, max_delay) in seconds
    :return: List of dictionaries with URL and content
    """
    visited = set()
    to_visit = {start_url}
    collected_pages = []
    base_domain = start_url.split('/')[2]  # Extract 'www.geeksforgeeks.org'
    
    # Initialize progress bar
    pbar = tqdm(total=max_pages, desc="Crawling pages")
    
    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop()
        
        try:
            # Respect crawl delay with random interval
            time.sleep(random.uniform(*delay))
            
            # Fetch page with timeout
            response = requests.get(
                current_url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            
            # Skip if not successful
            if response.status_code != 200:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract all text content (more comprehensive than just p and article)
            text_content = ' '.join([
                element.get_text(strip=True) 
                for element in soup.find_all(['p', 'article', 'section', 'div'])
            ])
            
            collected_pages.append({
                'url': current_url,
                'title': soup.title.string if soup.title else 'No title',
                'content': text_content
            })
            
            # Update progress bar
            pbar.update(1)
            pbar.set_postfix({'Found': len(collected_pages), 'Queued': len(to_visit)})
            
            # Find new links to visit
            for link in soup.find_all('a', href=True):
                href = link['href']
                
                # Skip these URL types
                if any(href.startswith(s) for s in ['mailto:', 'tel:', 'javascript:']):
                    continue
                    
                absolute_url = urljoin(current_url, href)
                
                # Only follow links within the same domain
                if (absolute_url.split('/')[2] == base_domain and
                    absolute_url not in visited and
                    absolute_url not in to_visit and
                    '#' not in absolute_url.split('#')[0]):
                    
                    to_visit.add(absolute_url)
            
            visited.add(current_url)
            
        except Exception as e:
            tqdm.write(f"Error crawling {current_url}: {str(e)}")
            continue
    
    pbar.close()
    return collected_pages

# Example usage
all_geeksforgeeks_pages = crawl_entire_website(
    start_url='https://www.geeksforgeeks.org/',
    max_pages=200,  # Increase for more comprehensive crawling
    delay=(1, 3)    # Random delay between 1-3 seconds
)

print(f"\nFinished crawling. Collected {len(all_geeksforgeeks_pages)} pages.")

# Save data to a file 
with open('.../../data/raw/gfg_technical_corpus.json', 'w', encoding='utf-8') as f:
    json.dump(all_geeksforgeeks_pages, f, indent=2, ensure_ascii=False)

print("Sample pages:")
for page in all_geeksforgeeks_pages:
    print(f"- {page['title']} ({page['url']}) ")