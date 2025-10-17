#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point when running as a module.

This allows the package to be run with:
    python -m miniflux_exporter
"""

from .cli import main

if __name__ == '__main__':
    raise SystemExit(main())
