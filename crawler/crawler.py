import requests
from bs4 import BeautifulSoup
import time
import json
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin, urlparse

USER_AGENT = "ChickenJockeyBot"
SEED_URL = "https://minecraft.fandom.com/wiki/Crafting"
DOMAIN = "minecraft.fandom.com"
MAX_PAGES = 500
OUTPUT_DIR = "data"
DELAY = 1
OUTPUT_FILE = "collection.json"


def setup_crawler():
    """Initializes RobotFileParser"""
    print("Setting up the crawler...")
    rp = RobotFileParser()
    robots_url = f"https://{DOMAIN}/robots.txt"
    print(f"reading robots.txt: {robots_url}")
    rp.set_url(robots_url)
    rp.read()
    return rp


def is_valid_to_crawl(soup):
    """Checks if a page should be crawled based on language & tags"""
    html_tag = soup.find('html')
    if not html_tag or not html_tag.get('lang', '').lower().startswith('en'):
        print(" SKIPPING: Not an english page")
        return False
    tag_robots = soup.find('meta', attrs={'name': 'robots'})
    if tag_robots and 'noindex' in tag_robots.get('content', '').lower():
        print(" SKIPPING: Page contains 'noindex' meta tag")
        return False
    return True


def crawl():
    """Main crawling function"""
    robot_parser = setup_crawler()
    
    url_queue = [SEED_URL]
    visited = set()
    collection_data = []
    pages_crawled = 0

    print("\n--- Starting crawl ---\n")

    while url_queue and pages_crawled < MAX_PAGES:
        current_url = url_queue.pop(0)

        if current_url in visited:
            continue

        if not robot_parser.can_fetch(USER_AGENT, current_url):
            print(f"DISALLOWED by robots.txt: {current_url}")
            visited.add(current_url)
            continue
            
        visited.add(current_url)
        print(f"[{pages_crawled + 1}/{MAX_PAGES}] visiting: {current_url}")
        
        time.sleep(DELAY)

        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(current_url, headers=headers, timeout=10)

            if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                print(f" SKIPPING: non-HTML / bad status code ({response.status_code})")
                continue

            soup = BeautifulSoup(response.content, 'lxml')

            if not is_valid_to_crawl(soup):
                continue
                
            pages_crawled += 1
            text_content = soup.get_text(separator=' ', strip=True)
            
            links = set()
            
            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                new_url = urljoin(current_url, href)
                new_url = urlparse(new_url)._replace(fragment="").geturl()

                parsed_url = urlparse(new_url)

                if (parsed_url.netloc == DOMAIN and parsed_url.path.startswith('/wiki/')) and not parsed_url.path.startswith('/wiki/File:'):

                    links.add(new_url)
                    
                    if new_url not in visited and new_url not in url_queue:
                        url_queue.append(new_url)
            
            page_data = {
                "id": pages_crawled,
                "url": current_url,
                "content": text_content,
                "links": list(links)
            }
            
            collection_data.append(page_data)
            print(f" SUCCESS: added to collection (ID: {pages_crawled}), found {len(links)} links")

        except requests.RequestException as e:
            print(f" ERROR: could not fetch {current_url}. reason: {e}")
        except Exception as e:
            print(f" ERROR: {e}")

    with open(f'{OUTPUT_DIR}/{OUTPUT_FILE}', 'w', encoding='utf-8') as f:
        json.dump(collection_data, f, indent=2, ensure_ascii=False)

    print(f"\n--- Crawl finished ---")
    print(f"# of pages downloaded: {pages_crawled}")
    print(f"data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    crawl()
    