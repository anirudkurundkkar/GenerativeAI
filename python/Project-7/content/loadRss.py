import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

RSS_FEED_URL = "https://www.w3schools.com/xml/xml_rss.asp"

def fetch_rss_xml(rss_url):
    resp = requests.get(rss_url)
    resp.raise_for_status()
    # The W3Schools RSS demo page contains the RSS XML within the page as a code block.
    # We'll extract the XML between <rss>...</rss>
    start = resp.text.find('<rss')
    end = resp.text.find('</rss>') + len('</rss>')
    if start == -1 or end == -1:
        raise Exception("RSS XML not found in the page.")
    return resp.text[start:end]

def fetch_rss_links(xml_content):
    root = ET.fromstring(xml_content)
    # Find all <item><link>
    links = []
    for item in root.iter('item'):
        link = item.find('link')
        if link is not None:
            links.append(link.text)
    return links

def fetch_content(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        print(f"\nURL: {url}\nContent:\n{r.text[:500]}...\n")  # Print first 500 chars for brevity
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

def main():
    xml_content = fetch_rss_xml(RSS_FEED_URL)
    links = fetch_rss_links(xml_content)
    print(f"Found {len(links)} links in RSS feed.")
    if not links:
        return
    with ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(fetch_content, links)

if __name__ == "__main__":
    main()