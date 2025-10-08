"""
Sitemap utilities for generating XML sitemaps and sitemap indexes.
Provides functions to write sitemaps and optionally gzip the output.
"""

from __future__ import annotations

import gzip
import os
from datetime import datetime, timezone
from typing import Iterable
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring


def _write_bytes(path: str, data: bytes, gzip_output: bool) -> str:
    if gzip_output:
        if not path.endswith(".gz"):
            path = path + ".gz"
        with gzip.open(path, "wb") as f:
            f.write(data)
    else:
        with open(path, "wb") as f:
            f.write(data)
    return path


def write_sitemap(urls: Iterable[str]) -> bytes:
    """Return a UTF-8 XML sitemap document for the given URLs."""
    urlset = Element(
        "urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    )
    now = datetime.now(timezone.utc).date().isoformat()
    for u in urls:
        uel = SubElement(urlset, "url")
        SubElement(uel, "loc").text = u
        SubElement(uel, "lastmod").text = now
    xml_bytes = tostring(urlset, encoding="utf-8")
    return minidom.parseString(xml_bytes).toprettyxml(
        indent="  ", encoding="utf-8"
    )


def write_sitemap_index(entries: list[tuple[str, str]]) -> bytes:
    """
    Return a sitemap index XML as bytes.

    entries: list of (loc, lastmod_iso_date)
    """
    smi = Element(
        "sitemapindex", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
    )
    for loc, lastmod in entries:
        el = SubElement(smi, "sitemap")
        SubElement(el, "loc").text = loc
        SubElement(el, "lastmod").text = lastmod
    xml_bytes = tostring(smi, encoding="utf-8")
    return minidom.parseString(xml_bytes).toprettyxml(
        indent="  ", encoding="utf-8"
    )


def write_sitemap_auto(
    urls: list[str],
    out_path: str,
    max_urls: int = 50_000,
    gzip_output: bool = False,
) -> list[str]:
    """
    Write a single sitemap or a sitemap
    index + parts, returning written file paths.

    Splits into chunks of at most `max_urls` per the protocol.
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    if len(urls) <= max_urls:
        data = write_sitemap(urls)
        path = _write_bytes(out_path, data, gzip_output)
        return [path]

    # Multi-part with index
    written: list[str] = []
    today = datetime.now(timezone.utc).date().isoformat()
    base, ext = os.path.splitext(out_path)
    part = 0
    index_entries: list[tuple[str, str]] = []

    while urls:
        chunk = urls[:max_urls]
        urls = urls[max_urls:]
        part += 1
        part_path = f"{base}_{part}{ext}"
        data = write_sitemap(chunk)
        written_path = _write_bytes(part_path, data, gzip_output)
        written.append(written_path)

        # Assume local file path maps to deploy URL later; caller may rewrite.
        index_entries.append((part_path, today))

    index_bytes = write_sitemap_index(index_entries)
    idx_path = _write_bytes(out_path, index_bytes, gzip_output=False)
    written.insert(0, idx_path)
    return written


def utcnow():
    """Return the current UTC datetime (timezone-aware)."""
    return datetime.now(timezone.utc)
