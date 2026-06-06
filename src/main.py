import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

from scraper import RSSscraper
from scorer import NewsScorer
from config import RSS_SOURCES, OUTPUT_CONFIG, SCORING_CONFIG

# 每个 region 按分类配额各取 N 篇，保证多样性
CATEGORY_QUOTA = {
    'tech': 2,
    'ai': 2,
    'supply_chain': 2,
    'politics': 2,
    'business': 2,
}

def pick_top_by_quota(scored_articles, quota):
    """
    从已按分数降序排列的文章中，按分类配额选取。
    配额满后剩余篇数从高分文章里补全，确保总数达到目标。
    """
    by_cat = defaultdict(list)
    for a in scored_articles:
        by_cat[a.get('category', 'unknown')].append(a)

    selected = []
    used_titles = set()

    # 第一轮：按配额各取
    for cat, limit in quota.items():
        count = 0
        for a in by_cat[cat]:
            if count >= limit:
                break
            if a['title'] not in used_titles:
                selected.append(a)
                used_titles.add(a['title'])
                count += 1

    # 第二轮：配额不足时用剩余高分文章补全
    target = sum(quota.values())
    if len(selected) < target:
        for a in scored_articles:
            if len(selected) >= target:
                break
            if a['title'] not in used_titles:
                selected.append(a)
                used_titles.add(a['title'])

    return sorted(selected, key=lambda x: x['score'], reverse=True)


def main():
    print("=" * 60)
    print("开始抓取 — 中国新闻 & 国外新闻各 Top 10")
    print("=" * 60)

    OUTPUT_FILE = OUTPUT_CONFIG['output_file']

    # 抓取
    scraper = RSSscraper(RSS_SOURCES)
    articles = scraper.scrape_all()

    if not articles:
        print("❌ 未能抓取到任何文章")
        return

    # 评分（全量）
    scorer = NewsScorer(SCORING_CONFIG)
    all_scored = scorer.rank_articles(articles, top_n=10000)

    # 建立 source -> region/category 映射，补全缺失字段
    source_meta = {s['name']: s for s in RSS_SOURCES}
    for a in all_scored:
        meta = source_meta.get(a.get('source'), {})
        if not a.get('region'):
            a['region'] = meta.get('region', 'global')
        if not a.get('category'):
            a['category'] = meta.get('category', 'tech')

    # 按 region 分组
    china_articles  = [a for a in all_scored if a.get('region') == 'china']
    global_articles = [a for a in all_scored if a.get('region') == 'global']

    china_top10  = pick_top_by_quota(china_articles,  CATEGORY_QUOTA)
    global_top10 = pick_top_by_quota(global_articles, CATEGORY_QUOTA)

    # 输出结构
    result = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total_articles': len(articles),
        'china': {
            'count': len(china_top10),
            'articles': china_top10
        },
        'global': {
            'count': len(global_top10),
            'articles': global_top10
        }
    }

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 打印预览
    for region_key, label in [('china', '🇨🇳 中国新闻'), ('global', '🌍 国外新闻')]:
        print(f"\n{'='*60}\n{label} Top 10\n{'='*60}")
        for i, a in enumerate(result[region_key]['articles'], 1):
            print(f"{i}. [{a.get('category','?').upper()} | {a['source']}] 评分:{a['score']}")
            print(f"   {a['title']}")

    print(f"\n✅ 结果已保存到: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == '__main__':
    main()
