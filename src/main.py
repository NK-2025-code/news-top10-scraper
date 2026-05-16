import json
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from scraper import RSSscraper
from scorer import NewsScorer
# 引入字典配置
from config import RSS_SOURCES, OUTPUT_CONFIG, SCORING_CONFIG

def main():
    print("=" * 60)
    print("开始抓取并生成各分类 Top 2 新闻")
    print("=" * 60)
    
    OUTPUT_FILE = OUTPUT_CONFIG['output_file']
    
    # 第1步：抓取所有RSS源
    scraper = RSSscraper(RSS_SOURCES)
    articles = scraper.scrape_all()
    
    if not articles:
        print("❌ 未能抓取到任何文章")
        return
    
    # 第2步：评分和全量排序
    # 必须将 SCORING_CONFIG 传给 NewsScorer
    scorer = NewsScorer(SCORING_CONFIG)
    # 取一个极大的 top_n 值（如 10000），让评分器返回所有去重并打好分的文章
    all_scored_articles = scorer.rank_articles(articles, top_n=10000)
    
    # 第3步：按类别分组并强制提取每个分类的 Top 2
    target_categories = ['tech', 'supply_chain', 'politics', 'ai', 'business']
    articles_by_category = defaultdict(list)
    
    for article in all_scored_articles:
        cat = article.get('category')
        if cat in target_categories:
            articles_by_category[cat].append(article)
            
    top_articles = []
    for cat in target_categories:
        # 因为 all_scored_articles 已经是按分数降序排列好的
        # 这里直接取前2篇即为该类别的最高分文章
        cat_top2 = articles_by_category[cat][:2]
        top_articles.extend(cat_top2)
        
    # 将提取出的10篇文章，再按总分做一次全局降序排序，保证最终榜单质量最高的内容在最前
    top_articles = sorted(top_articles, key=lambda x: x['score'], reverse=True)
    
    # 第4步：生成结果
    result = {
        'generated_at': datetime.now().isoformat(),
        'total_articles': len(articles),
        'top_count': len(top_articles),
        'articles': top_articles
    }
    
    # 第5步：保存到文件
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印结果
    print("\n" + "=" * 60)
    print("✅ 各分类 Top 2 榜单生成完毕")
    print("=" * 60)
    for i, article in enumerate(top_articles, 1):
        # 终端展示时加上类别前缀以便检查
        cat_display = article.get('category', 'unknown').upper()
        print(f"\n{i}. 【{cat_display} | {article['source']}】 评分: {article['score']}")
        print(f"   标题: {article['title']}")
        print(f"   链接: {article['link']}")
        print(f"   摘要: {article['summary'][:80]}...")
    
    print(f"\n结果已保存到: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == '__main__':
    main()
