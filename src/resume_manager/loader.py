from pathlib import Path

from .errors import ResumeManagerError


def load_resume(path: Path) -> str:
    if not path.exists():
        raise ResumeManagerError(f"简历文件不存在: {path}")
    if path.suffix.lower() != ".md":
        raise ResumeManagerError(f"配置的简历文件不是 Markdown 文件: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as error:
        raise ResumeManagerError(f"简历文件不是有效的 UTF-8 文本: {path}") from error
