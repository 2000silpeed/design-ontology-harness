"""Download the generated species images listed in assets/manifest.json.

Run this once the GPT Image 2 asset CDN host is reachable from this
environment (it is blocked by the default network egress policy). After it
succeeds, re-render the screens with `render_html.py` to embed the real images.
"""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
MANIFEST = json.loads((ASSETS / "manifest.json").read_text())


def main() -> int:
    ok = True
    for item in MANIFEST["assets"]:
        dest = ASSETS / item["file"]
        try:
            with urllib.request.urlopen(item["url"], timeout=30) as resp:
                data = resp.read()
            if len(data) < 1000:
                raise ValueError(f"suspiciously small payload ({len(data)} bytes)")
            dest.write_bytes(data)
            print(f"ok   {item['file']}  ({len(data)} bytes)")
        except Exception as exc:  # noqa: BLE001
            ok = False
            print(f"FAIL {item['file']}: {exc}", file=sys.stderr)
    if not ok:
        print(
            "\nSome downloads failed. If you see a 403 'Host not in allowlist', "
            "add the manifest URL host to the environment's network egress "
            "allowlist, or download the files manually into this assets/ dir.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
