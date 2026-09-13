class ResumeManagerError(Exception):
    """Base error for expected CLI failures."""


class ResumeOverflowError(ResumeManagerError):
    """Raised when the rendered resume exceeds one A4 page."""
