# MD 简历管理器

将用户指定的 Markdown 简历转换为规范的单页 A4 PDF。
新增SSH签名（）。

## 当前范围

- Windows 优先。
- 首期提供 CLI。
- 配置单个 Markdown 文件路径。
- 只允许单页 A4 简历，内容溢出时构建失败。
- 构建失败不会覆盖上一次成功生成的 PDF。
- 框架不限制简历章节格式，也不负责多页简历管理。

## 初始化

```powershell
py -3 -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m playwright install chromium
```

## 使用

```powershell
.venv\Scripts\resume-manager.exe check
.venv\Scripts\resume-manager.exe build
```

默认配置位于 `config/config.toml`，示例简历位于 `resumes/简历模板.md`。

## 标准简历模板

`resumes/简历模板.md` 提供了一份适合单页 A4 简历的通用示例，包含：

- 姓名、目标职位、联系方式和所在地
- 个人简介
- 工作经历
- 项目经历
- 教育经历
- 技能
- 证书与语言

模板不强制固定章节。可以按个人经历删减、重命名或调整章节，但应控制内容总高度，使最终结果保持为单页 A4。

### 可选照片栏

模板中的第一张图片会自动定位到右上角照片栏，当前示例使用：

```markdown
![个人照片](photo-placeholder.svg)
```

使用时可以将 `resumes/photo-placeholder.svg` 替换为自己的照片文件，并同步修改 Markdown 中的文件名，例如：

```markdown
![个人照片](my-photo.jpg)
```

照片路径相对于当前简历文件所在目录。若不需要照片，删除这行图片 Markdown 即可，其他内容会自动占用正常版面。

框架会将简历目录中的本地图片内嵌到 HTML/PDF 中，因此不要求把图片放到固定的模板目录。

### 调整照片尺寸

照片栏使用 CSS Grid 分栏布局，不是脱离文档流的绝对定位。若要修改照片大小，需要在 `templates/style.css` 中同步修改以下三处：

```css
.resume-header {
	grid-template-columns: minmax(0, 1fr) 25mm;
}

.resume-header > p:has(> img) {
	width: 25mm;
	height: 35mm;
}

.resume-header > p:has(> img) > img {
	width: 25mm;
	height: 35mm;
}
```

上例会将照片调整为宽 `25mm`、高 `35mm`。右侧 Grid 列宽度、照片容器尺寸和图片尺寸应保持一致，这样姓名信息会自动使用左侧剩余空间，正文也会从完整头部区域之后开始，不会覆盖照片。

修改后重新执行：

```powershell
.venv\Scripts\python -m resume_manager check
.venv\Scripts\python -m resume_manager build
```

如果照片或其他内容导致简历超过一页 A4，`check` 和 `build` 会报告溢出错误，且不会覆盖已有的成功 PDF。

## Markdown 与 HTML 标签对应关系

框架使用 Python 包 `markdown-it-py`，按 CommonMark 规则将 Markdown 转换为 HTML。常用语法对应关系如下：

| Markdown 写法 | HTML 标签 |
| --- | --- |
| `# 标题` | `<h1>标题</h1>` |
| `## 标题` | `<h2>标题</h2>` |
| `### 标题` | `<h3>标题</h3>` |
| `普通文本` | `<p>普通文本</p>` |
| `- 项目` | `<ul><li>项目</li></ul>` |
| `[链接](地址)` | `<a href="地址">链接</a>` |
| `> 引用` | `<blockquote><p>引用</p></blockquote>` |
| `**加粗**` | `<strong>加粗</strong>` |
| `` `代码` `` | `<code>代码</code>` |
| `---` | `<hr>` |

Markdown 生成的内容会被放入 `templates/default.html` 的以下位置：

```html
<main class="resume-page">
	{{ content }}
</main>
```

因此可以在 `templates/style.css` 中使用 `h1`、`h2`、`h3`、`p`、`ul`、`a`、`blockquote` 等选择器修改对应元素的样式。

## 自定义简历样式

用户可以直接修改 `templates/style.css`，自定义简历的颜色、字体、字号、间距、边框和布局。例如：

```css
:root {
	color: #263238;
	font-family: "Microsoft YaHei", sans-serif;
}

h1,
h2 {
	color: #7b2d26;
}

h2 {
	border-bottom-color: #d9a441;
}

a {
	color: #287271;
}
```

也可以创建新的 CSS 文件，然后在 `config/config.toml` 中修改样式路径：

```toml
stylesheet = "templates/my-style.css"
```

修改样式后重新执行 `build` 即可生成新的 PDF。CSS 只负责视觉样式，Markdown 内容仍由用户自行维护；生成结果仍必须满足单页 A4 高度限制。
