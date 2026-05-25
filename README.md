# 每日Top 10新闻爬虫

自动抓取和整理每天最值得阅读的新闻，覆盖科技、供应链、政治、AI、商业五大分类。

## 功能特性

- 自动从17个RSS源抓取新闻
- 五维评分排序：热度(35%) > 新鲜度(25%) > 关键词(20%) > 源权重(15%) > 长度(5%)
- 每个分类各取Top 2，共输出10篇
- 每天自动运行 (UTC 1:00 / 北京时间 9:00)
- 支持手动触发
- 去重处理（按标题去重）

## 新闻分类与RSS源

| 分类 | 源 |
|------|----|
| 🔧 科技 | TechCrunch, Hacker News, The Verge, ArXiv CS |
| 📦 供应链 | Supply Chain Dive, FreightWaves, Logistics Mgmt |
| 🏛️ 政治 | Reuters, The Guardian, Politico, China Daily |
| 🤖 AI | OpenAI Blog, DeepMind Blog, AI News |
| 💼 商业 | 钛媒体, 虎嗅, 界面新闻 |

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 执行爬虫
python src/main.py
```

## 查看结果

结果保存在 `data/news.json`，格式如下：

```json
{
  "generated_at": "2026-01-01T01:00:00+00:00",
  "total_articles": 200,
  "top_count": 10,
  "articles": [...]
}
```

## 自定义配置

编辑 `src/config.py`：

```python
# 修改RSS源
RSS_SOURCES = [...]

# 修改输出数量/分数门槛
OUTPUT_CONFIG = {
    'output_file': 'data/news.json',
    'top_n': 10,
    'min_score': 0.5,
}

# 修改评分权重
SCORING_CONFIG = {
    'weights': {
        'engagement': 0.35,
        'freshness': 0.25,
        'keywords': 0.20,
        'source': 0.15,
        'length': 0.05,
    }
}
```

## 执行日志

- GitHub Actions 每天 UTC 1:00 自动运行
- 可在 Actions 标签页查看执行日志
- 点击 "workflow_dispatch" 可手动触发

## 项目结构

```
newletter/
├── .github/
│   └── workflows/
│       └── daily-scrape.yml
├── src/
│   ├── config.py      # RSS源、评分权重、关键词词库
│   ├── scraper.py     # RSS抓取器
│   ├── scorer.py      # 评分器
│   └── main.py        # 入口：抓取 → 评分 → 输出Top 10
├── data/
│   └── news.json
├── requirements.txt
└── README.md
```
