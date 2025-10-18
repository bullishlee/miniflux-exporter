#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command-line interface for Miniflux Exporter.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .config import Config
from .exporter import MinifluxExporter


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration.

    Args:
        verbose: Enable verbose logging.
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def print_banner() -> None:
    """Print application banner."""
    print("=" * 60)
    print(f"Miniflux Exporter v{__version__}")
    print("Export your Miniflux articles to Markdown format")
    print("=" * 60)
    print()


def test_connection(config: Config) -> int:
    """
    Test connection to Miniflux.

    Args:
        config: Configuration object.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print("Testing connection to Miniflux...")
    print(f"URL: {config['miniflux_url']}")
    print()

    exporter = MinifluxExporter(config)
    result = exporter.test_connection()

    if not result['success']:
        print(f"✗ Connection failed: {result.get('error', 'Unknown error')}")
        print()
        print("Troubleshooting:")
        print("  1. Check if MINIFLUX_URL is correct (don't include /v1/ suffix)")
        print("  2. Verify API_KEY is valid")
        print("  3. Ensure network connectivity")
        return 1

    print("✓ Connection successful!")
    print()
    print("User Information:")
    print(f"  Username: {result['user']['username']}")
    print(f"  User ID: {result['user']['id']}")
    print(f"  Admin: {'Yes' if result['user']['is_admin'] else 'No'}")
    print()
    print("Statistics:")
    print(f"  Feeds: {result['feeds_count']}")
    print(f"  Categories: {result['categories_count']}")
    print(f"  Total Entries: {result['total_entries']}")

    if result['filtered_entries'] != result['total_entries']:
        print(f"  Filtered Entries: {result['filtered_entries']}")

    print()
    return 0


def run_export(config: Config, quiet: bool = False) -> int:
    """
    Run the export process.

    Args:
        config: Configuration object.
        quiet: Suppress progress output.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    if not quiet:
        print_banner()
        print("Configuration:")
        print(f"  URL: {config['miniflux_url']}")
        print(f"  Output: {config['output_dir']}")
        print(f"  Organize by feed: {config['organize_by_feed']}")
        print(f"  Organize by category: {config['organize_by_category']}")

        if config['filter_status']:
            print(f"  Filter status: {config['filter_status']}")
        if config['filter_starred'] is not None:
            print(f"  Filter starred: {config['filter_starred']}")

        print()

    exporter = MinifluxExporter(config)

    # Connect to Miniflux
    if not quiet:
        print("Connecting to Miniflux...")

    if not exporter.connect():
        print("✗ Failed to connect to Miniflux")
        return 1

    if not quiet:
        print("✓ Connected successfully")
        print()
        print("Starting export...")
        print()

    # Run export
    try:
        results = exporter.export()

        if not quiet:
            print()
            print("=" * 60)
            print("Export Complete!")
            print("=" * 60)
            print(f"✓ Successfully saved: {results['saved']} articles")

            if results['skipped'] > 0:
                print(f"⊘ Skipped (already exists): {results['skipped']} articles")

            if results['failed'] > 0:
                print(f"✗ Failed: {results['failed']} articles")

            print(f"⏱  Duration: {results['duration']:.1f} seconds")
            print(f"💾 Output size: {results['output_size_formatted']}")
            print(f"📁 Location: {results['output_dir']}")
            print("=" * 60)

        return 0

    except KeyboardInterrupt:
        print("\n\nExport interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n✗ Error during export: {e}")
        logging.exception("Export failed")
        return 1


def interactive_setup() -> Optional[Config]:
    """
    Interactive setup wizard.

    Returns:
        Configured Config object, or None if cancelled.
    """
    print_banner()
    print("Interactive Setup Wizard")
    print()
    print("Press Ctrl+C at any time to cancel.")
    print()

    try:
        # Miniflux URL
        print("[1/5] Miniflux Configuration")
        print("-" * 60)
        url = input("Miniflux URL (e.g., https://miniflux.example.com): ").strip()
        if not url:
            print("Error: URL is required")
            return None

        # API Key
        api_key = input("API Key: ").strip()
        if not api_key:
            print("Error: API Key is required")
            return None

        print()

        # Output directory
        print("[2/5] Output Configuration")
        print("-" * 60)
        output_dir = input("Output directory [miniflux_articles]: ").strip()
        if not output_dir:
            output_dir = "miniflux_articles"

        print()

        # Organization
        print("[3/5] File Organization")
        print("-" * 60)
        print("1. Organize by feed")
        print("2. Organize by category + feed")
        print("3. All in one directory")
        org_choice = input("Choose organization [1]: ").strip() or "1"

        organize_by_feed = org_choice != "3"
        organize_by_category = org_choice == "2"

        print()

        # Filters
        print("[4/5] Filters")
        print("-" * 60)
        print("1. All articles")
        print("2. Unread only")
        print("3. Read only")
        print("4. Starred only")
        filter_choice = input("Choose filter [1]: ").strip() or "1"

        filter_status = None
        filter_starred = None

        if filter_choice == "2":
            filter_status = "unread"
        elif filter_choice == "3":
            filter_status = "read"
        elif filter_choice == "4":
            filter_starred = True

        print()

        # Advanced options
        print("[5/5] Advanced Options")
        print("-" * 60)
        include_metadata = input("Include metadata in files? [Y/n]: ").strip().lower() != 'n'
        save_json = input("Save metadata JSON file? [Y/n]: ").strip().lower() != 'n'

        print()

        # Create config
        config = Config({
            'miniflux_url': url,
            'api_key': api_key,
            'output_dir': output_dir,
            'organize_by_feed': organize_by_feed,
            'organize_by_category': organize_by_category,
            'filter_status': filter_status,
            'filter_starred': filter_starred,
            'include_metadata': include_metadata,
            'save_json_metadata': save_json
        })

        # Test connection
        print("Testing connection...")
        exporter = MinifluxExporter(config)
        result = exporter.test_connection()

        if not result['success']:
            print(f"✗ Connection test failed: {result.get('error', 'Unknown error')}")
            retry = input("Continue anyway? [y/N]: ").strip().lower()
            if retry != 'y':
                return None
        else:
            print(f"✓ Connected successfully as {result['user']['username']}")
            print(f"  Found {result['total_entries']} articles")

        print()

        # Offer to save config
        save_config = input("Save configuration to file? [y/N]: ").strip().lower()
        if save_config == 'y':
            config_file = input("Config file path [config.yaml]: ").strip() or "config.yaml"
            config.to_file(config_file)
            print(f"✓ Configuration saved to {config_file}")

        print()
        return config

    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        return None
    except Exception as e:
        print(f"\nError during setup: {e}")
        return None


def main() -> int:
    """
    Main entry point for CLI.

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(
        description='Export Miniflux articles to Markdown format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive setup
  miniflux-export --setup

  # Use config file
  miniflux-export --config config.yaml

  # Quick export with parameters
  miniflux-export --url https://miniflux.example.com --api-key YOUR_KEY

  # Test connection only
  miniflux-export --config config.yaml --test

  # Export with filters
  miniflux-export --config config.yaml --status unread --starred

For more information, visit: https://github.com/bullishlee/miniflux-exporter
        """
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'miniflux-exporter {__version__}'
    )

    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Configuration file (YAML or JSON)'
    )

    parser.add_argument(
        '--setup',
        action='store_true',
        help='Run interactive setup wizard'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='Test connection only (do not export)'
    )

    # Miniflux connection
    parser.add_argument(
        '--url',
        type=str,
        help='Miniflux instance URL'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Miniflux API key'
    )

    # Output options
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output directory'
    )

    parser.add_argument(
        '--organize-by-feed',
        action='store_true',
        help='Organize articles by feed'
    )

    parser.add_argument(
        '--organize-by-category',
        action='store_true',
        help='Organize articles by category'
    )

    # Filters
    parser.add_argument(
        '--status',
        type=str,
        choices=['read', 'unread'],
        help='Filter by article status'
    )

    parser.add_argument(
        '--starred',
        action='store_true',
        help='Export only starred articles'
    )

    # Other options
    parser.add_argument(
        '--batch-size',
        type=int,
        help='Number of articles to fetch per batch'
    )

    parser.add_argument(
        '--no-metadata',
        action='store_true',
        help='Do not include metadata in files'
    )

    parser.add_argument(
        '--no-json',
        action='store_true',
        help='Do not save metadata JSON file'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress progress output'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Interactive setup
    if args.setup:
        config = interactive_setup()
        if not config:
            return 1

        # Ask if user wants to run export now
        run_now = input("Run export now? [Y/n]: ").strip().lower() != 'n'
        if not run_now:
            print("Setup complete. Run 'miniflux-export' to start export.")
            return 0

        return run_export(config, args.quiet)

    # Load or create config
    if args.config:
        try:
            config = Config.from_file(args.config)
        except Exception as e:
            print(f"Error loading config file: {e}")
            return 1
    else:
        # Create config from command-line arguments
        config_dict = {}

        if args.url:
            config_dict['miniflux_url'] = args.url
        if args.api_key:
            config_dict['api_key'] = args.api_key
        if args.output:
            config_dict['output_dir'] = args.output
        if args.organize_by_feed:
            config_dict['organize_by_feed'] = True
        if args.organize_by_category:
            config_dict['organize_by_category'] = True
        if args.status:
            config_dict['filter_status'] = args.status
        if args.starred:
            config_dict['filter_starred'] = True
        if args.batch_size:
            config_dict['batch_size'] = args.batch_size
        if args.no_metadata:
            config_dict['include_metadata'] = False
        if args.no_json:
            config_dict['save_json_metadata'] = False

        config = Config(config_dict)

    # Validate config
    try:
        config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print()
        print("Run 'miniflux-export --setup' for interactive configuration")
        return 1

    # Test connection only
    if args.test:
        return test_connection(config)

    # Run export
    return run_export(config, args.quiet)


if __name__ == '__main__':
    sys.exit(main())
