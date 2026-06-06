import feedparser
import requests
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RSSscraper:
    def __init__(self, sources: List[Dict]):
        self.sources = sources
        self.articles = []

    def fetch_feed(self, source: Dict) -> List[Dict]:
        """抓取单个RSS源"""
        try:
            logger.info(f"正在抓取 {source['name']}...")
            feed = feedparser.parse(source['url'])
            
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
            
        except Exception as e:
            logger.error(f"抓取 {source['name']} 失败: {str(e)}")
            return []

    def scrape_all(self) -> List[Dict]:
        """抓取所有RSS源"""
        all_articles = []
        for source in self.sources:
            articles = self.fetch_feed(source)
            all_articles.extend(articles)
        
        self.articles = all_articles
        logger.info(f"总共抓取 {len(all_articles)} 篇文章")
        return all_articles
