from urllib.parse import urlparse

class ValidateUtils:

    def looks_like_gsheets(self, url: str) -> bool:
        if "docs.google.com/spreadsheets" in url:
            return True
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https") and parsed.path.lower().endswith(".xlsx"):
            return True
        return False