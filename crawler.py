import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Set, Dict, List
import re

class Crawler:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.visited_urls: Set[str] = set()
        self.pages: Dict[str, dict] = {}
        
    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the same domain and is HTML."""
        parsed = urlparse(url)
        return (parsed.netloc == self.base_domain and
                not url.endswith(('.pdf', '.jpg', '.png', '.gif')))
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text by removing extra whitespace."""
        return ' '.join(text.split())
    
    def extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """Extract and normalize all links from the page."""
        links = []
        for link in soup.find_all('a', href=True):
            url = urljoin(current_url, link['href'])
            if self.is_valid_url(url):
                links.append(url)
        return links
    
    def crawl_page(self, url: str) -> None:
        """Crawl a single page and extract its content."""
        if url in self.visited_urls:
            return
        
        try:
            print(f"\nCrawling: {url}")  # Debug print
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                print(f"Failed to fetch {url}: Status code {response.status_code}")
                return
            
            self.visited_urls.add(url)
            
            if 'text/html' not in response.headers.get('Content-Type', ''):
                print(f"Skipping non-HTML content: {url}")
                return
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract page content
            title = soup.title.string if soup.title else ''
            text = self.clean_text(soup.get_text())
            
            # Debug prints
            print(f"Title: {title}")
            print(f"Text length: {len(text)} characters")
            print(f"First 100 chars: {text[:100]}...")
            
            # Store page data
            self.pages[url] = {
                'title': title,
                'text': text,
                'links': self.extract_links(soup, url)
            }
            
            # Debug print
            print(f"Found {len(self.pages[url]['links'])} links")
            
            # Recursively crawl linked pages
            for link in self.pages[url]['links']:
                self.crawl_page(link)
                
        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
    
    def crawl(self) -> Dict[str, dict]:
        """Start crawling from the start URL."""
        self.crawl_page(self.start_url)
        return self.pages

# Test the crawler
if __name__ == "__main__":
    TEST_URL = "https://vm009.rz.uos.de/crawl/index.html"
    crawler = Crawler(TEST_URL)
    pages = crawler.crawl()
    
    print(f"Crawled {len(pages)} pages:")
    for url, data in pages.items():
        print(f"\nURL: {url}")
        print(f"Title: {data['title']}")
        print(f"Text length: {len(data['text'])} characters")
        print(f"Links: {len(data['links'])} found") 