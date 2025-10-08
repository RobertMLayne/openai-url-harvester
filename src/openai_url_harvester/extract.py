"""extract.py: Utilities for extracting URLs from files and
directories. Supports text, HTML, and PDF files. Provides
functions to extract URLs and save them in list or JSON format.
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Iterable

from bs4 import BeautifulSoup
from chardet import detect
from pdfminer.high_level import extract_text as pdf_extract_text

URL_RE = re.compile(r"(https?://[^\s<>'\"\\)\\]]+)", re.IGNORECASE)


def _read_text_guess(path: pathlib.Path) -> str:
    """Read file as text using chardet to guess encoding."""
    b = path.read_bytes()
    enc = "utf-8"
    try:
        enc = detect(b).get("encoding") or "utf-8"
    except (OSError, ValueError):
        pass
    try:
        return b.decode(enc, errors="ignore")
    except UnicodeDecodeError:
        return b.decode("utf-8", errors="ignore")


def extract_from_files(paths: Iterable[str]) -> list[str]:
    """Extract http(s) URLs from the given files and directories."""
    urls: set[str] = set()
    for p in paths:
        pth = pathlib.Path(p)
        if pth.is_dir():
            for f in pth.rglob("*"):
                if f.is_file():
                    urls.update(extract_from_files([str(f)]))
        else:
            lower = pth.suffix.lower()
            try:
                if lower in {".md", ".txt", ".json", ".csv", ".html", ".htm"}:
                    txt = _read_text_guess(pth)
                    urls.update(URL_RE.findall(txt))
                    if lower in {".html", ".htm"}:
                        soup = BeautifulSoup(txt, "html.parser")
                        for tag, attr in (("a", "href"), ("link", "href")):
                            for t in soup.find_all(tag):
                                href = t.get(attr)
                                if href:
                                    href_str = (
                                        str(href[0])
                                        if isinstance(href, list)
                                        else str(href)
                                    )
                                    if href_str.startswith(
                                        ("http://", "https://")
                                    ):
                                        urls.add(href_str)
                elif lower == ".pdf":
                    txt = pdf_extract_text(str(pth)) or ""
                    urls.update(URL_RE.findall(txt))
            except (OSError, UnicodeDecodeError, ValueError):
                # Skip unreadable/unsupported files
                continue
    return sorted(urls)


def save_list(urls: list[str], out_path: str) -> None:
    """Save a list of URLs to a text file, one URL per line."""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(urls))


def save_json(urls: list[str], out_path: str) -> None:
    """Save a list of URLs to a JSON file under the key 'urls'."""
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"urls": urls}, f, ensure_ascii=False, indent=2)
