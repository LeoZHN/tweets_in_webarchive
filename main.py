import os
import sys
import asyncio
import json
from datetime import datetime

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, expect

print("Script started")

# 获取应用程序路径
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# 读取配置文件
config_path = os.path.join(application_path, 'config.json')
print(f"Looking for config file at: {config_path}")

with open(config_path, 'r') as f:
    config = json.load(f)

OUTPUT_FILE = config['output_file']
START_DATE = datetime.strptime(config['start_date'], '%Y-%m-%d')
END_DATE = datetime.strptime(config['end_date'], '%Y-%m-%d')
URL = config['url']

async def get_illustration(context, url):
    print("Starting get_illustration function")
    async_name = asyncio.current_task().get_name()

    page = await context.new_page()

    try:
        await page.goto(url, timeout=60000)
        await expect(page.locator('li.js-stream-item').nth(0)).to_be_visible(timeout=30000)
    except Exception as e:
        print(f"{async_name} -> Page load error: {str(e)}", flush=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output_file:
        last_article_count = 0
        while True:
            try:
                article_count = await page.locator('li.js-stream-item').count()
            except Exception as e:
                print(f"{async_name} -> Error counting articles: {str(e)}", flush=True)
                break

            if article_count == last_article_count:
                print(f"{async_name} -> No more new tweets.", flush=True)
                break
            last_article_count = article_count

            for y in range(article_count):
                print(f"{async_name} -> Processing tweet {y + 1}", flush=True)

                try:
                    article = page.locator("li.js-stream-item").nth(y)
                    soup = BeautifulSoup(await article.inner_html(), "lxml")

                    time_element = soup.find("span", class_="_timestamp")
                    if not time_element:
                        print(f"{async_name} -> No timestamp found, skipping.", flush=True)
                        continue

                    publish_time = time_element.get("data-time")
                    publish_time_dt = datetime.fromtimestamp(int(publish_time))

                    if publish_time_dt < START_DATE:
                        print(f"{async_name} -> Reached tweets earlier than {START_DATE}, stopping.", flush=True)
                        return

                    if publish_time_dt > END_DATE:
                        print(f"{async_name} -> Tweet date {publish_time_dt} is after {END_DATE}, skipping.", flush=True)
                        continue

                    publish_url = "https://twitter.com" + soup.find("a", class_="tweet-timestamp").get("href")
                    tweet_text = soup.find("p", class_="tweet-text")
                    publish_content = tweet_text.get_text() if tweet_text else ""
                    author = soup.find("strong", class_="fullname").get_text()
                    author_id = soup.find("span", class_="username").get_text()

                    print(f"{async_name} -> Date: {publish_time_dt.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
                    print(f"{async_name} -> Author: {author}{author_id}", flush=True)
                    print(f"{async_name} -> URL: {publish_url}", flush=True)
                    print(f"{async_name} -> Content: {publish_content}", flush=True)

                    output_file.write(f"Date: {publish_time_dt.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    output_file.write(f"Author: {author}{author_id}\n")
                    output_file.write(f"URL: {publish_url}\n")
                    output_file.write(f"Content: {publish_content}\n")
                    output_file.write("=" * 50 + "\n")

                except Exception as e:
                    print(f"{async_name} -> Error processing tweet: {str(e)}", flush=True)

            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            await asyncio.sleep(2)

async def main():
    print("Main function started")
    chromium_path = os.path.join(application_path, 'chromium', 'chrome.exe')
    print(f"Chromium path: {chromium_path}")

    async with async_playwright() as p:
        print("Launching browser")
        browser = await p.chromium.launch(headless=False, executable_path=chromium_path)
        print("Browser launched")
        context = await browser.new_context()
        print("Browser context created")

        print("Starting scraping process")
        await asyncio.gather(
            get_illustration(context, URL)
        )
        print("Scraping process completed")

if __name__ == '__main__':
    print("Script execution started")
    asyncio.run(main())
    print("Script execution completed")