import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin

# Set up headers to mimic a browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Configure scraper
MAX_PAGES = 3  # For demo purposes - increase for more data
DELAY = 2  # Seconds between requests to be polite

def scrape_ai_data():
    sources = [
        {
            'name': 'Towards Data Science',
            'url': 'https://towardsdatascience.com/',
            'selectors': {
                'article_links': 'div.postArticle a[href*="/towards-data-science/"]',
                'content': 'article section',
                'title': 'h1'
            },
            'type': 'articles'
        },
        {
            'name': 'arXiv CS',
            'url': 'https://arxiv.org/list/cs/recent',
            'selectors': {
                'article_links': 'dt a[href^="/abs/"]',
                'content': 'div.abstract',
                'title': 'h1.title'
            },
            'type': 'research'
        },
        {
            'name': 'PyTorch Docs',
            'url': 'https://pytorch.org/docs/stable/',
            'selectors': {
                'article_links': 'a.reference.internal',
                'content': 'section',
                'title': 'h1'
            },
            'type': 'documentation'
        },
        {
            'name': 'freeCodeCamp',
            'url': 'https://www.freecodecamp.org/news/tag/artificial-intelligence/',
            'selectors': {
                'article_links': 'a.post-card-image-link',
                'content': 'div.post-content',
                'title': 'h1'
            },
            'type': 'tutorials'
        },
        {
            'name': 'GeeksforGeeks',
            'url': 'https://www.geeksforgeeks.org/machine-learning/',
            'selectors': {
                'article_links': 'a[href*="/machine-learning/"]',
                'content': 'div.article--container_content',
                'title': 'h1'
            },
            'type': 'educational'
        }
    ]
    
    all_data = []
    
    for source in sources:
        print(f"\nScraping {source['name']}...")
        
        # Get list of article URLs
        article_urls = []
        try:
            # For paginated sources
            if source['name'] in ['Towards Data Science', 'freeCodeCamp']:
                for page in range(1, MAX_PAGES + 1):
                    page_url = f"{source['url']}archive?page={page}" if source['name'] == 'Towards Data Science' else f"{source['url']}page/{page}/"
                    
                    response = requests.get(page_url, headers=HEADERS)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    links = soup.select(source['selectors']['article_links'])
                    for link in links:
                        href = link.get('href')
                        if href:
                            full_url = urljoin(source['url'], href)
                            if full_url not in article_urls:
                                article_urls.append(full_url)
                    
                    time.sleep(DELAY + random.random())
            else:
                response = requests.get(source['url'], headers=HEADERS)
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.select(source['selectors']['article_links'])
                article_urls.extend([urljoin(source['url'], link.get('href')) for link in links])
                
        except Exception as e:
            print(f"Error getting article list from {source['name']}: {e}")
            continue
        
        # Scrape individual articles
        for url in article_urls[:10]:  # Limit to 10 articles per source for demo
            try:
                response = requests.get(url, headers=HEADERS)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get title
                title_elem = soup.select_one(source['selectors']['title'])
                title = title_elem.get_text(strip=True) if title_elem else "No title"
                
                # Get content
                content_elem = soup.select_one(source['selectors']['content'])
                if not content_elem:
                    continue
                    
                # Clean content
                for element in content_elem(['script', 'style', 'nav', 'footer', 'aside']):
                    element.decompose()
                    
                content = ' '.join(content_elem.stripped_strings)
                
                if len(content) < 500:  # Skip short articles
                    continue
                
                all_data.append({
                    'title': title,
                    'content': content,
                    'url': url,
                    'source': source['name'],
                    'type': source['type']
                })
                
                print(f"  Collected: {title[:50]}...")
                time.sleep(DELAY + random.random())
                
            except Exception as e:
                print(f"Error scraping article {url}: {e}")
                continue
    
# ... (keep all your existing code until the saving part)

    # Save to TXT file
    with open('ai_ml_data.txt', 'w', encoding='utf-8') as f:
        for item in all_data:
            f.write(f"Title: {item['title']}\n")
            f.write(f"Source: {item['source']} ({item['type']})\n")
            f.write(f"URL: {item['url']}\n")
            f.write(f"Content:\n{item['content']}\n")
            f.write("\n" + "="*80 + "\n\n")  # separator between articles
    
    print(f"\nFinished scraping. Collected {len(all_data)} articles.")
    return all_data

# Run the scraper
data = scrape_ai_data()
    
