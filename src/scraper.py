import feedparser
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT_SECONDS = 15
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; newsletter-scraper/1.0; +https://github.com/NK-2025-code/news-top10-scraper)'
}


class RSSscraper:
    def __init__(self, sources: List[Dict]):
        self.sources = sources
        self.articles = []

    def fetch_feed(self, source: Dict) -> List[Dict]:
        """抓取单个RSS源"""
        try:
            logger.info(f"正在抓取 {source['name']}...")
            response = requests.get(
                source['url'],
                headers=REQUEST_HEADERS,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            feed = feedparser.parse(response.text)

            articles = []
            for entry in feed.entries[:50]:  # 每个源取前50条
                article = {
                    'title': entry.get('title', 'N/A'),
                    'link': entry.get('link', ''),
                    'source': source['name'],
                    'source_weight': source['weight'],
                    'category': source.get('category', ''),
                    'region': source.get('region', 'global'),
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', '')[:200],  # 摘要前200字
                    'fetch_time': datetime.now().isoformat()
                }
                articles.append(article)

            logger.info(f"成功抓取 {source['name']} 的 {len(articles)} 篇文章")
            return articles

        except requests.RequestException as exc:
            logger.error(f"抓取 {source['name']} 失败: {exc}")
            return []
        except Exception as exc:
            logger.error(f"解析 {source['name']} 失败: {exc}")
            return []

    def scrape_all(self) -> List[Dict]:
        """抓取所有RSS源"""
        max_workers = min(8, max(1, len(self.sources)))
        all_articles = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.fetch_feed, source): source for source in self.sources}
            for future in as_completed(futures):
                try:
                    all_articles.extend(future.result())
                except Exception as exc:
                    source = futures[future]
                    logger.error(f"源 {source['name']} 任务异常: {exc}")

        self.articles = all_articles
        logger.info(f"总共抓取 {len(all_articles)} 篇文章")
        return all_articles
