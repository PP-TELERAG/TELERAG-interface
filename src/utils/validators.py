class UrlValidator():
    @staticmethod
    def is_telegram_url(url: str) -> bool:
        url = url.strip().lower()
        return any(url.startswith(prefix) for prefix in ("@", "t.me/", "https://t.me/", "http://t.me/"))

    @staticmethod
    def normalize_telegram_url(url: str) -> str:
        url = url.strip().lower()

        if url.startswith("@"):
            return f"https://t.me/{url[1:]}"

        if url.startswith(("http://", "https://")):
            return url.replace("http://", "https://")

        if url.startswith("t.me/"):
            return f"https://{url}"

        return f"https://t.me/{url}"

    @staticmethod
    def validate_telegram_channel(url: str) -> tuple[bool, str]:
        normalized = UrlValidator.normalize_telegram_url(url)

        channel_name = normalized[13:]

        if not 5 <= len(channel_name) <= 32:
            return False, ""

        allowed_chars = set("abcdefghijklmnopqrstuvwxyz0123456789_")
        if not all(c in allowed_chars for c in channel_name):
            return False, ""

        return True, normalized