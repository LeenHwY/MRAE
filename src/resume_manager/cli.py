import argparse
from pathlib import Path

from .config import AppConfig
from .errors import ResumeManagerError
from .loader import load_resume
from .pdf import build_pdf, check_single_page
from .renderer import render_html


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="将 Markdown 简历生成单页 A4 PDF")
    parser.add_argument(
        "command",
        choices=("check", "build"),
        help="check 只检查并渲染，build 生成 PDF",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/config.toml"),
        help="配置文件路径",
    )
    return parser


def run(command: str, config_path: Path) -> int:
    config = AppConfig.load(config_path)
    markdown_text = load_resume(config.resume_path)
    html = render_html(
        markdown_text,
        config.template_html,
        config.stylesheet,
        config.resume_path.stem,
        config.resume_path.parent,
    )

    if command == "check":
        check_single_page(html, config.playwright_browsers_path)
        print(f"检查通过: {config.resume_path}")
        print("已完成 Markdown 解析、HTML 渲染和单页 A4 溢出检查。")
        return 0

    build_pdf(html, config.output_pdf, config.playwright_browsers_path)
    print(f"PDF 已生成: {config.output_pdf}")
    return 0


def main() -> int:
    args = make_parser().parse_args()
    try:
        return run(args.command, args.config)
    except (OSError, KeyError, ResumeManagerError) as error:
        print(f"错误: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
