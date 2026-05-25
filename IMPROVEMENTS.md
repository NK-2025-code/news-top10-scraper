# news-top10-scraper 仓库总结与改进建议

## 一、仓库概览

**用途**：Python 编写的 RSS 新闻聚合 + 排名工具。每天抓取 17 个 RSS 源（5 个分类：tech / supply_chain / politics / ai / business），按 5 维加权打分，每个分类取 top 2，共 10 篇写入 `data/news.json`；GitHub Pages 站点（`docs/index.html`）以手绘风、中英双语展示。GitHub Actions 每天 01:00 UTC 自动运行并提交 JSON。

**文件结构**

| 文件 | 行数 | 职责 |
|------|------|------|
| `src/main.py` | 97 | 编排入口 |
| `src/scraper.py` | 51 | `RSSscraper` 同步抓取 |
| `src/scorer.py` | 160 | `NewsScorer` 五维打分（engagement / freshness / keywords / source / length） |
| `src/config.py` | 328 | 数据配置：RSS 源、打分权重、关键词词典、分类元数据 |
| `data/news.json` | — | 最近一次输出 |
| `docs/index.html` | 481 | 前端单文件站点，运行时通过 GitHub Contents API 读 JSON |
| `.github/workflows/daily-scrape.yml` | — | 每日 cron + 自动 commit |

**运行方式**
- 本地：`pip install -r requirements.txt && python src/main.py`（须从 repo 根目录执行）
- 自动：GitHub Actions cron `0 1 * * *`（北京时间 09:00）

**数据流**

```
RSS_SOURCES (config.py)
    ↓
RSSscraper.scrape_all()   — 串行，无 timeout，无 category 字段
    ↓
NewsScorer.rank_articles() — 去重（仅精确 title），打分，排序
    ↓
main.py: 补 category → 每分类取 top 2 → 重排
    ↓
data/news.json  →  GitHub Pages / Contents API  →  index.html
```

---

## 二、问题清单

### P0 — 正确性

- [ ] **`scraper.py` 不传递 `category` 字段**（scraper.py:23-31）：`main.py:38-49` 用反查 dict 打补丁，应从源头修。
- [ ] **`calculate_engagement_score` 数学有误**（scorer.py:26）：`keyword_count / len(self.keywords)`，分母 ≈110，命中 5 个关键词仅贡献 0.045，keyword 因子几乎被吞掉。
- [ ] **关键词与 source_weight 双重计算**：`engagement` 内已混入两者，外部 `weights` 又各自计一次 → 实际占比远超声明值。
- [ ] **`top_n=10000` 魔数 hack**（main.py:34）：应让 `rank_articles` 支持 `top_n=None`。
- [ ] **去重过弱**（scorer.py:140-144）：仅精确 title 比对，同一篇多源转发仍重复；建议加 URL 规范化 + title 归一化。
- [ ] **空列表崩溃**（scorer.py:158）：全部源失败时 `ranked[0]['score']` 会 `IndexError`。
- [ ] **写文件非原子**（main.py:77-78）：中途崩溃会损坏 `news.json`；应写临时文件再 `os.replace`。

### P1 — 健壮性 / 可观测性

- [ ] **抓取无 timeout / 无 UA / 无重试 / 串行**（scraper.py:fetch_feed）：17 个源可并发，任一源挂死会拖慢整个 job。
- [ ] **未校验 `feed.bozo` / `feed.status`**：解析失败安静返回空。
- [ ] **裸 `except:`**（scorer.py:44）：应收窄为 `except (ValueError, TypeError)`。
- [ ] **`logging.basicConfig` 在 import 时副作用**（scraper.py:7）：污染调用方的 logging 配置。
- [ ] **时区不一致**：`fetch_time` 用 naive local（scraper.py:30），`generated_at` 用 UTC（main.py:67）。
- [ ] **CI 工作流未使用 `requirements.txt`**（daily-scrape.yml:27）：版本 pin 形同虚设；`git commit … || true`（line 37）默默吞掉失败。

### P2 — 代码质量 / 可维护性

- [ ] **包结构缺失**：`src/` 无 `__init__.py`，`main.py` 用 `sys.path.insert` workaround。
- [ ] **类型注解稀少**；`RSSscraper` 不符合 PEP 8（应为 `RSSScraper`）。
- [ ] **分类名重复定义在 4 处**（`RSS_SOURCES`、`main.target_categories`、`CATEGORY_CONFIG`、`docs/index.html` 的 `categoryThemes`）→ 漂移风险；Python 端 `CATEGORY_CONFIG` 未被任何 Python 代码引用，是死代码。
- [ ] **关键词字典每条带 `category` 字段但 scorer 从不使用** → 死配置。
- [ ] **魔数散落**：`feed.entries[:50]`、`summary[:200]`、`[:2]`（每类篇数）、`top_n=10000`。
- [ ] **README 已过时**：仍写"3 个 RSS 源"，实际 17 个。
- [ ] **前端硬编码仓库路径** `NK-2025-code/news-top10-scraper`（docs/index.html:327）→ fork 后无法直接用。
- [ ] **`_config.yml` 与 `.nojekyll` 同时存在**，语义冲突；前端已绕过 Pages 走 GitHub Contents API。

### P3 — 工程化基建（当前全部缺失）

- [ ] 无任何测试（无 `tests/`、无 pytest、无 fixture）
- [ ] 无 lint / format / type-check 配置（无 ruff、black、mypy、pre-commit）
- [ ] 无 PR CI（只有 daily cron，PR 不跑任何检查）
- [ ] 无打包配置（无 `pyproject.toml`、无 CLI entrypoint）

### 安全

- [ ] **前端 XSS 风险**：RSS 源不可信，`docs/index.html` 的 `displayNews` 函数（~line 380）使用 `innerHTML` 注入 title/summary → 应改为 `textContent` 或做 sanitize。
- [ ] **HTTP 源未走 HTTPS**：ArXiv CS feed 用 `http://`（config.py:33）。

---

## 三、改进方案（分阶段）

### Phase A — 低风险清扫（预计 ~1 小时）

目标：消除明显 bug，统一配置入口，修复 CI。

- `scraper.py`：`fetch_feed` 的 article dict 加 `category=source['category']`
- `main.py`：移除 source→category 反查 workaround；`[:2]` 提成 `OUTPUT_CONFIG['per_category']`；用 `os.replace` 实现原子写；`top_n=10000` 改为 `top_n=None`
- `scorer.py`：`rank_articles` 支持 `top_n=None`；裸 `except` 改成 `except (ValueError, TypeError)`；空列表早返回（`if not articles: return []`）
- `config.py`：`OUTPUT_CONFIG` 加 `per_category: 2`；把 `[:50]`、`[:200]` 提成常量
- `workflow`：改成 `pip install -r requirements.txt`；去掉 `|| true`
- `README`：更新到 17 源 / 5 分类 / 每类 Top 2

### Phase B — 抓取健壮性（预计 ~1–2 小时）

目标：并发、容错、去重升级。

- 用 `concurrent.futures.ThreadPoolExecutor(max_workers=8)` 并发抓取
- 通过 `requests` 预取（加自定义 UA、timeout=10s），再把 response text 喂给 `feedparser.parse`
- 校验 `feed.bozo` / `feed.status`，按源记录 success/fail，写到 `news.json` metadata
- 去重：按 URL 规范化（去 tracking 参数）+ title 归一化（小写、去标点、去多余空白）双重比对

### Phase C — 评分模型修复（预计 ~1 小时）

目标：让 5 个权重维度互不重叠、行为符合 config 中的声明。具体方案在 Phase B 完成后与用户确认（选项：全面重写 / 仅修 keyword 分母 / 仅打 TODO）。

---

## 四、验证方法

1. `python src/main.py` 本地跑通，产出正好 10 篇，每分类 2 篇。
2. `data/news.json` 的每条 `category` 字段不为空。
3. 故意把一个 RSS URL 改坏 → 工作流日志报错不再被 `|| true` 吞掉；其它源正常入库。
4. 并发后总运行时间 < 串行版本的一半（17 源，期望 <15s）。
