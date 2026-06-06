# -*- coding: utf-8 -*-
"""
评分器：计算新闻的综合评分
新评分顺序: 关键词(45%) > 新鲜度(30%) > 源权重(20%) > 长度(5%)
关键词按文章语言分别匹配（中文文章匹配中文词，英文文章匹配英文词），避免跨语言命中率为零。
"""

import math
from datetime import datetime, timedelta
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


def _is_chinese(text: str) -> bool:
    """中文字符占比超过15%即视为中文文章"""
    if not text:
        return False
    chinese_chars = sum(1 for c in text if '一' <= c <= '鿿')
    return chinese_chars / max(len(text), 1) > 0.15


class NewsScorer:
    def __init__(self, config):
        self.config = config
        self.score_weights = config['weights']
        self.freshness_levels = config['freshness_levels']
        self.keywords = config['keywords']

        # 预分离中英文关键词，避免每篇文章重复计算
        self._cn_keywords = {k: v for k, v in self.keywords.items()
                             if any('一' <= c <= '鿿' for c in k)}
        self._en_keywords = {k: v for k, v in self.keywords.items()
                             if not any('一' <= c <= '鿿' for c in k)}

    def calculate_freshness_score(self, published_str: str) -> float:
        try:
            if not published_str:
                return 0.4
            from dateutil import parser
            published_time = parser.parse(published_str)
            now = datetime.now(published_time.tzinfo) if published_time.tzinfo else datetime.now()
            delta = now - published_time

            if delta <= timedelta(hours=1):
                return self.freshness_levels['hours_1']
            elif delta <= timedelta(hours=6):
                return self.freshness_levels['hours_6']
            elif delta <= timedelta(hours=24):
                return self.freshness_levels['hours_24']
            elif delta <= timedelta(hours=72):
                return self.freshness_levels['hours_72']
            else:
                return self.freshness_levels['days_7']
        except Exception as e:
            logger.warning(f"计算新鲜度分数失败: {str(e)}")
            return 0.4

    def calculate_keyword_score(self, title: str, summary: str) -> float:
        """
        按文章语言分别匹配关键词，返回 0-1 分数。
        用 sqrt 压缩原始命中比例，保留区分度的同时避免零命中文章得分过低。
        """
        text = f"{title} {summary}".lower()
        is_cn = _is_chinese(text)
        pool = self._cn_keywords if is_cn else self._en_keywords

        if not pool:
            return 0.0

        total_weight = sum(info['weight'] for kw, info in pool.items() if kw.lower() in text)
        max_possible = sum(info['weight'] for info in pool.values())

        raw = total_weight / max_possible if max_possible > 0 else 0.0
        return round(min(math.sqrt(raw) * 1.2, 1.0), 4)

    def calculate_length_score(self, text: str) -> float:
        length = len(text)
        if length < 100:
            return 0.2
        elif length < 300:
            return 0.6
        elif length <= 800:
            return 1.0
        elif length <= 1500:
            return 0.8
        else:
            return 0.5

    def score_article(self, article: Dict) -> float:
        source_weight = article.get('source_weight', 0.8)
        keyword_score = self.calculate_keyword_score(
            article.get('title', ''),
            article.get('summary', '')
        )
        freshness = self.calculate_freshness_score(article.get('published', ''))
        length = self.calculate_length_score(
            f"{article.get('title', '')} {article.get('summary', '')}"
        )

        total_score = (
            keyword_score * self.score_weights['keywords'] +
            freshness     * self.score_weights['freshness'] +
            source_weight * self.score_weights['source'] +
            length        * self.score_weights['length']
        )
        return round(total_score, 3)

    def rank_articles(self, articles: List[Dict], top_n: int = 10000) -> List[Dict]:
        unique_articles = {}
        for article in articles:
            title = article['title']
            if title not in unique_articles:
                unique_articles[title] = article

        for article in unique_articles.values():
            article['score'] = self.score_article(article)

        ranked = sorted(unique_articles.values(), key=lambda x: x['score'], reverse=True)

        if ranked:
            end = min(top_n - 1, len(ranked) - 1)
            logger.info(f"评分范围: {ranked[0]['score']:.3f} - {ranked[end]['score']:.3f}")

        return ranked[:top_n]
