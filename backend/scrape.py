import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
from typing import List, Set, Optional
from tools import TOOLS, ToolConfig, get_tool_config, get_enabled_tools

class UniversalScraper:
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def scrape_tool(self, tool_name: str) -> List[str]:
        """Scrape documentation for a specific tool"""
        config = get_tool_config(tool_name)
        if not config:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        if not config.enabled:
            print(f"Tool {tool_name} is disabled")
            return []

        print(f"Scraping {config.name} documentation...")
        chunks = []
        visited = set()

        for path in config.scrape_paths:
            url = urljoin(config.base_url, path)
            if url in visited:
                continue
            
            try:
                content = self._scrape_page(url, config)
                if content:
                    chunks.extend(content)
                visited.add(url)
                time.sleep(config.delay)
                
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
                continue

        print(f"Scraped {len(chunks)} chunks from {config.name}")
        return chunks

    def scrape_all_tools(self) -> List[str]:
        """Scrape all enabled tools and return a flat list of chunks"""
        all_chunks = []
        
        for tool_name, config in get_enabled_tools().items():
            try:
                chunks = self.scrape_tool(tool_name)
                all_chunks.extend(chunks)
            except Exception as e:
                print(f"Failed to scrape {tool_name}: {str(e)}")
                continue
        
        return all_chunks

    def scrape_all_tools_dict(self) -> dict:
        """Scrape all enabled tools and return organized chunks by tool"""
        all_chunks = {}
        
        for tool_name, config in get_enabled_tools().items():
            try:
                chunks = self.scrape_tool(tool_name)
                all_chunks[tool_name] = chunks
            except Exception as e:
                print(f"Failed to scrape {tool_name}: {str(e)}")
                all_chunks[tool_name] = []
        
        return all_chunks

    def _scrape_page(self, url: str, config: ToolConfig) -> List[str]:
        """Scrape a single page based on tool configuration"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # remove excluded elements
            if 'exclude' in config.selectors:
                for element in soup.select(config.selectors['exclude']):
                    element.decompose()
            
            # extract content
            content_elements = soup.select(config.selectors['content'])
            if not content_elements:
                # fallback to common content selectors
                content_elements = soup.select('article, main, .content, .documentation')
            
            chunks = []
            for element in content_elements:
                # get title if available
                title_elem = element.select_one(config.selectors.get('title', 'h1, h2, h3'))
                title = title_elem.get_text().strip() if title_elem else ""
                
                # get text content
                text = element.get_text().strip()
                if text and len(text) > 100:  # only include substantial content
                    # add source information
                    chunk = f"Source: {config.name} - {title}\nURL: {url}\n\n{text}"
                    chunks.append(chunk)
            
            return chunks
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return []

    def _chunk_text(self, text: str, max_chunk_size: int = 1500) -> List[str]:
        """Split long text into smaller chunks"""
        if len(text) <= max_chunk_size:
            return [text]
        
        # split on paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk + para) <= max_chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

# Legacy functions for backward compatibility
def scrape_stripe_docs():
    """Legacy function - scrape only Stripe docs"""
    scraper = UniversalScraper()
    return scraper.scrape_tool("stripe")

def scrape_all_docs():
    """Scrape all enabled documentation - returns flat list"""
    scraper = UniversalScraper()
    return scraper.scrape_all_tools()  # Now returns a flat list

# Individual tool functions for backward compatibility (if needed)
def scrape_tailwind_docs():
    """Scrape only Tailwind docs"""
    scraper = UniversalScraper()
    return scraper.scrape_tool("tailwind")

def scrape_react_docs():
    """Scrape only React docs"""
    scraper = UniversalScraper()
    return scraper.scrape_tool("react")

def scrape_vercel_docs():
    """Scrape only Vercel docs"""
    scraper = UniversalScraper()
    return scraper.scrape_tool("vercel")

def scrape_nextjs_docs():
    """Scrape only Next.js docs"""
    scraper = UniversalScraper()
    return scraper.scrape_tool("nextjs")