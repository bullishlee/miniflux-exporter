#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for Miniflux Exporter.
"""

import re
from pathlib import Path
from typing import Any, Dict


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Clean filename by removing illegal characters.

    Args:
        filename: Original filename.
        max_length: Maximum filename length.

    Returns:
        Sanitized filename.
    """
    # Remove or replace illegal characters
    filename = re.sub(r'[\\/:*?"<>|]', "_", filename)
    # Remove leading/trailing spaces
    filename = filename.strip()
    # Remove consecutive underscores
    filename = re.sub(r"_+", "_", filename)
    # Remove leading/trailing underscores and dots
    filename = filename.strip("_.")
    # Limit length
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename or "untitled"


def create_markdown_frontmatter(entry: Dict[str, Any]) -> str:
    """
    Create YAML Front Matter for Markdown file.

    Args:
        entry: Miniflux entry object.

    Returns:
        YAML formatted Front Matter string.
    """
    feed_title = entry.get("feed", {}).get("title", "Unknown")
    category_title = (
        entry.get("feed", {}).get("category", {}).get("title", "Uncategorized")
    )

    # Escape quotes
    title = entry.get("title", "").replace('"', '\\"')
    author = entry.get("author", "").replace('"', '\\"')
    feed_title = feed_title.replace('"', '\\"')
    category_title = category_title.replace('"', '\\"')

    frontmatter = f"""---
title: "{title}"
author: "{author}"
feed: "{feed_title}"
category: "{category_title}"
url: "{entry.get('url', '')}"
published_at: "{entry.get('published_at', '')}"
created_at: "{entry.get('created_at', '')}"
status: "{entry.get('status', '')}"
starred: {str(entry.get('starred', False)).lower()}
reading_time: {entry.get('reading_time', 0)}
entry_id: {entry.get('id', 0)}
feed_id: {entry.get('feed_id', 0)}
---

"""
    return frontmatter


def format_filename(entry: Dict[str, Any], template: str = "{date}_{title}") -> str:
    """
    Format filename based on template.

    Args:
        entry: Miniflux entry object.
        template: Filename template with placeholders.

    Returns:
        Formatted filename (without extension).
    """
    # Get date
    published_at = entry.get("published_at", "")
    if published_at:
        date = published_at[:10]  # YYYY-MM-DD
    else:
        from datetime import datetime

        date = datetime.now().strftime("%Y-%m-%d")

    # Get title
    title = entry.get("title", "Untitled")
    title = sanitize_filename(title)

    # Get ID
    entry_id = entry.get("id", 0)

    # Format filename
    filename = template.format(date=date, title=title, id=entry_id)

    return sanitize_filename(filename)


def get_save_path(
    entry: Dict[str, Any],
    base_dir: str,
    organize_by_feed: bool = True,
    organize_by_category: bool = False,
) -> Path:
    """
    Determine save path for entry based on organization settings.

    Args:
        entry: Miniflux entry object.
        base_dir: Base output directory.
        organize_by_feed: Whether to organize by feed.
        organize_by_category: Whether to organize by category.

    Returns:
        Path object for the entry's directory.
    """
    path = Path(base_dir)

    if organize_by_category:
        # Organize by category
        category_title = (
            entry.get("feed", {}).get("category", {}).get("title", "Uncategorized")
        )
        category_name = sanitize_filename(category_title)
        path = path / category_name

    if organize_by_feed:
        # Organize by feed
        feed_title = entry.get("feed", {}).get("title", "Unknown")
        feed_name = sanitize_filename(feed_title)
        path = path / feed_name

    return path


def print_progress_bar(
    current: int, total: int, prefix: str = "", suffix: str = "", length: int = 40
) -> None:
    """
    Print a progress bar to console.

    Args:
        current: Current progress value.
        total: Total value.
        prefix: Prefix string.
        suffix: Suffix string.
        length: Length of progress bar.
    """
    if total == 0:
        percent = 0
    else:
        percent = current / total * 100

    filled_length = int(length * current // total) if total > 0 else 0
    bar = "█" * filled_length + "░" * (length - filled_length)

    print(
        f"\r{prefix} |{bar}| {current}/{total} ({percent:.1f}%) {suffix}",
        end="",
        flush=True,
    )

    if current == total:
        print()  # New line on completion


def format_bytes(bytes_size: int) -> str:
    """
    Format bytes to human-readable string.

    Args:
        bytes_size: Size in bytes.

    Returns:
        Formatted string (e.g., "1.5 MB").
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"


def validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL string to validate.

    Returns:
        True if URL is valid, False otherwise.
    """
    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    return url_pattern.match(url) is not None


def truncate_string(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate string to maximum length.

    Args:
        text: Text to truncate.
        max_length: Maximum length.
        suffix: Suffix to append if truncated.

    Returns:
        Truncated string.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
