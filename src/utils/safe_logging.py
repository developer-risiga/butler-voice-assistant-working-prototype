# src/utils/safe_logging.py
import logging
import sys

def _is_printable(ch: str, stream) -> bool:
    try:
        enc = getattr(stream, "encoding", None) or "utf-8"
        ch.encode(enc)
        return True
    except Exception:
        return False

class SanitizingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        sanitized = []
        out_stream = sys.stdout

        for ch in msg:
            if _is_printable(ch, out_stream):
                sanitized.append(ch)
            else:
                sanitized.append("?")

        record.msg = "".join(sanitized)
        record.args = ()
        return True

def configure_logging(level=logging.INFO):
    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    handler.addFilter(SanitizingFilter())

    root.handlers = []
    root.addHandler(handler)
