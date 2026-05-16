# 每日Top 10新闻爬虫

自动抓取和整理每天最值得阅读的技术新闻。

## 功能特性

- ✅ 自动从多个RSS源抓取新闻
- ✅ 智能评分排序 (考虑新鲜度、来源、关键词、内容长度)
- ✅ 每天自动运行 (北京时间 9:00)
- ✅ 支持手动触发
- ✅ 去重处理

## RSS源

- TechCrunch
- 财新网
- ReadHub

## 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 执行爬虫
python src/main.py
```

### 查看结果

结果保存在 `data/news.json`

## 自定义配置

编辑 `src/config.py`:

```python
# 修改RSS源
RSS_SOURCES = [...]

# 修改输出数量
TOP_N = 15

# 修改输出文件
OUTPUT_FILE = 'data/my_news.json'
```

## 执行日志

- GitHub Actions 会每天自动运行
- 可在 Actions 标签页查看执行日志
- 点击 "workflow_dispatch" 可手动触发

## 项目结构

```
news-top10-scraper/
├── .github/
│   └── workflows/
│       └── daily-scrape.yml
├── src/
│   ├── config.py
│   ├── scraper.py
│   ├── scorer.py
│   └── main.py
├── data/
│   └── news.json
├── requirements.txt
└── README.md
```
