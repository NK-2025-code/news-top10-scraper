import json
import sys
from datetime import datetime
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from scraper import RSSscraper
from scorer import NewsScorer
# 🔧 修复 1：修改这里的导入，引入字典配置
from config import RSS_SOURCES, OUTPUT_CONFIG, SCORING_CONFIG

def main():
    print("=" * 60)
    print("开始抓取Top 10新闻")
    print("=" * 60)
    
    # 🔧 修复 2：从 OUTPUT_CONFIG 中提取输出路径和数量
    OUTPUT_FILE = OUTPUT_CONFIG['output_file']
    TOP_N = OUTPUT_CONFIG['top_n']
    
    # 第1步：抓取所有RSS源
    scraper = RSSscraper(RSS_SOURCES)
    articles = scraper.scrape_all()
    
    if not articles:
        print("❌ 未能抓取到任何文章")
        return
    
    # 第2步：评分和排序
    # 🔧 修复 3：必须将 SCORING_CONFIG 传给 NewsScorer
    scorer = NewsScorer(SCORING_CONFIG)
    top_articles = scorer.rank_articles(articles, TOP_N)
    
    # 第3步：生成结果
    result = {
        'generated_at': datetime.now().isoformat(),
        'total_articles': len(articles),
        'top_count': len(top_articles),
        'articles': top_articles
    }
    
    # 第4步：保存到文件
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # 打印结果
    print("\n" + "=" * 60)
    print("✅ Top 10 最值得阅读的新闻")
    print("=" * 60)
    for i, article in enumerate(top_articles, 1):
        print(f"\n{i}. 【{article['source']}】 评分: {article['score']}")
        print(f"   标题: {article['title']}")
        print(f"   链接: {article['link']}")
        print(f"   摘要: {article['summary'][:100]}...")
    
    print(f"\n结果已保存到: {OUTPUT_FILE}")
    print("=" * 60)

if __name__ == '__main__':
    main()
