#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration management for Miniflux Exporter.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """Configuration manager for Miniflux Exporter."""

    # Default configuration values
    DEFAULTS = {
        'miniflux_url': None,
        'api_key': None,
        'output_dir': 'miniflux_articles',
        'organize_by_feed': True,
        'organize_by_category': False,
        'filter_status': None,
        'filter_starred': None,
        'filename_format': '{date}_{title}',
        'batch_size': 100,
        'include_metadata': True,
        'save_json_metadata': True,
        'markdown_options': {
            'ignore_links': False,
            'ignore_images': False,
            'body_width': 0,
            'skip_internal_links': False,
        }
    }

    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.

        Args:
            config_dict: Dictionary containing configuration values.
        """
        self.config = self.DEFAULTS.copy()

        if config_dict:
            self.update(config_dict)

        # Load from environment variables
        self._load_from_env()

    def update(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration with provided values.

        Args:
            config_dict: Dictionary containing configuration values to update.
        """
        for key, value in config_dict.items():
            if key in self.config:
                if key == 'markdown_options' and isinstance(value, dict):
                    self.config[key].update(value)
                else:
                    self.config[key] = value

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            'MINIFLUX_URL': 'miniflux_url',
            'MINIFLUX_API_KEY': 'api_key',
            'MINIFLUX_OUTPUT_DIR': 'output_dir',
        }

        for env_key, config_key in env_mappings.items():
            value = os.environ.get(env_key)
            if value:
                self.config[config_key] = value

    @classmethod
    def from_file(cls, filepath: str) -> 'Config':
        """
        Load configuration from a file.

        Args:
            filepath: Path to configuration file (JSON or YAML).

        Returns:
            Config instance with loaded configuration.

        Raises:
            FileNotFoundError: If configuration file doesn't exist.
            ValueError: If file format is not supported.
        """
        path = Path(filepath)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")

        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix in ['.yaml', '.yml']:
                config_dict = yaml.safe_load(f)
            elif path.suffix == '.json':
                config_dict = json.load(f)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")

        return cls(config_dict)

    def to_file(self, filepath: str) -> None:
        """
        Save configuration to a file.

        Args:
            filepath: Path to save configuration file.
        """
        path = Path(filepath)

        with open(path, 'w', encoding='utf-8') as f:
            if path.suffix in ['.yaml', '.yml']:
                yaml.dump(self.config, f, default_flow_style=False)
            elif path.suffix == '.json':
                json.dump(self.config, f, indent=2)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")

    def validate(self) -> bool:
        """
        Validate configuration.

        Returns:
            True if configuration is valid.

        Raises:
            ValueError: If required configuration is missing or invalid.
        """
        if not self.config.get('miniflux_url'):
            raise ValueError("miniflux_url is required")

        if not self.config.get('api_key'):
            raise ValueError("api_key is required")

        # Validate URL format
        url = self.config['miniflux_url']
        if not url.startswith(('http://', 'https://')):
            raise ValueError("miniflux_url must start with http:// or https://")

        # Remove trailing /v1/ if present
        if url.endswith('/v1/') or url.endswith('/v1'):
            self.config['miniflux_url'] = url.rstrip('/').rsplit('/v1', 1)[0]

        # Validate filter_status
        if self.config.get('filter_status'):
            valid_statuses = ['read', 'unread', 'removed']
            if self.config['filter_status'] not in valid_statuses:
                raise ValueError(f"filter_status must be one of: {valid_statuses}")

        # Validate batch_size
        if self.config['batch_size'] < 1 or self.config['batch_size'] > 1000:
            raise ValueError("batch_size must be between 1 and 1000")

        return True

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            key: Configuration key.
            default: Default value if key doesn't exist.

        Returns:
            Configuration value or default.
        """
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dict-like access."""
        return self.config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set configuration value using dict-like access."""
        self.config[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if key exists in configuration."""
        return key in self.config

    def __repr__(self) -> str:
        """Return string representation of configuration."""
        # Hide sensitive data
        safe_config = self.config.copy()
        if safe_config.get('api_key'):
            safe_config['api_key'] = '***HIDDEN***'
        return f"Config({safe_config})"
