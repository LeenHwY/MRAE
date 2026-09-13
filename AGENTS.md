# AGENTS.md

本文件是 MD 简历管理器的协作与开发约定，适用于仓库中的人类开发者、AI 编程代理和后续跨平台维护。

## 项目定位

这是一个 Python CLI 工具，将用户指定的 Markdown 简历渲染为规范的单页 A4 PDF。

核心边界：

- 只支持单个 Markdown 输入文件。
- 只面向单页 A4 简历；内容超过一页时构建失败。
- 不负责多页简历管理，也不强制具体简历章节格式。
- 用户可以通过 HTML 模板和 CSS 自定义视觉样式。
- 构建失败不得覆盖已有的成功 PDF。

## 项目结构

- `src/resume_manager/`: Python 包和 CLI 实现。
- `src/resume_manager/config.py`: 读取 TOML 配置并解析项目路径。
- `src/resume_manager/loader.py`: 读取并检查 Markdown 文件。
- `src/resume_manager/renderer.py`: 使用 `markdown-it-py` 将 Markdown 转换为 HTML，并内嵌本地图片资源。
- `src/resume_manager/pdf.py`: 使用 Playwright Chromium 检查单页高度并生成 PDF。
- `config/config.toml`: 输入简历、输出 PDF、HTML 模板和 CSS 的路径配置。
- `resumes/`: 示例或用户维护的 Markdown 简历及相关图片资源。
- `templates/default.html`: HTML 外层模板。
- `templates/style.css`: A4 页面尺寸、布局、颜色和排版样式。
- `tests/`: 自动化测试。
- `output/`: 本地生成结果，不提交到 Git。

## 环境初始化

Python 版本要求见 `pyproject.toml`，当前最低版本为 Python 3.11。

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m playwright install chromium
```

### macOS / Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/python -m playwright install chromium
```

不要提交 `.venv/`、Playwright 浏览器缓存或 `output/` 生成物。

## 常用命令

Windows：

```powershell
.venv\Scripts\python -m resume_manager check
.venv\Scripts\python -m resume_manager build
```

macOS / Linux：

```bash
.venv/bin/python -m resume_manager check
.venv/bin/python -m resume_manager build
```

也可以通过 `--config` 指定其他配置文件：

```text
python -m resume_manager build --config path/to/config.toml
```

## 修改规则

### 修改简历内容

- 优先修改 `resumes/` 下的 Markdown 文件。
- 不要把个人真实信息写入框架源码、测试或公共模板，除非用户明确要求。
- Markdown 中的第一张图片会被模板作为可选的右上角照片处理。
- 本地图片路径相对于 Markdown 简历所在目录。

### 修改样式或模板

- 颜色、字体、间距、照片尺寸和单页布局优先修改 `templates/style.css`。
- HTML 结构修改放在 `templates/default.html`，并同步检查 CSS 选择器。
- 当前 Markdown HTML 内嵌默认关闭，渲染器配置为 `html=False`。如果要开启，必须先设计标签白名单和安全过滤，不要直接全量放开。
- 修改照片尺寸时要同步调整 CSS Grid 右列、照片容器和图片本身的宽高。
- 不要使用会让照片或正文脱离布局的绝对定位，除非同时增加浏览器级布局测试。

### 修改 Python 代码

- 保持公共 CLI 命令和 TOML 配置字段兼容，除非需求明确要求变更。
- 使用 `pathlib.Path` 处理路径，避免写死 Windows 分隔符。
- 路径、文件编码和异常信息应兼容 Windows、macOS 和 Linux。
- 外部资源失败时给出明确的 CLI 错误，不要静默覆盖成功输出。
- 保持 PDF 输出使用临时文件，确认成功后再替换目标文件。
- 不做与当前需求无关的重构。

## 验证要求

每次修改后至少运行与改动相关的检查：

1. Python 语法或类型相关改动：

   ```text
   python -m compileall -q src tests
   ```

2. Markdown、模板或渲染相关改动：

   ```text
   python -m resume_manager check
   ```

3. PDF、CSS、布局或照片相关改动：

   ```text
   python -m resume_manager build
   ```

4. 如果新增或修改测试，运行项目测试命令，并确保测试不依赖开发者本机的绝对路径。

验证时应关注：

- 仍然是单页 A4。
- 内容溢出时构建失败。
- 构建失败不会覆盖旧 PDF。
- 照片、姓名和正文没有互相覆盖。
- 本地图片能正确内嵌到 HTML/PDF。

## GitHub 与跨端协作

- 提交源代码、配置示例、模板、测试和文档；不提交 `.venv/`、`output/`、缓存和个人隐私数据。
- 新增依赖必须同步修改 `pyproject.toml`，不要只依赖本地环境。
- 命令和文档同时提供 Windows 与 macOS/Linux 形式，避免依赖 `py` 启动器或硬编码盘符。
- 使用 UTF-8 保存 Markdown、Python、HTML、CSS 和 TOML 文件。
- 保持示例路径使用相对路径；需要外部简历时通过 `config.toml` 指定绝对路径。
- 不提交真实身份证件、联系方式、照片或其他个人敏感信息。
- 提交信息应简短说明行为变化，例如 `fix: keep photo inside resume header layout`。

## 当前验证基线

一个干净环境应能完成：

1. 创建 `.venv`。
2. 执行 `pip install -e .`。
3. 执行 `python -m playwright install chromium`。
4. 使用示例配置运行 `check`。
5. 使用示例配置运行 `build` 并生成 `output/resume.pdf`。

README 是面向最终使用者的说明；本文件是面向开发者和代理的协作约束。两者出现冲突时，应优先确认实际代码和用户最新需求，并同步修正文档。
