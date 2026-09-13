from pathlib import Path

from resume_manager.config import AppConfig


def test_load_config_resolves_project_paths(tmp_path: Path) -> None:
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_path = config_dir / "config.toml"
    config_path.write_text(
        'resume_path = "resumes/resume.md"\n'
        'output_pdf = "output/resume.pdf"\n'
        'template_html = "templates/default.html"\n'
        'stylesheet = "templates/style.css"\n',
        encoding="utf-8",
    )

    config = AppConfig.load(config_path)

    assert config.resume_path == tmp_path / "resumes/resume.md"
    assert config.output_pdf == tmp_path / "output/resume.pdf"
