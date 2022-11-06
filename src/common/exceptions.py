from typing import Dict, Any, Optional


class ApplicationError(Exception):

    def __init__(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        self.message = message
        self.extra = extra or {}
