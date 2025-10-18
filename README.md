# Miniflux Exporter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/miniflux-exporter.svg)](https://badge.fury.io/py/miniflux-exporter)

Export your [Miniflux](https://miniflux.app/) articles to Markdown format with full metadata preservation.

[English](README.md) | [中文](README_CN.md)

## ✨ Features

- 📄 **Export to Markdown**: Convert all your Miniflux articles to clean Markdown format
- 🗂️ **Flexible Organization**: Organize by feed, category, or keep all in one place
- 🔍 **Smart Filtering**: Export all articles, only unread, starred, or custom filters
- 📊 **Metadata Preservation**: Keep all article metadata (author, date, tags, etc.)
- 🐳 **Docker Support**: Run in a container without installing dependencies
- 🔄 **Incremental Export**: Skip already exported articles
- 🎨 **Customizable**: Configure filename formats, organization, and more
- 📦 **Batch Processing**: Efficiently handle thousands of articles
- 🌐 **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

### Installation

```bash
pip install miniflux-exporter
```

### Basic Usage

```bash
# Interactive setup (recommended for first time)
miniflux-export --setup

# Or use command-line arguments
miniflux-export --url https://miniflux.example.com \
                --api-key YOUR_API_KEY \
                --output ./articles

# Alternative: Run as Python module (if command not found in PATH)
python -m miniflux_exporter --setup
python -m miniflux_exporter --url https://miniflux.example.com \
                            --api-key YOUR_API_KEY \
                            --output ./articles
```

### Using Configuration File

Create a `config.yaml`:

```yaml
miniflux_url: https://miniflux.example.com
api_key: your_api_key_here
output_dir: miniflux_articles
organize_by_feed: true
organize_by_category: false
```

Then run:

```bash
miniflux-export --config config.yaml
```

## 📖 Documentation

### Getting Your API Key

1. Log in to your Miniflux instance
2. Go to **Settings** → **API Keys**
3. Click **Create a new API key**
4. Give it a description (e.g., "Export Tool")
5. Copy the generated key

### Command-Line Options

```
usage: miniflux-export [-h] [--version] [--config CONFIG] [--setup] [--test]
                       [--url URL] [--api-key API_KEY] [--output OUTPUT]
                       [--organize-by-feed] [--organize-by-category]
                       [--status {read,unread}] [--starred]
                       [--batch-size BATCH_SIZE] [--no-metadata] [--no-json]
                       [--quiet] [--verbose]

Export Miniflux articles to Markdown format

Optional arguments:
  -h, --help            Show this help message and exit
  --version             Show program's version number and exit
  --config CONFIG, -c CONFIG
                        Configuration file (YAML or JSON)
  --setup               Run interactive setup wizard
  --test                Test connection only (do not export)
  
Connection:
  --url URL             Miniflux instance URL
  --api-key API_KEY     Miniflux API key
  
Output:
  --output OUTPUT, -o OUTPUT
                        Output directory
  --organize-by-feed    Organize articles by feed
  --organize-by-category
                        Organize articles by category
  
Filters:
  --status {read,unread}
                        Filter by article status
  --starred             Export only starred articles
  
Advanced:
  --batch-size BATCH_SIZE
                        Number of articles to fetch per batch
  --no-metadata         Do not include metadata in files
  --no-json             Do not save metadata JSON file
  --quiet, -q           Suppress progress output
  --verbose, -v         Enable verbose logging
```

### Configuration File Format

#### YAML Example

```yaml
# Miniflux connection
miniflux_url: https://miniflux.example.com
api_key: your_api_key_here

# Output settings
output_dir: miniflux_articles
organize_by_feed: true
organize_by_category: false

# Filters (optional)
filter_status: null  # null, 'read', or 'unread'
filter_starred: null  # null, true, or false

# Filename format
filename_format: "{date}_{title}"  # Supports {date}, {id}, {title}

# Advanced options
batch_size: 100
include_metadata: true
save_json_metadata: true

# Markdown conversion options
markdown_options:
  ignore_links: false
  ignore_images: false
  body_width: 0
  skip_internal_links: false
```

#### JSON Example

```json
{
  "miniflux_url": "https://miniflux.example.com",
  "api_key": "your_api_key_here",
  "output_dir": "miniflux_articles",
  "organize_by_feed": true,
  "organize_by_category": false,
  "filter_status": null,
  "filter_starred": null,
  "filename_format": "{date}_{title}",
  "batch_size": 100,
  "include_metadata": true,
  "save_json_metadata": true
}
```

## 📂 Output Structure

### Organized by Feed

```
miniflux_articles/
├── articles_metadata.json
├── TechCrunch/
│   ├── 2024-01-15_Article_Title_1.md
│   └── 2024-01-16_Article_Title_2.md
├── Hacker_News/
│   ├── 2024-01-15_Article_Title_3.md
│   └── 2024-01-17_Article_Title_4.md
└── Blog_Name/
    └── 2024-01-18_Article_Title_5.md
```

### Organized by Category + Feed

```
miniflux_articles/
├── articles_metadata.json
├── Technology/
│   ├── TechCrunch/
│   │   └── 2024-01-15_Article_Title_1.md
│   └── Hacker_News/
│       └── 2024-01-15_Article_Title_2.md
└── Programming/
    └── Blog_Name/
        └── 2024-01-18_Article_Title_3.md
```

### Markdown File Format

Each exported file contains:

```markdown
---
title: "Article Title"
author: "Author Name"
feed: "Feed Name"
category: "Category Name"
url: "https://example.com/article"
published_at: "2024-01-15T10:30:00Z"
created_at: "2024-01-15T11:00:00Z"
status: "read"
starred: false
reading_time: 5
entry_id: 12345
feed_id: 67
---

# Article Title

Article content in Markdown format...

## Section

Content here...
```

## 🐳 Docker Usage

### Using Docker Hub Image

```bash
docker run -v $(pwd)/articles:/output \
           -e MINIFLUX_URL=https://miniflux.example.com \
           -e MINIFLUX_API_KEY=your_api_key \
           fisherpensieve/miniflux-exporter
```

### Using Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  miniflux-exporter:
    image: fisherpensieve/miniflux-exporter
    volumes:
      - ./articles:/output
    environment:
      - MINIFLUX_URL=https://miniflux.example.com
      - MINIFLUX_API_KEY=your_api_key
      - MINIFLUX_OUTPUT_DIR=/output
```

Then run:

```bash
docker-compose up
```

### Building from Source

```bash
cd docker
docker build -t miniflux-exporter .
```

## 💡 Use Cases

### Backup Your Articles

```bash
# Export all articles for backup
miniflux-export --config config.yaml
```

### Export Reading List

```bash
# Export only unread articles
miniflux-export --config config.yaml --status unread
```

### Archive Starred Articles

```bash
# Export only starred articles
miniflux-export --config config.yaml --starred
```

### Migrate to Another Platform

```bash
# Export everything with metadata
miniflux-export --config config.yaml --output ./export
```

### Integration with Other Tools

Export articles and:
- Import to **Obsidian** for knowledge management
- Import to **Notion** for note-taking
- Generate a static site with **Hugo** or **Jekyll**
- Analyze with custom scripts using the JSON metadata

## 🔧 Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/bullishlee/miniflux-exporter.git
cd miniflux-exporter

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .
```

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format code
black miniflux_exporter/

# Lint code
flake8 miniflux_exporter/
pylint miniflux_exporter/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Miniflux](https://miniflux.app/) - A minimalist and opinionated feed reader
- [html2text](https://github.com/Alir3z4/html2text) - Convert HTML to Markdown
- [Python Miniflux Client](https://github.com/miniflux/python-client) - Official Python client

## 📞 Support

- 📖 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/bullishlee/miniflux-exporter/issues)
- 💬 [Discussions](https://github.com/bullishlee/miniflux-exporter/discussions)

## 📈 Roadmap

- [ ] Web UI for easier configuration and monitoring
- [ ] Support for exporting to other formats (PDF, EPUB, HTML)
- [ ] Integration with cloud storage services
- [ ] Advanced filtering and search capabilities
- [ ] Scheduling and automation features
- [ ] Plugin system for custom processors

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=bullishlee/miniflux-exporter&type=Date)](https://star-history.com/#bullishlee/miniflux-exporter&Date)

---

Made with ❤️ by the Miniflux Exporter community