from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class AppConfig:
    root: Path
    resume_path: Path
    output_pdf: Path
    template_html: Path
    stylesheet: Path
    playwright_browsers_path: Path

    @classmethod
    def load(cls, config_path: Path) -> "AppConfig":
        config_path = config_path.resolve()
        with config_path.open("rb") as config_file:
            values = tomllib.load(config_file)

        root = config_path.parent.parent

        def resolve(value: str) -> Path:
            path = Path(value).expanduser()
            return path if path.is_absolute() else root / path

        return cls(
            root=root,
            resume_path=resolve(values["resume_path"]),
            output_pdf=resolve(values["output_pdf"]),
            template_html=resolve(values["template_html"]),
            stylesheet=resolve(values["stylesheet"]),
            playwright_browsers_path=resolve(
                values.get("playwright_browsers_path", ".playwright-browsers")
            ),
        )
