# Academic Homepage · 科研个人主页

简洁、响应式的学术主页模板。内容均为占位文本，包含个人简介、研究方向、分类论文（可展开摘要）、教育经历、科研经历、荣誉及讲义资源。

使用原生 HTML + CSS，无需安装依赖、无需构建，没有追踪脚本或外部字体。双击 `index.html` 即可本地预览；支持 GitHub Pages 的个人域名和仓库子路径。

## 部署到 GitHub Pages

1. 在 GitHub 创建一个空的 **Public** 仓库。个人主站建议命名为 `你的用户名.github.io`；也可以使用 `academic-homepage` 等普通名称。创建时不要勾选初始化 README、License 或 .gitignore。
2. 在本文件夹打开终端，把下面的 `YOUR_USERNAME` 和 `YOUR_REPOSITORY` 替换为实际值，再执行：

   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git push -u origin main
   ```

   若你是通过 ZIP 下载而不是使用已初始化的仓库，先执行 `git init -b main`、`git add .` 和 `git commit -m "Create academic homepage"`。Git 需要配置你自己的用户名和邮箱；推送时按 GitHub 提示登录。

3. 在仓库进入 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。
4. 在 **Actions** 打开 **Deploy academic homepage to GitHub Pages**，点击 **Run workflow**，选择 `main`。以后向 `main` 推送内容会自动更新网站。如果首次推送发生在启用 Pages 之前并失败，启用后重新运行即可。
5. 等待部署完成，在 **Settings → Pages** 查看访问地址：个人主站为 `https://YOUR_USERNAME.github.io/`，普通仓库为 `https://YOUR_USERNAME.github.io/YOUR_REPOSITORY/`。

部署配置遵循 [GitHub Pages 自定义工作流文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。工作流仅发布 `index.html`、`assets/` 及可选的 `files/`，不发布 README 等仓库文件。

## 修改内容

所有正文集中在 **`index.html`**，无需理解 JavaScript 或模板语法。

| 内容 | 修改位置 |
| --- | --- |
| 浏览器标题和搜索摘要 | `<title>` 和 `meta name="description"` |
| 顶栏姓名、个人信息、简介 | `PROFILE` 注释附近及 `.wordmark` |
| 头像 | 把照片放入 `assets/profile.jpg`，按照 HTML 注释把头像占位块替换为 `<img>` |
| 论文、作者、会议和摘要 | `PUBLICATIONS` 下的 `<article class="paper">`，复制整块即可添加论文 |
| 教育、经历、奖项及笔记 | 对应标题下的条目 |
| 页脚日期 | 手动修改 `Last updated` |
| 主题色和字体 | `assets/style.css` 顶部 `:root` |
| 浏览器图标 | `assets/favicon.svg` 中的字母和颜色 |

示例中的身份、论文和奖项都不是你的真实信息，请在正式展示前替换。模板将尚未填写的外部链接显示为普通文字，避免访客点到无效页面。

### 添加邮箱、简历和学术链接

在 `.contact-links` 内，将相应的 `<span>...</span>` 替换为真实链接，例如：

```html
<a href="mailto:you@university.edu">Email ↗</a>
<a href="files/cv.pdf">CV ↗</a>
<a href="https://scholar.google.com/citations?user=YOUR_ID">Google Scholar ↗</a>
<a href="https://github.com/YOUR_USERNAME">GitHub ↗</a>
```

创建 `files/` 文件夹后放入真实 PDF；默认工作流会自动发布该文件夹。这里的文件都会公开，请只放适合公开分享的资料。

论文链接同样将 `.pending` 占位文字替换为 `<a href="实际论文地址">Paper ↗</a>`；笔记标题也可改成 `<a href="files/notes.pdf">笔记名称</a>`。

使用 `assets/...`、`files/...` 这样的相对路径，避免 `/assets/...`，从而兼容普通仓库的子路径。文件名大小写必须与链接一致。

### 使用中文

将 `<html lang="en">` 改成 `<html lang="zh-CN">`，再直接翻译正文和导航即可。样式已包含中文字体回退。

## 文件结构

```text
index.html                 页面及所有个人内容
assets/style.css           页面样式和手机适配
assets/favicon.svg         站点图标
.github/workflows/pages.yml GitHub Pages 自动部署
.nojekyll                  禁用 Jekyll 处理
.gitignore                排除临时文件
README.md                 使用说明
```

信息结构参考 [Zixun Huang 的个人主页](https://alexhuang13.github.io/)，代码与排版为本模板重新编写，没有复制其个人资料、头像或论文内容。
