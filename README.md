# Xueyi Zhang — 学术主页

基于 Jekyll 的双语（中/英）个人学术主页，素净学术配色（默认 `ink` 墨蓝，另附 3 套可一键切换），
左栏个人卡片 + 右侧正文，论文以卡片形式展示（主图 + 标签 + PDF/Code/Project 按钮）。可直接部署到 GitHub Pages。

---

## 一、部署到 GitHub Pages

### 前提：GitHub 仓库名必须等于你的用户名

用户页（`用户名.github.io`）有个硬规则：**仓库名必须正好是 `<你的GitHub用户名>.github.io`**，
名字对不上 Pages 就不会生效。

本站对应的账号是 **`xueyizhang1998`**，所以：

| 项目 | 值 |
|---|---|
| 仓库名 | `xueyizhang1998.github.io` |
| 网址 | `https://xueyizhang1998.github.io` |

（网址是小写。域名不区分大小写，GitHub 实际提供服务的是全小写地址。）

### 第 1 步：建空仓库

打开 <https://github.com/new>，仓库名填 `xueyizhang1998.github.io`，
选 Public，**不要勾** Add a README / .gitignore / license（保持空仓库，否则首次推送会冲突）。

### 第 2 步：跑部署脚本

在「终端」里执行：

```bash
cd ~/Desktop/xueyizhang1998.github.io
bash deploy.sh xueyizhang1998
```

> 路径按你解压的实际位置填。本地文件夹叫什么都行，只有 GitHub 上的**仓库名**必须等于用户名。

脚本会依次：把 `_config.yml` 的 `url` 改成你的实际地址 → `git init` → 提交 →
关联远端 → **停下来问你一次**，你回 `y` 才推送。它不会自动传任何东西。

如果 git 还没设过提交身份，脚本会在 `git init` 之后问你姓名和邮箱，
**只写进这个仓库**的 `.git/config`，不动你机器上的全局配置、不影响其他项目。

### 第 3 步：开启 Pages（这步只能手动点）

1. 打开 `https://github.com/xueyizhang1998/xueyizhang1998.github.io/settings/pages`
2. Source 选 **Deploy from a branch**
3. Branch 选 `main`，目录选 **/ (root)**，点 Save
4. 等 1–2 分钟，访问 `https://xueyizhang1998.github.io`

> GitHub Pages 会在云端自动用 Jekyll 构建，你本地不用装 Ruby 或 Jekyll。

### 以后更新内容

改完 `_data/` 里的 yml，然后：

```bash
git add -A && git commit -m "update" && git push
```

推上去约 1 分钟后线上自动更新。

### 手动部署（不想用脚本的话）

```bash
cd ~/Desktop/xueyizhang1998.github.io
git init
git add -A
git commit -m "Academic homepage: bilingual Jekyll site"
git branch -M main
git remote add origin https://github.com/xueyizhang1998/xueyizhang1998.github.io.git
git push -u origin main
```

注意手动走这条路时，记得自己把 `_config.yml` 里的 `url:` 改成你的实际地址
（脚本本来会帮你改）。这个值只影响 sitemap 和 RSS 里的绝对链接，页面本身不受影响。

---

## 二、本地预览（两种方式）

**方式 A：不装 Jekyll，直接看效果（推荐先用这个）**

```bash
python3 build_preview.py      # 需要 pip install pyyaml
```

会生成 `preview.html`，双击用浏览器打开即可。它读取的是和正式站点**同一批** `_data/*.yml`，
所见即所得。注意：这只是预览，正式站以 GitHub Pages 构建为准。

**方式 B：本地跑真正的 Jekyll（需要 Ruby 环境）**

```bash
bundle install
bundle exec jekyll serve
# 浏览器打开 http://localhost:4000
```

---

## 三、怎么改内容（都在 `_data/` 里，改完推送即可）

| 想改什么 | 打开这个文件 |
|---|---|
| 姓名 / 身份 / 单位 / 所在地 / 头像 / 邮箱 / 各种链接 | `_data/profile.yml` |
| 自我介绍 + 研究关键词 | `_data/about.yml` |
| News 动态 | `_data/news.yml` |
| **论文列表** | `_data/publications.yml` |
| 论文的研究方向分组（组名、顺序） | `_data/pub_groups.yml` |
| **经历（工作/学历/访学合并）** | `_data/experience.yml` |
| 科研项目 | `_data/projects.yml` |
| 荣誉奖励 | `_data/honors.yml` |
| 界面文案（版块标题、按钮字） | `_data/ui.yml` |

> 注：教育经历与工作/访学经历统一放在 `experience.yml`，按 `sort` 字段（YYYYMM）倒序展示。

每个字段都有 `en` 和 `zh` 两个版本，改冒号右边引号里的文字即可。

### 加一篇论文

在 `_data/publications.yml` 里复制一个 `- title:` 块，按注释填：

```yaml
- title: "你的论文标题"
  authors: "First Author, **Xueyi Zhang**, Third Author"   # 用 **名字** 加粗自己
  venue: "NeurIPS 2025"
  year: 2025
  order: 110               # ★必填★ 越大越靠前；现有最大值是 100，想排最前面就填更大的数
  group: continual          # 属于哪个研究方向，见 _data/pub_groups.yml
  selected: true            # true = 代表作，显示 ★ 并出现在“代表性论文”区
  image: "/assets/img/pub/my-paper.jpg"   # 主图放到 assets/img/pub/ 下；留空则显示占位
  tags: ["Continual Learning", "Deepfake"]
  desc:                     # 一句话贡献要点，可留空
    en: "One-sentence contribution."
    zh: "一句话贡献要点。"
  links:
    paper: "https://..."    # 论文 PDF / 出版页
    code:  "https://github.com/..."   # 代码仓库
    project: "https://..."  # 项目主页
    bibtex: "#"
    video: ""               # 没有的链接留空 "" 即可，按钮会自动隐藏
  note: "Oral"              # 可选，如 Oral / Spotlight
```

**`order` 是排序字段，必填。** 数字越大越靠前，现有论文是 10、20、…、100。
想插到两篇之间就用中间值，比如 75。漏填会被当成 0，掉到列表最底下。

年份不参与排序，只用于显示。原因是同年论文会并列，Jekyll 的排序对并列项的
先后不保证稳定，会出现线上和本地预览顺序不一致的情况，所以改用唯一的 `order`。

`group` 必须是 `_data/pub_groups.yml` 里已有的 id（`continual` / `multimodal` /
`neuro` / `robust`），填错的话那篇论文不会出现在任何分组里。

### 论文展示方式：分组 or 按年份

`_config.yml` 里：

```yaml
group_publications: true    # true = 按研究方向分组；false = 按年份倒序
```

分组的组名与顺序在 `_data/pub_groups.yml` 里改；每篇论文用 `group:` 指定归属。

### 关于代码链接

当前只有两篇论文配了 GitHub 按钮，因为只有这两个官方仓库被核实过：

- `Listening to the Brain` → [NeuroListen/NeuroListen](https://github.com/NeuroListen/NeuroListen)
- `Language Without Borders` → [cslr-lipreading/CSLR](https://github.com/cslr-lipreading/CSLR)

其余八篇暂未找到公开官方仓库，因此没有加 `code` 字段。以后有了仓库，
在对应论文的 `links:` 下加一行 `code: "https://github.com/..."` 即可。

### 换头像和论文主图

- 头像：把图片命名为 `avatar.jpg` 放到 `assets/img/`（或改 `profile.yml` 里的 `avatar` 路径）。
- 论文主图：放到 `assets/img/pub/`，在对应论文的 `image:` 填**完整路径**，
  形如 `/assets/img/pub/my-paper.jpg`（注意开头的斜杠）。
- 建议尺寸：头像正方形（如 400×400），论文主图约 16:10（如 640×400）。

论文主图的显示框是 190×119px，图片按 `object-fit: contain` 缩放，
**不裁切**——所以比例不对只会两侧留白，不会切掉内容，不用自己精修尺寸。
路径写错或图片缺失时，会自动退化成显示会议名的占位块（不会出现裂图）。

### 换经历里的机构 logo

图片放进 `assets/img/logo/`，然后在 `_data/experience.yml` 对应条目里填**文件名**：

```yaml
logo: "nus.png"     # 只写文件名，不要写路径（模板会自动补 /assets/img/logo/）
abbr: "NUS"         # logo 留空时显示的文字占位
```

这里和论文主图的写法不一样：**论文主图填完整路径，机构 logo 只填文件名。**
写成 `logo: "/assets/img/logo/nus.png"` 会导致路径重复拼接，图标显示不出来。

显示框是宽 160px、高度上限 44px，左对齐、按原比例缩放。因此**横版 logo
（校徽 + 校名文字）效果最好**，校名文字仍然清晰可读；压成方形小图标会糊。

新增机构时如果拿到的是为深色页头设计的纯白 logo，记得先反相处理，
否则白底上完全看不见（现有的 NUDT 和 DMU 就是这么处理的，详见
`assets/img/logo/README.md`）。

不想放 logo 就把 `logo` 留空，会自动显示 `abbr` 的文字圆角占位块。

### 加一条经历

在 `_data/experience.yml` 复制一个 `- period:` 块。工作、学历、访学放在同一个
版块里，按 `sort` 字段（YYYYMM 数字）倒序排列，越大越靠上：

```yaml
- period: "2026.06 – Present"   # 显示用的时间区间，写法自由
  sort: 202606                  # 排序用，起始年月，六位数字
  kind: position                # position 职位 / degree 学位 / visiting 访学
  role:
    en: "Research Fellow (Postdoc)"
    zh: "博士后研究员"
  org:
    en: "National University of Singapore"
    zh: "新加坡国立大学"
  dept:                         # 院系，可留空
    en: ""
    zh: ""
  location:
    en: "Singapore"
    zh: "新加坡"
  advisor:                      # 可留空，留空则整行不显示
    en: "Supervisor: Prof. Jiaheng Zhang"
    zh: "合作导师：Jiaheng Zhang 教授"
  logo: "nus.png"
  abbr: "NUS"
```

`kind: visiting` 会在职位后面显示一个「访学」小标签，另两种不显示标签。
访学与读博时间重叠不影响展示，合并成一条时间线看起来是连贯的。

### 放 CV

把你的 PDF 命名为 `cv.pdf` 放到 `assets/`（`profile.yml` 里 `cv` 已指向它）；不需要就把 `cv` 留空。

---

## 四、换配色

全站配色是 Ink 一套（白底 + 墨蓝），没有主题切换器。
所有颜色集中在 `assets/css/style.css` 顶部的 `:root` 变量里，改 hex 即可，
不用动任何组件样式：

```css
:root {
  --accent:      #2f4a6d;   /* ← 主色（墨蓝），改这里换主色 */
  --accent-soft: #436690;   /* 悬停态 */
  --accent-weak: #eef2f7;   /* 标签底色 */
  --gold:        #8a6d3b;   /* 低饱和金棕，点缀用 */
  --bg:          #ffffff;   /* 页面背景底色 */
  ...
}
```

层级逻辑：`--bg` 页面底 → `--surface` 卡片 → `--surface-alt` 侧栏和浅色区块，
`--border` 分割线，正文三档深浅 `--text` / `--text-soft` / `--text-faint`。

> 主色用的是中性墨蓝，不绑定任何学校配色——以后换单位也不用改。
> 如果想换成 NUS 校色（深蓝 `#003D7C` + 橙 `#EF7C00`），把 `--accent` 和 `--gold` 换成这两个值即可。

### 头像形状

默认是圆角方形。想改成圆形，在 `assets/css/style.css` 找 `.avatar`，
把 `border-radius: 18px` 改成 `border-radius: 50%`。

### 关掉某个版块

比如不想要「荣誉奖励」：把 `_data/honors.yml` 内容清空（保留文件），该版块会自动隐藏。

---

## 五、语言

- 右上角「中/EN」按钮切换，记忆在浏览器。
- 默认语言在 `_config.yml` 的 `lang:` 设置（`en` 或 `zh`）。
- 每条内容中英文分开填；只想要单语也可以，把不用的语言留同样文字即可。

---

## 六、目录结构

```
xueyizhang1998.github.io/
├── _config.yml           # 站点配置（默认语言、默认主题、URL）
├── Gemfile               # Ruby 依赖（GitHub Pages 用）
├── index.html            # 首页（拼装各版块）
├── _layouts/default.html # 页面骨架
├── _includes/            # 侧栏、顶部导航、工具条、图标、论文卡片模板
├── _data/                # ★ 你的内容都在这里
├── assets/
│   ├── css/style.css     # 样式 + 4 套配色变量
│   ├── js/main.js        # 语言/主题切换、邮箱反爬、论文展开
│   └── img/              # 头像、论文主图、favicon
├── build_preview.py      # 本地免安装预览生成器
└── preview.html          # 预览产物（可删，运行脚本会重建）
```

---

## 七、待你补充的内容

已按你提供的信息填好：身份（NUS 博士后）、邮箱、教育与访学经历、三项荣誉、
国家重点研发计划项目、10 篇一作论文（标题/会议/年份/论文链接均来自 DBLP 核验表）。

10 篇一作论文的完整作者列表已按 DBLP 填好。页面只展示一作论文，不设合作论文版块。

还差这些：

- [ ] **头像**：把照片命名为 `avatar.jpg` 放到 `assets/img/`（当前显示占位图）
- [ ] **论文主图**：放到 `assets/img/pub/`，在对应论文 `image:` 填路径（当前显示 venue 占位）
- [ ] 合作论文里有几条 `paper:` 链接是空的，可自行补 DOI
- [ ] AAAI 那篇标题待确认（见下方说明）

### 经历版块与机构图标

工作、学历、访学已**合并为一个 Experience 版块**，按时间倒序（`sort` 字段控制，YYYYMM）。
这样访学（2023.03 起）与读博（2020–2025）时间重叠也不会显得对不上。
参考 Hankai Liu 的做法——他同样把职位与学历合并在 `Experiences` 下。

五所学校的**真实校徽已放入**（`assets/img/logo/`，共 44KB）。这些校徽是横版（校徽+校名文字），
所以按原比例左对齐显示、限高 44px，不做成方形小图标——否则校名会糊成一团。
其中国防科大与大连海事的原图是**纯白 logo**（为深色页头设计），放白底上看不见，
已自动反相为深色；深色主题下 CSS 会再反相提亮。详见 `assets/img/logo/README.md`。

头像与十篇论文主图**已放入并处理完毕**（`assets/img/avatar.jpg`、`assets/img/pub/*.jpg`）。
主图按原比例缩放、最大宽 900px，不裁切——因为多张是很扁的架构图，
强行裁成固定比例会切掉两侧关键结构；卡片里由 CSS 的 `object-fit: contain` 负责留白。
想换某张图，直接替换 `assets/img/pub/` 下同名文件即可。

### 论文链接现状

一作 10 篇、合作 9 篇**全部已有链接**（共 24 个链接，含 2 个代码仓库）。

`paper` 字段优先填**免费全文**（CVF / AAAI OJS / NeurIPS 官方页 / ACL Anthology / arXiv），
正式 DOI 填在单独的 `doi` 字段，卡片上显示为灰色次要按钮。这样读者能免费看全文，
引用时也拿得到规范标识符。若 `paper` 本身就是 doi.org 链接，就不必再填 `doi`。

一处已知的例外，在对应条目的注释里写明了：

- **Listening to the Brain** 无正式 DOI（NeurIPS 页面与 DBLP 均未收录；Zenodo 存档 DOI 不等于论文 DOI）

### 仍待补充

- [ ] 博士导师姓名（`experience.yml` 国防科大那条的 `advisor`）
- [ ] 国家重点研发计划的起止年份（`projects.yml` 的 `period`）
- [ ] 中文名确认（`profile.yml` 里暂填「张雪毅」，从拼音反推）
- [ ] CV PDF（放 `assets/cv.pdf` 并在 `profile.yml` 填 `cv: "/assets/cv.pdf"`）
- [ ] ORCID / LinkedIn（可选，`profile.yml`）

Google Scholar 与 DBLP 链接**已填好**。

---

### AAAI 论文标题待确认

DBLP 上该条标题为「Rep Deep & Machine Learning: Exemplar-Free Continual Video Action
Recognition via Slow-Fast Collaborative Learning」。前半段「Rep Deep & Machine Learning」
读起来不像论文标题本体，疑似 DBLP 收录时混入了栏目名。建议打开 PDF 首页核对，
若确认多余，把 `publications.yml` 里该条 `title` 改为
「Exemplar-Free Continual Video Action Recognition via Slow-Fast Collaborative Learning」。

---

## 八、设计参考来源

布局与论文分组参考 [Hankai Liu](https://liuhankai.github.io/) 与
[AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io)；
配置驱动的内容组织方式与克制的排版风格参考 [PRISM](https://github.com/xyjoey/PRISM)（MIT）。
本站为独立实现，未复制上述项目的代码或素材。


