import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching website content: {e}")
        return None


def parse_content(html):
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='post-link')

    feed_items = []
    for article in articles:
        title_tag = article.find('a', class_='title')
        summary_tag = article.find('div', class_='summary')

        if not title_tag or not summary_tag:
            continue  # Skip if any required tag is missing

        title = title_tag.text.strip()
        link = title_tag['href']
        description = summary_tag.text.strip()
        pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")  # Use the current date and time

        feed_items.append({
            'title': title,
            'link': link,
            'description': description,
            'pub_date': pub_date
        })
    return feed_items


def generate_rss_feed(items):
    rss_feed = '<?xml version="1.0" encoding="UTF-8" ?>'
    rss_feed += '<rss version="2.0"><channel>'
    rss_feed += '<title>AnonBlogs</title>'
    rss_feed += '<link>http://www.anonblogs.net</link>'
    rss_feed += '<description>Anonymous Blogs Feed</description>'
    for item in items:
        rss_feed += '<item>'
        rss_feed += f'<title>{item["title"]}</title>'
        rss_feed += f'<link>{item["link"]}</link>'
        rss_feed += f'<description>{item["description"]}</description>'
        rss_feed += f'<pubDate>{item["pub_date"]}</pubDate>'
        rss_feed += '</item>'
    rss_feed += '</channel></rss>'
    return rss_feed


def save_rss_feed(feed, file_path):
    with open(file_path, 'w') as file:
        file.write(feed)


if __name__ == "__main__":
    url = 'https://anonblogs.net/recent'
    html_content = fetch_website_content(url)
    if html_content:
        items = parse_content(html_content)
        rss_feed = generate_rss_feed(items)
        save_rss_feed(rss_feed, 'anonblogs_rss_feed.xml')
        print("RSS feed generated and saved as 'anonblogs_rss_feed.xml'")
    else:
        print("Failed to fetch website content.")
