from pathlib import Path
import base64
import mimetypes
import re
from urllib.parse import quote

from markdown_it import MarkdownIt

from .errors import ResumeManagerError


def _local_image_uri(source: str, asset_base_dir: Path | None) -> str:
    if asset_base_dir is None or "://" in source or source.startswith(("data:", "#")):
        return source

    image_path = Path(source).expanduser()
    if not image_path.is_absolute():
        image_path = asset_base_dir / image_path
    if not image_path.is_file():
        return source

    mime_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def render_html(
    markdown_text: str,
    template_path: Path,
    stylesheet_path: Path,
    title: str,
    asset_base_dir: Path | None = None,
) -> str:
    if not template_path.exists():
        raise ResumeManagerError(f"HTML 模板不存在: {template_path}")
    if not stylesheet_path.exists():
        raise ResumeManagerError(f"CSS 样式文件不存在: {stylesheet_path}")

    markdown = MarkdownIt("commonmark", {"html": False, "linkify": True})
    default_image_rule = markdown.renderer.rules["image"]

    def render_image(tokens, index, options, environment):
        token = tokens[index]
        source = token.attrGet("src")
        if source:
            token.attrSet("src", _local_image_uri(source, asset_base_dir))
        return default_image_rule(tokens, index, options, environment)

    markdown.renderer.rules["image"] = render_image
    content = markdown.render(markdown_text)
    content = re.sub(
        r"<p>(?=<img(?:\s|>))",
        '<p class="resume-photo">',
        content,
    )
    header, separator, body = content.partition("<h2>")
    if separator:
        content = f'<header class="resume-header">{header}</header>{separator}{body}'
    template = template_path.read_text(encoding="utf-8")
    stylesheet_uri = f"data:text/css;charset=utf-8,{quote(stylesheet_path.read_text(encoding='utf-8'))}"
    return (
        template.replace("{{ title }}", title)
        .replace("{{ stylesheet_uri }}", stylesheet_uri)
        .replace("{{ content }}", content)
    )
