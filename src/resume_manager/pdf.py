from pathlib import Path
import os

from .errors import ResumeOverflowError, ResumeManagerError


def _load_playwright(browsers_path: Path):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browsers_path)
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise ResumeManagerError("缺少 Playwright，请先安装项目依赖。") from error
    return PlaywrightError, sync_playwright


def check_single_page(html: str, browsers_path: Path) -> None:
    playwright_error, sync_playwright = _load_playwright(browsers_path)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html, wait_until="networkidle")
            overflowed = page.locator(".resume-page").evaluate(
                "element => element.scrollHeight > element.clientHeight + 1"
            )
            browser.close()
        if overflowed:
            raise ResumeOverflowError("简历内容超过一页 A4，高度溢出，未覆盖已有 PDF。")
    except ResumeOverflowError:
        raise
    except playwright_error as error:
        raise ResumeManagerError(
            "无头浏览器启动失败，请在项目虚拟环境中执行: python -m playwright install chromium"
        ) from error


def build_pdf(html: str, output_path: Path, browsers_path: Path) -> None:
    playwright_error, sync_playwright = _load_playwright(browsers_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(output_path.suffix + ".tmp")

    try:
        check_single_page(html, browsers_path)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(html, wait_until="networkidle")
            page.pdf(
                path=str(temporary_path),
                format="A4",
                print_background=True,
                prefer_css_page_size=True,
            )
            browser.close()
        temporary_path.replace(output_path)
    except ResumeOverflowError:
        temporary_path.unlink(missing_ok=True)
        raise
    except playwright_error as error:
        temporary_path.unlink(missing_ok=True)
        raise ResumeManagerError(
            "无头浏览器启动失败，请在项目虚拟环境中执行: python -m playwright install chromium"
        ) from error
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise
