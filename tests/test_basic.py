"""
Basic tests for Miniflux Exporter.
"""

import pytest

from miniflux_exporter import __version__
from miniflux_exporter.config import Config
from miniflux_exporter.utils import format_bytes, sanitize_filename


def test_version():
    """Test that version is defined."""
    assert __version__
    assert isinstance(__version__, str)
    assert len(__version__.split('.')) >= 2


def test_config_defaults():
    """Test Config default values."""
    config = Config()
    assert config['output_dir'] == 'miniflux_articles'
    assert config['organize_by_feed'] is True
    assert config['batch_size'] == 100


def test_config_validation_missing_url():
    """Test config validation with missing URL."""
    config = Config()
    with pytest.raises(ValueError, match="miniflux_url is required"):
        config.validate()


def test_config_validation_missing_api_key():
    """Test config validation with missing API key."""
    config = Config({'miniflux_url': 'https://example.com'})
    with pytest.raises(ValueError, match="api_key is required"):
        config.validate()


def test_config_validation_success():
    """Test successful config validation."""
    config = Config({
        'miniflux_url': 'https://example.com',
        'api_key': 'test_key'
    })
    assert config.validate() is True


def test_sanitize_filename():
    """Test filename sanitization."""
    # Test basic sanitization
    assert sanitize_filename('hello world') == 'hello world'

    # Test illegal characters
    assert sanitize_filename('hello/world') == 'hello_world'
    assert sanitize_filename('hello:world') == 'hello_world'
    assert sanitize_filename('hello*world') == 'hello_world'
    assert sanitize_filename('hello?world') == 'hello_world'
    assert sanitize_filename('hello"world') == 'hello_world'
    assert sanitize_filename('hello<world>') == 'hello_world'
    assert sanitize_filename('hello|world') == 'hello_world'

    # Test multiple underscores
    assert sanitize_filename('hello___world') == 'hello_world'

    # Test empty string
    assert sanitize_filename('') == 'untitled'

    # Test length limit
    long_name = 'a' * 300
    result = sanitize_filename(long_name, max_length=200)
    assert len(result) == 200


def test_format_bytes():
    """Test byte formatting."""
    assert format_bytes(0) == '0.0 B'
    assert format_bytes(1023) == '1023.0 B'
    assert format_bytes(1024) == '1.0 KB'
    assert format_bytes(1024 * 1024) == '1.0 MB'
    assert format_bytes(1024 * 1024 * 1024) == '1.0 GB'
    assert format_bytes(1536) == '1.5 KB'  # 1.5 KB


def test_config_from_dict():
    """Test creating config from dictionary."""
    config_dict = {
        'miniflux_url': 'https://example.com',
        'api_key': 'test_key',
        'output_dir': 'custom_dir',
        'batch_size': 50
    }
    config = Config(config_dict)
    assert config['miniflux_url'] == 'https://example.com'
    assert config['api_key'] == 'test_key'
    assert config['output_dir'] == 'custom_dir'
    assert config['batch_size'] == 50


def test_config_update():
    """Test updating config."""
    config = Config()
    config.update({
        'miniflux_url': 'https://example.com',
        'batch_size': 200
    })
    assert config['miniflux_url'] == 'https://example.com'
    assert config['batch_size'] == 200
    # Default values should still exist
    assert config['output_dir'] == 'miniflux_articles'


def test_markdown_options():
    """Test markdown options in config."""
    config = Config()
    assert config['markdown_options']['ignore_links'] is False
    assert config['markdown_options']['ignore_images'] is False
    assert config['markdown_options']['body_width'] == 0


def test_config_url_validation():
    """Test URL validation."""
    # Invalid URL (no http/https)
    config = Config({
        'miniflux_url': 'example.com',
        'api_key': 'test'
    })
    with pytest.raises(ValueError, match="must start with http"):
        config.validate()

    # Valid URL
    config = Config({
        'miniflux_url': 'https://example.com',
        'api_key': 'test'
    })
    assert config.validate() is True


def test_config_removes_v1_suffix():
    """Test that /v1/ suffix is removed from URL."""
    config = Config({
        'miniflux_url': 'https://example.com/v1/',
        'api_key': 'test'
    })
    config.validate()
    assert config['miniflux_url'] == 'https://example.com'

    config = Config({
        'miniflux_url': 'https://example.com/v1',
        'api_key': 'test'
    })
    config.validate()
    assert config['miniflux_url'] == 'https://example.com'


def test_config_status_filter_validation():
    """Test status filter validation."""
    # Invalid status
    config = Config({
        'miniflux_url': 'https://example.com',
        'api_key': 'test',
        'filter_status': 'invalid'
    })
    with pytest.raises(ValueError, match="filter_status must be one of"):
        config.validate()

    # Valid status
    for status in ['read', 'unread', 'removed']:
        config = Config({
            'miniflux_url': 'https://example.com',
            'api_key': 'test',
            'filter_status': status
        })
        assert config.validate() is True


def test_config_batch_size_validation():
    """Test batch size validation."""
    # Too small
    config = Config({
        'miniflux_url': 'https://example.com',
        'api_key': 'test',
        'batch_size': 0
    })
    with pytest.raises(ValueError, match="batch_size must be between"):
        config.validate()

    # Too large
    config = Config({
        'miniflux_url': 'https://example.com',
        'api_key': 'test',
        'batch_size': 2000
    })
    with pytest.raises(ValueError, match="batch_size must be between"):
        config.validate()

    # Valid
    config = Config({
        'miniflux_url': 'https://example.com',
        'api_key': 'test',
        'batch_size': 100
    })
    assert config.validate() is True
