#!/usr/bin/env python3
"""Upload a local file to a netdrive signed URL with retry on credential errors."""
import argparse
import sys
import time
import urllib.request


def put_file(url: str, file_path: str, max_retries: int = 3) -> int:
    headers = {
        "Content-Type": "application/octet-stream",
        "x-oss-forbid-overwrite": "false",
    }
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            with open(file_path, "rb") as f:
                data = f.read()
            req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.status
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code in (403, 400) and attempt < max_retries:
                print(f"Attempt {attempt} failed (HTTP {e.code}), retrying after 2s...", file=sys.stderr)
                time.sleep(2)
                continue
            raise
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                print(f"Attempt {attempt} failed ({e}), retrying...", file=sys.stderr)
                time.sleep(2)
                continue
            raise
    raise RuntimeError(f"Max retries exceeded. Last error: {last_error}")


def main():
    parser = argparse.ArgumentParser(description="PUT upload file with retry")
    parser.add_argument("url", help="Signed upload URL")
    parser.add_argument("file_path", help="Local file path")
    parser.add_argument("--max-retries", type=int, default=3)
    args = parser.parse_args()
    status = put_file(args.url, args.file_path, args.max_retries)
    print(f"Upload succeeded: HTTP {status}")


if __name__ == "__main__":
    main()
