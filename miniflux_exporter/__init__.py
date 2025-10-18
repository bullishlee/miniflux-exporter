"""
Miniflux Exporter
~~~~~~~~~~~~~~~~~

Export your Miniflux articles to Markdown format.

:copyright: (c) 2024 by Miniflux Exporter Contributors.
:license: MIT, see LICENSE for more details.
"""

__version__ = "1.0.0"
__author__ = "Miniflux Exporter Contributors"
__license__ = "MIT"

from .config import Config
from .exporter import MinifluxExporter

__all__ = ["MinifluxExporter", "Config", "__version__"]
