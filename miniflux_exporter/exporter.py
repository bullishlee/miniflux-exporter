#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core exporter module for Miniflux Exporter.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

try:
    import miniflux
except ImportError:
    raise ImportError("miniflux package is required. Install it with: pip install miniflux")

try:
    import html2text
except ImportError:
    raise ImportError("html2text package is required. Install it with: pip install html2text")

from .config import Config
from .utils import (
    sanitize_filename,
    create_markdown_frontmatter,
    format_filename,
    get_save_path,
    print_progress_bar,
    format_bytes
)


logger = logging.getLogger(__name__)


class MinifluxExporter:
    """Main exporter class for Miniflux articles."""

    def __init__(self, config: Config):
        """
        Initialize the exporter.

        Args:
            config: Configuration object.
        """
        self.config = config
        self.client: Optional[miniflux.Client] = None
        self.stats = {
            'total': 0,
            'saved': 0,
            'failed': 0,
            'skipped': 0
        }

    def connect(self) -> bool:
        """
        Connect to Miniflux instance.

        Returns:
            True if connection successful, False otherwise.
        """
        try:
            self.client = miniflux.Client(
                self.config['miniflux_url'],
                api_key=self.config['api_key']
            )

            # Test connection
            user = self.client.me()
            if not user:
                logger.error("Failed to authenticate with Miniflux")
                return False

            logger.info(f"Connected to Miniflux as user: {user.get('username')}")
            return True

        except Exception as e:
            logger.error(f"Failed to connect to Miniflux: {e}")
            return False

    def get_feeds_info(self) -> Dict[str, Any]:
        """
        Get information about feeds and categories.

        Returns:
            Dictionary with feeds and categories info.
        """
        if not self.client:
            raise RuntimeError("Not connected to Miniflux. Call connect() first.")

        try:
            feeds = self.client.get_feeds()
            categories = self.client.get_categories()

            return {
                'feeds': feeds,
                'categories': categories,
                'feeds_count': len(feeds),
                'categories_count': len(categories)
            }
        except Exception as e:
            logger.error(f"Failed to get feeds info: {e}")
            return {
                'feeds': [],
                'categories': [],
                'feeds_count': 0,
                'categories_count': 0
            }

    def get_entries_count(self, **filters) -> int:
        """
        Get total count of entries matching filters.

        Args:
            **filters: Filter parameters for entries.

        Returns:
            Total number of entries.
        """
        if not self.client:
            raise RuntimeError("Not connected to Miniflux. Call connect() first.")

        try:
            result = self.client.get_entries(limit=1, **filters)
            return result.get('total', 0)
        except Exception as e:
            logger.error(f"Failed to get entries count: {e}")
            return 0

    def _html_to_markdown(self, html_content: str) -> str:
        """
        Convert HTML content to Markdown.

        Args:
            html_content: HTML string.

        Returns:
            Markdown string.
        """
        h = html2text.HTML2Text()

        # Apply markdown options from config
        markdown_options = self.config['markdown_options']
        for key, value in markdown_options.items():
            if hasattr(h, key):
                setattr(h, key, value)

        return h.handle(html_content)

    def _save_entry(self, entry: Dict[str, Any]) -> bool:
        """
        Save a single entry to file.

        Args:
            entry: Entry dictionary from Miniflux.

        Returns:
            True if saved successfully, False otherwise.
        """
        try:
            # Determine save path
            save_dir = get_save_path(
                entry,
                self.config['output_dir'],
                self.config['organize_by_feed'],
                self.config['organize_by_category']
            )
            save_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename
            filename = format_filename(entry, self.config['filename_format']) + '.md'
            filepath = save_dir / filename

            # Check if file already exists
            if filepath.exists():
                logger.debug(f"Skipping existing file: {filepath}")
                self.stats['skipped'] += 1
                return True

            # Convert content
            content_html = entry.get('content', '')
            content_md = self._html_to_markdown(content_html)

            # Build full markdown content
            if self.config['include_metadata']:
                full_content = create_markdown_frontmatter(entry) + content_md
            else:
                title = entry.get('title', 'Untitled')
                full_content = f"# {title}\n\n{content_md}"

            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            logger.debug(f"Saved entry {entry.get('id')} to {filepath}")
            self.stats['saved'] += 1
            return True

        except Exception as e:
            logger.error(f"Failed to save entry {entry.get('id')}: {e}")
            self.stats['failed'] += 1
            return False

    def _collect_metadata(self, entry: Dict[str, Any], filepath: Path) -> Dict[str, Any]:
        """
        Collect metadata for an entry.

        Args:
            entry: Entry dictionary.
            filepath: Path where entry was saved.

        Returns:
            Metadata dictionary.
        """
        return {
            'id': entry.get('id'),
            'title': entry.get('title'),
            'author': entry.get('author'),
            'url': entry.get('url'),
            'published_at': entry.get('published_at'),
            'feed': entry.get('feed', {}).get('title'),
            'feed_id': entry.get('feed_id'),
            'category': entry.get('feed', {}).get('category', {}).get('title'),
            'status': entry.get('status'),
            'starred': entry.get('starred'),
            'reading_time': entry.get('reading_time'),
            'saved_path': str(filepath.relative_to(self.config['output_dir']))
        }

    def export(self, progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Export all entries matching configured filters.

        Args:
            progress_callback: Optional callback function(current, total, entry).

        Returns:
            Dictionary with export statistics.
        """
        if not self.client:
            raise RuntimeError("Not connected to Miniflux. Call connect() first.")

        # Reset stats
        self.stats = {
            'total': 0,
            'saved': 0,
            'failed': 0,
            'skipped': 0
        }

        # Create output directory
        output_path = Path(self.config['output_dir'])
        output_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {output_path.absolute()}")

        # Build query parameters
        query_params = {
            'limit': self.config['batch_size'],
            'offset': 0,
            'direction': 'desc',
            'order': 'published_at'
        }

        # Add filters
        if self.config['filter_status']:
            query_params['status'] = self.config['filter_status']

        if self.config['filter_starred'] is not None:
            query_params['starred'] = self.config['filter_starred']

        logger.info(f"Filters: status={self.config['filter_status'] or 'all'}, "
                   f"starred={self.config['filter_starred'] if self.config['filter_starred'] is not None else 'all'}")

        # Metadata collection
        all_metadata = []

        # Start export
        start_time = datetime.now()
        logger.info("Starting export...")

        try:
            while True:
                # Fetch entries
                result = self.client.get_entries(**query_params)
                entries = result.get('entries', [])

                if not entries:
                    break

                total = result.get('total', 0)

                # Process each entry
                for entry in entries:
                    self.stats['total'] += 1

                    # Save entry
                    success = self._save_entry(entry)

                    # Collect metadata if needed
                    if success and self.config['save_json_metadata']:
                        save_dir = get_save_path(
                            entry,
                            self.config['output_dir'],
                            self.config['organize_by_feed'],
                            self.config['organize_by_category']
                        )
                        filename = format_filename(entry, self.config['filename_format']) + '.md'
                        filepath = save_dir / filename

                        metadata = self._collect_metadata(entry, filepath)
                        all_metadata.append(metadata)

                    # Progress callback
                    if progress_callback:
                        progress_callback(self.stats['total'], total, entry)
                    else:
                        # Default progress display
                        feed_name = entry.get('feed', {}).get('title', '')[:20]
                        print_progress_bar(
                            self.stats['total'],
                            total,
                            prefix='Progress:',
                            suffix=f'[{feed_name}]'
                        )

                # Update offset
                query_params['offset'] += self.config['batch_size']

                # Check if we've processed all entries
                if query_params['offset'] >= total:
                    break

        except KeyboardInterrupt:
            logger.warning("Export interrupted by user")
        except Exception as e:
            logger.error(f"Error during export: {e}")

        # Save metadata JSON
        if self.config['save_json_metadata'] and all_metadata:
            metadata_file = output_path / 'articles_metadata.json'
            try:
                with open(metadata_file, 'w', encoding='utf-8') as f:
                    json.dump(all_metadata, f, ensure_ascii=False, indent=2)
                logger.info(f"Metadata saved to: {metadata_file.name}")
            except Exception as e:
                logger.error(f"Failed to save metadata: {e}")

        # Calculate statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Calculate output size
        total_size = sum(f.stat().st_size for f in output_path.rglob('*.md'))

        results = {
            **self.stats,
            'duration': duration,
            'output_size': total_size,
            'output_size_formatted': format_bytes(total_size),
            'output_dir': str(output_path.absolute())
        }

        logger.info(f"Export completed in {duration:.1f} seconds")
        logger.info(f"Total: {self.stats['total']}, "
                   f"Saved: {self.stats['saved']}, "
                   f"Skipped: {self.stats['skipped']}, "
                   f"Failed: {self.stats['failed']}")

        return results

    def test_connection(self) -> Dict[str, Any]:
        """
        Test connection and return basic information.

        Returns:
            Dictionary with connection test results.
        """
        if not self.connect():
            return {
                'success': False,
                'error': 'Failed to connect to Miniflux'
            }

        try:
            user = self.client.me()
            feeds_info = self.get_feeds_info()
            entries_count = self.get_entries_count()

            filters = {}
            if self.config['filter_status']:
                filters['status'] = self.config['filter_status']
            if self.config['filter_starred'] is not None:
                filters['starred'] = self.config['filter_starred']

            filtered_count = self.get_entries_count(**filters) if filters else entries_count

            return {
                'success': True,
                'user': {
                    'username': user.get('username'),
                    'id': user.get('id'),
                    'is_admin': user.get('is_admin')
                },
                'feeds_count': feeds_info['feeds_count'],
                'categories_count': feeds_info['categories_count'],
                'total_entries': entries_count,
                'filtered_entries': filtered_count
            }

        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
