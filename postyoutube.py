#!/usr/bin/env python3

import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from datetime import datetime


def extract_video_id(url):
    p = urlparse(url)

    if p.netloc in ("youtu.be", "www.youtu.be"):
        return p.path.lstrip("/")

    if p.netloc.endswith("youtube.com"):
        if p.path == "/watch":
            return parse_qs(p.query).get("v", [None])[0]

        if p.path.startswith("/shorts/"):
            return p.path.split("/")[2]

        if p.path.startswith("/live/"):
            return p.path.split("/")[2]

        if p.path.startswith("/embed/"):
            return p.path.split("/")[2]

    raise ValueError("Not a supported YouTube URL")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <youtube-url>")
        sys.exit(1)

    video_id = extract_video_id(sys.argv[1])

    now = datetime.now().astimezone()
    #timestamp = now.isoformat(timespec="minutes")
    timestamp = now.isoformat(timespec="seconds")

    filename = f"{now:%Y-%m-%d-%H%M}-{video_id}.md"
    path = Path("content/posts") / filename

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(f"""---
title: ""
date: {timestamp}
draft: false
---
{{{{< youtube {video_id} >}}}}
""")

    print(f"Created {path}")


if __name__ == "__main__":
    main()
