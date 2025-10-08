# Thin wrapper retained for backward compatibility.
"""
url_crawl.py: Thin wrapper retained for backward compatibility.
Executes the main entry point from openai_url_harvester.
"""
from __future__ import annotations

from openai_url_harvester.__main__ import main

if __name__ == "__main__":
    main()
