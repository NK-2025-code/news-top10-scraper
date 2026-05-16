# -*- coding: utf-8 -*-
"""
评分器：计算新闻的综合评分
新评分顺序: 热度(35%) > 新鲜度(25%) > 关键词(20%) > 源权重(15%) > 长度(5%)
"""

from datetime import datetime, timedelta
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class NewsScorer:
    def __init__(self, config):
        self.config = config
        self.score_weights = config['weights']
        self.freshness_levels = config['freshness_levels']
        self.keywords = config['keywords']
    
    def calculate_engagement_score(self, source_weight: float, keyword_count: int) -> float:
        """
        计算热度分数 (0-1)
        热度 = 源权重(60%) + 关键词数量(40%)
        """
        keyword_score = min(keyword_count / len(self.keywords), 1.0)
        engagement = source_weight * 0.6 + keyword_score * 0.4
        return min(engagement, 1.0)
    
    def calculate_freshness_score(self, published_str: str) -> float:
        """
        计算新鲜度分数 (0-1)
        越新的文章分数越高
        """
        try:
            if not published_str:
                return 0.5
            
            # 尝试解析发布时间
            try:
                # 尝试多种时间格式
                from dateutil import parser
                published_time = parser.parse(published_str)
            except:
                return 0.5
            
            now = datetime.now(published_time.tzinfo) if published_time.tzinfo else datetime.now()
            delta = now - published_time
            
            # 根据时间差返回分数
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
            return 0.5
    
    def calculate_keyword_score(self, title: str, summary: str) -> tuple:
        """
        计算关键词分数和匹配数量
        返回 (分数, 关键词数量)
        """
        text = f"{title} {summary}".lower()
        matched_keywords = []
        total_weight = 0
        
        for keyword, info in self.keywords.items():
            if keyword.lower() in text:
                matched_keywords.append(keyword)
                total_weight += info['weight']
        
        # 分数 = 匹配的关键词权重总和 / 最大可能权重
        max_weight = sum(info['weight'] for info in self.keywords.values())
        keyword_score = min(total_weight / max_weight if max_weight > 0 else 0, 1.0)
        
        return keyword_score, len(matched_keywords)
    
    def calculate_length_score(self, text: str) -> float:
        """
        计算内容长度分数
        最优长度: 300-800字
        """
        length = len(text)
        
        if length < 100:
            return 0.2
        elif 100 <= length < 300:
            return 0.6
        elif 300 <= length <= 800:
            return 1.0  # 完美长度
        elif 800 < length <= 1500:
            return 0.8
        else:
            return 0.5  # 过长
    
    def score_article(self, article: Dict) -> float:
        """
        计算单篇文章的综合分数
        顺序: 热度 > 新鲜度 > 关键词 > 源权重 > 长度
        """
        source_weight = article.get('source_weight', 0.8)
        keyword_score, keyword_count = self.calculate_keyword_score(
            article.get('title', ''),
            article.get('summary', '')
        )
        
        # 热度 = 源权重(60%) + 关键词(40%)
        engagement = self.calculate_engagement_score(source_weight, keyword_count)
        
        freshness = self.calculate_freshness_score(article.get('published', ''))
        
        length = self.calculate_length_score(
            f"{article.get('title', '')} {article.get('summary', '')}"
        )
        
        # 综合分数计算
        total_score = (
            engagement * self.score_weights['engagement'] +      # 热度: 35%
            freshness * self.score_weights['freshness'] +        # 新鲜度: 25%
            keyword_score * self.score_weights['keywords'] +     # 关键词: 20%
            source_weight * self.score_weights['source'] +       # 源权重: 15%
            length * self.score_weights['length']                # 长度: 5%
        )
        
        return round(total_score, 3)
    
    def rank_articles(self, articles: List[Dict], top_n: int = 10) -> List[Dict]:
        """
        给文章排序，返回Top N
        """
        # 去重（按title）
        unique_articles = {}
        for article in articles:
            title = article['title']
            if title not in unique_articles:
                unique_articles[title] = article
        
        # 评分
        for article in unique_articles.values():
            article['score'] = self.score_article(article)
        
        # 排序（按分数降序）
        ranked = sorted(
            unique_articles.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        logger.info(f"排序完成，返回Top {top_n}新闻")
        logger.info(f"评分范围: {ranked[0]['score']:.2f} - {ranked[min(top_n-1, len(ranked)-1)]['score']:.2f}")
        
        return ranked[:top_n]
