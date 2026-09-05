# 科研个人主页：内容修改指南

日常只修改 `content.toml`，无需编辑 HTML。保存并推送后，GitHub Actions 会自动将内容生成到 HTML 并部署到 https://felixchen04.github.io/ 。页面样式沿用原版。

## 应该改哪个文件？

`content.toml` 是 UTF-8 纯文本，可用记事本、VS Code 或 GitHub 在线编辑器打开。其中已经包含所有占位内容及中文注释。

| 分组 | 填写内容 |
| --- | --- |
| `[site]` | 浏览器标题、搜索描述、语言、更新日期 |
| `[labels]` | 导航与栏目标题，换中文时在这里翻译 |
| `[profile]` | 姓名、身份、单位、头像、研究方向、个人简介 |
| `[[contacts]]` | 邮箱、简历、Google Scholar、GitHub 等链接 |
| `[[publications]]` | 研究方向、论文标题、作者、年份、会议、简介、摘要和链接 |
| `[[education]]` | 教育经历 |
| `[[experience]]` | 科研与实习经历 |
| `[[teaching]]` | 教学经历：dates 为学期，institution 为课程名，role 为职务，description 为学校 |
| `[[honors]]` | 奖项和年份 |
| `[[notes]]` | 讲义、笔记、链接及状态 |

等号左边的字段名保持不变，修改右边的值。`[profile]` 这样的单方括号分组只能出现一次；`[[publications]]` 这样的双方括号表示可重复条目。

## 填写示例

```toml
[profile]
name = "Your Name"
name_local = "你的中文姓名"
role = "Ph.D. Student · Department of Mathematics"
affiliation = "Your University"
photo = "assets/profile.jpg"
initials = "YN"
interests = ["Machine Learning", "Optimization"]
bio = '''
这里写第一段个人简介，可用 **加粗** 强调文字。

空一行开始下一段。可以写中文，也可以写英文。
'''
```

请修改已有分组，不要在文件末尾再次添加同名 `[profile]`。正文是纯文本，不是完整 Markdown：简介、作者、论文概要、摘要及经历/笔记描述支持 `**加粗**`；简介和摘要还支持空行分段。链接使用专用 `url` 字段，HTML 标签会按普通文字显示。

普通字符串用双引号包裹；需要在其中写英文双引号时，用 `\"`。长摘要也可以像 `bio` 一样用三单引号包裹并换行；多行文字内部不要写连续三个单引号。保存编码选择 UTF-8。

### 新增论文

复制一个完整的 `[[publications]]` 小节，再修改其字段：

```toml
[[publications]]
group = "Machine Learning"
year = "2026"
venue = "Preprint"
neutral = true
title = "Your Paper Title"
authors = "**Your Name**, Collaborator Name"
summary = "一句话介绍这篇论文。"
abstract = '''
这里填写完整摘要。
'''
links = [
  { label = "Paper", url = "https://arxiv.org/abs/YOUR_ID" },
  { label = "Code", url = "https://github.com/YOUR_USERNAME/YOUR_REPO" },
]
```

示例网址须替换成真实地址。相同 `group` 自动归入同一研究方向，分组按首次出现顺序排列，组内按文件顺序排列。`neutral = true` 是灰色会议标签，`false` 是蓝色；不要给 true/false 加引号。摘要留空 `abstract = ""` 时不显示展开按钮。

新增教育、经历、奖项、笔记或联系方式同理，复制对应双方括号小节即可。删除整个条目即可移除它；删除某栏目的全部条目后，该栏目和导航入口自动隐藏。

### 头像、简历、邮箱与论文链接

- 头像放入 `assets/profile.jpg`，再填写 `photo = "assets/profile.jpg"`。空字符串保留占位头像。
- 简历和讲义放入自行创建的 `files/` 文件夹，例如 `files/cv.pdf`，链接填写同样的相对路径。
- 邮箱填写 `url = "mailto:you@university.edu"`。
- 其他外部链接填写完整 `https://...` 地址。尚未准备好的链接留空，网页显示占位文字。
- 本地链接只支持 `assets/` 和 `files/` 下已存在的文件，大小写必须一致；文件名尽量不要含空格。生成器会检查文件是否存在。
- 页脚日期由 `[site].updated` 手动填写；`[site].title` 和 `description` 也请同步更新。

## 修改后需要运行脚本吗？

**更新线上网站：不需要。** 修改并推送后，GitHub 自动运行生成脚本，再部署生成的 HTML：

```powershell
git add .
git commit -m "Update homepage content"
git push
```

这次首次迁移需要将 `content.toml`、`scripts/`、`templates/`、更新后的工作流和其他改动一起提交。以后通常只修改并提交内容文件和新增的图片/PDF。也可以在 GitHub 直接编辑 `content.toml` 并提交到 `main`，效果相同。

到仓库 Actions 等待绿色对勾后刷新网站。语法或文件路径有误时，生成步骤会失败并提示原因，原有线上版本保留。

**本地预览：需要先生成一次。** 安装 Python 3.11 或更高版本，然后在项目文件夹运行：

```powershell
py -3 scripts/build.py
```

如果你的 Python 命令是 `python`，则运行 `python scripts/build.py`。无需安装任何第三方包。生成后双击 `index.html`，或刷新已经打开的页面。

仓库中的 `index.html` 是预览快照，修改 TOML 不会自动更新本地快照；GitHub 每次部署都会重新生成，所以无需为了线上发布手动更新它，也不会自动把生成结果提交回仓库。不要直接编辑这个文件，修改会在下次生成时被覆盖。

## 文件结构

```text
content.toml                日常编辑的唯一内容来源
scripts/build.py            生成脚本（Python 标准库）
templates/page.html         页面外壳模板（日常不用改）
index.html                  生成的静态页面 / 本地预览快照
assets/                     样式、图标和个人头像
files/                      可选的简历、讲义等公开文件
.github/workflows/pages.yml 自动生成和部署
```

原有 GitHub Pages 的 Source 保持 GitHub Actions 即可。部署仅发布生成页面、assets 和可选 files；内容源文件不进入网站产物，但公开仓库中的源文件仍可被访问。
