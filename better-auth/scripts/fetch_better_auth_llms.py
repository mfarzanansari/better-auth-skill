#!/usr/bin/env python3
"""Fetch Better Auth markdown docs from llms.txt and store them locally.

Usage example:
  python3 scripts/fetch_better_auth_llms.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_SOURCE_URL = "https://www.better-auth.com/llms.txt"
DEFAULT_WORKERS = 12
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3

LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def _script_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_output_dir() -> Path:
    return _script_root() / "references" / "upstream" / "better-auth"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _fetch_bytes(url: str, timeout: int, retries: int) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": "codex-better-auth-llms-fetcher"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(0.35 * (2 ** (attempt - 1)))

    if last_error is None:
        raise RuntimeError(f"unknown fetch error for {url}")
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def _extract_markdown_urls(source_url: str, llms_text: str) -> list[str]:
    urls: set[str] = set()
    for raw_link in LINK_PATTERN.findall(llms_text):
        raw_link = raw_link.strip()
        if not raw_link:
            continue

        # Resolve relative links against the llms.txt URL and drop fragments/query.
        resolved = urllib.parse.urljoin(source_url, raw_link)
        split = urllib.parse.urlsplit(resolved)
        clean = split._replace(query="", fragment="")
        if not clean.path.endswith(".md"):
            continue
        normalized = urllib.parse.urlunsplit(clean)
        urls.add(normalized)

    return sorted(urls)


def _relative_path_from_url(url: str) -> str:
    split = urllib.parse.urlsplit(url)
    rel = split.path.lstrip("/")
    if not rel:
        raise ValueError(f"url has empty path: {url}")
    return rel


def _write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_bytes(content)
    tmp_path.replace(path)


def _iter_files_recursive(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted([p for p in root.rglob("*") if p.is_file()])


def _remove_empty_dirs(root: Path) -> None:
    if not root.exists():
        return
    for directory in sorted([p for p in root.rglob("*") if p.is_dir()], key=lambda p: len(p.parts), reverse=True):
        if directory == root:
            continue
        try:
            directory.rmdir()
        except OSError:
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Better Auth markdown docs from llms.txt")
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL)
    parser.add_argument("--output-dir", default=str(_default_output_dir()))
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--prune", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    output_dir = Path(args.output_dir).resolve()
    manifest_path = Path(args.manifest).resolve() if args.manifest else output_dir / "manifest.json"

    if args.workers < 1:
        print("[ERROR] --workers must be >= 1", file=sys.stderr)
        return 1
    if args.retries < 1:
        print("[ERROR] --retries must be >= 1", file=sys.stderr)
        return 1
    if args.timeout < 1:
        print("[ERROR] --timeout must be >= 1", file=sys.stderr)
        return 1

    print(f"[INFO] Source URL: {args.source_url}")
    print(f"[INFO] Output dir: {output_dir}")
    print(f"[INFO] Manifest:   {manifest_path}")
    print(f"[INFO] Dry run:    {args.dry_run}")
    print(f"[INFO] Prune:      {args.prune}")

    try:
        llms_bytes = _fetch_bytes(args.source_url, timeout=args.timeout, retries=args.retries)
        llms_text = llms_bytes.decode("utf-8", "replace")
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Unable to fetch source llms.txt: {exc}", file=sys.stderr)
        return 1

    urls = _extract_markdown_urls(args.source_url, llms_text)
    if not urls:
        print("[ERROR] No markdown URLs found in llms.txt", file=sys.stderr)
        return 1

    print(f"[INFO] Markdown URLs discovered: {len(urls)}")

    fetched_at = _now_iso()
    results: dict[str, tuple[bytes, str]] = {}
    failures: list[tuple[str, str]] = []

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {
            executor.submit(_fetch_bytes, url, args.timeout, args.retries): url
            for url in urls
        }

        for future in as_completed(future_map):
            url = future_map[future]
            try:
                content = future.result()
                relative_path = _relative_path_from_url(url)
                results[url] = (content, relative_path)
            except Exception as exc:  # noqa: BLE001
                failures.append((url, str(exc)))

    if failures:
        print("[ERROR] Failed downloads:", file=sys.stderr)
        for url, err in sorted(failures):
            print(f"  - {url}: {err}", file=sys.stderr)
        return 1

    entries = []
    total_bytes = 0
    expected_paths: set[Path] = set()

    for url in sorted(results):
        content, relative_path = results[url]
        total_bytes += len(content)
        file_path = output_dir / relative_path
        expected_paths.add(file_path.resolve())

        if not args.dry_run:
            _write_atomic(file_path, content)

        entries.append(
            {
                "url": url,
                "relative_path": relative_path,
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": len(content),
                "fetched_at": fetched_at,
            }
        )

    llms_snapshot_path = output_dir / "source-llms.txt"
    if not args.dry_run:
        _write_atomic(llms_snapshot_path, llms_bytes)

    expected_paths.add(llms_snapshot_path.resolve())
    expected_paths.add(manifest_path.resolve())

    removed_files = 0
    if args.prune and output_dir.exists() and not args.dry_run:
        for existing in _iter_files_recursive(output_dir):
            existing_resolved = existing.resolve()
            if existing_resolved not in expected_paths:
                existing.unlink()
                removed_files += 1
        _remove_empty_dirs(output_dir)

    manifest_payload = {
        "source_url": args.source_url,
        "generated_at": fetched_at,
        "document_count": len(entries),
        "documents": entries,
    }

    if not args.dry_run:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest_payload, indent=2) + "\n", encoding="utf-8")

    print(f"[OK] Documents fetched: {len(entries)}")
    print(f"[OK] Total bytes:       {total_bytes}")
    print(f"[OK] Removed stale:     {removed_files}")
    print("[OK] Completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
