from datetime import datetime, timedelta
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class NewsScorer:
    def __init__(self):
        self.score_weights = {
            'freshness': 0.3,      # 新鲜度 30%
            'source': 0.3,         # 源权重 30%
            'keywords': 0.2,       # 关键词 20%
            'length': 0.2          # 内容长度 20%
        }
        
        # 热点关键词
        self.hot_keywords = [
            'AI', '人工智能', '机器学习', 'ChatGPT', 'GPT-4',
            'web3', '区块链', '加密', '融资', '收购',
            '创新', '突破', '首次', '最新', '重磅',
            '技术', 'API', '开源', '开发者', '效率'
        ]

    def calculate_freshness_score(self, published_str: str) -> float:
        """计算新鲜度分数 (0-1)"""
        try:
            # 简单处理，假设最近发布的文章分数高
            if not published_str:
                return 0.5
            
            # 越新的文章分数越高
            return 0.9 if len(published_str) > 0 else 0.5
        except:
            return 0.5

    def calculate_keyword_score(self, title: str, summary: str) -> float:
        """根据关键词计算分数"""
        text = f"{title} {summary}".lower()
        keyword_count = sum(1 for kw in self.hot_keywords if kw.lower() in text)
        
        # 关键��越多分数越高，但有上限
        return min(keyword_count / len(self.hot_keywords), 1.0)

    def calculate_length_score(self, text: str) -> float:
        """内容长度分数"""
        # 300-500字为最优
        length = len(text)
        if length < 100:
            return 0.3
        elif 100 <= length < 300:
            return 0.6
        elif 300 <= length <= 500:
            return 1.0
        else:
            return 0.8

    def score_article(self, article: Dict) -> float:
        """计算单篇文章的综合分数"""
        freshness = self.calculate_freshness_score(article.get('published', ''))
        source_score = article.get('source_weight', 0.8)
        keyword = self.calculate_keyword_score(
            article.get('title', ''),
            article.get('summary', '')
        )
        length = self.calculate_length_score(
            f"{article.get('title', '')} {article.get('summary', '')}"
        )
        
        total_score = (
            freshness * self.score_weights['freshness'] +
            source_score * self.score_weights['source'] +
            keyword * self.score_weights['keywords'] +
            length * self.score_weights['length']
        )
        
        return round(total_score, 3)

    def rank_articles(self, articles: List[Dict], top_n: int = 10) -> List[Dict]:
        """给文章排序，返回Top N"""
        # 去重（按title）
        unique_articles = {}
        for article in articles:
            title = article['title']
            if title not in unique_articles:
                unique_articles[title] = article
        
        # 评分
        for article in unique_articles.values():
            article['score'] = self.score_article(article)
        
        # 排序
        ranked = sorted(
            unique_articles.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        logger.info(f"排序完成，返回Top {top_n}新闻")
        return ranked[:top_n]
