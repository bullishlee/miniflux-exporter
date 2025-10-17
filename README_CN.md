# Miniflux Exporter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/miniflux-exporter.svg)](https://badge.fury.io/py/miniflux-exporter)

将您的 [Miniflux](https://miniflux.app/) 文章导出为 Markdown 格式，完整保留元数据。

[English](README.md) | [中文](README_CN.md)

## ✨ 特性

- 📄 **导出为 Markdown**：将所有 Miniflux 文章转换为简洁的 Markdown 格式
- 🗂️ **灵活的组织方式**：按订阅源、分类组织，或保存在同一目录
- 🔍 **智能过滤**：导出全部文章、仅未读、星标文章或自定义过滤
- 📊 **元数据保留**：保留所有文章元数据（作者、日期、标签等）
- 🐳 **Docker 支持**：在容器中运行，无需安装依赖
- 🔄 **增量导出**：跳过已导出的文章
- 🎨 **可自定义**：配置文件名格式、组织方式等
- 📦 **批量处理**：高效处理数千篇文章
- 🌐 **跨平台**：支持 Windows、macOS 和 Linux

## 🚀 快速开始

### 安装

```bash
pip install miniflux-exporter
```

### 基本使用

```bash
# 交互式设置（首次使用推荐）
miniflux-export --setup

# 或使用命令行参数
miniflux-export --url https://miniflux.example.com \
                --api-key YOUR_API_KEY \
                --output ./articles
```

### 使用配置文件

创建 `config.yaml`：

```yaml
miniflux_url: https://miniflux.example.com
api_key: your_api_key_here
output_dir: miniflux_articles
organize_by_feed: true
organize_by_category: false
```

然后运行：

```bash
miniflux-export --config config.yaml
```

## 📖 文档

### 获取 API 密钥

1. 登录您的 Miniflux 实例
2. 进入 **设置** → **API Keys**
3. 点击 **Create a new API key**
4. 输入描述（例如："导出工具"）
5. 复制生成的密钥

### 命令行选项

```
用法: miniflux-export [-h] [--version] [--config CONFIG] [--setup] [--test]
                       [--url URL] [--api-key API_KEY] [--output OUTPUT]
                       [--organize-by-feed] [--organize-by-category]
                       [--status {read,unread}] [--starred]
                       [--batch-size BATCH_SIZE] [--no-metadata] [--no-json]
                       [--quiet] [--verbose]

将 Miniflux 文章导出为 Markdown 格式

可选参数:
  -h, --help            显示帮助信息并退出
  --version             显示程序版本号并退出
  --config CONFIG, -c CONFIG
                        配置文件（YAML 或 JSON）
  --setup               运行交互式设置向导
  --test                仅测试连接（不导出）
  
连接选项:
  --url URL             Miniflux 实例 URL
  --api-key API_KEY     Miniflux API 密钥
  
输出选项:
  --output OUTPUT, -o OUTPUT
                        输出目录
  --organize-by-feed    按订阅源组织文章
  --organize-by-category
                        按分类组织文章
  
过滤选项:
  --status {read,unread}
                        按文章状态过滤
  --starred             仅导出星标文章
  
高级选项:
  --batch-size BATCH_SIZE
                        每批获取的文章数量
  --no-metadata         不在文件中包含元数据
  --no-json             不保存元数据 JSON 文件
  --quiet, -q           静默模式，不显示进度
  --verbose, -v         启用详细日志
```

### 配置文件格式

#### YAML 示例

```yaml
# Miniflux 连接配置
miniflux_url: https://miniflux.example.com
api_key: your_api_key_here

# 输出设置
output_dir: miniflux_articles
organize_by_feed: true
organize_by_category: false

# 过滤器（可选）
filter_status: null  # null, 'read' 或 'unread'
filter_starred: null  # null, true 或 false

# 文件名格式
filename_format: "{date}_{title}"  # 支持 {date}, {id}, {title}

# 高级选项
batch_size: 100
include_metadata: true
save_json_metadata: true

# Markdown 转换选项
markdown_options:
  ignore_links: false
  ignore_images: false
  body_width: 0
  skip_internal_links: false
```

#### JSON 示例

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

## 📂 输出结构

### 按订阅源组织

```
miniflux_articles/
├── articles_metadata.json
├── TechCrunch/
│   ├── 2024-01-15_文章标题1.md
│   └── 2024-01-16_文章标题2.md
├── Hacker_News/
│   ├── 2024-01-15_文章标题3.md
│   └── 2024-01-17_文章标题4.md
└── 博客名称/
    └── 2024-01-18_文章标题5.md
```

### 按分类 + 订阅源组织

```
miniflux_articles/
├── articles_metadata.json
├── 科技/
│   ├── TechCrunch/
│   │   └── 2024-01-15_文章标题1.md
│   └── Hacker_News/
│       └── 2024-01-15_文章标题2.md
└── 编程/
    └── 博客名称/
        └── 2024-01-18_文章标题3.md
```

### Markdown 文件格式

每个导出的文件包含：

```markdown
---
title: "文章标题"
author: "作者名"
feed: "订阅源名称"
category: "分类名称"
url: "https://example.com/article"
published_at: "2024-01-15T10:30:00Z"
created_at: "2024-01-15T11:00:00Z"
status: "read"
starred: false
reading_time: 5
entry_id: 12345
feed_id: 67
---

# 文章标题

Markdown 格式的文章内容...

## 章节

内容在这里...
```

## 🐳 Docker 使用

### 使用 Docker Hub 镜像

```bash
docker run -v $(pwd)/articles:/output \
           -e MINIFLUX_URL=https://miniflux.example.com \
           -e MINIFLUX_API_KEY=your_api_key \
           miniflux-exporter/miniflux-exporter
```

### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  miniflux-exporter:
    image: miniflux-exporter/miniflux-exporter
    volumes:
      - ./articles:/output
    environment:
      - MINIFLUX_URL=https://miniflux.example.com
      - MINIFLUX_API_KEY=your_api_key
      - MINIFLUX_OUTPUT_DIR=/output
```

然后运行：

```bash
docker-compose up
```

### 从源码构建

```bash
cd docker
docker build -t miniflux-exporter .
```

## 💡 使用场景

### 备份文章

```bash
# 导出所有文章作为备份
miniflux-export --config config.yaml
```

### 导出阅读列表

```bash
# 仅导出未读文章
miniflux-export --config config.yaml --status unread
```

### 归档星标文章

```bash
# 仅导出星标文章
miniflux-export --config config.yaml --starred
```

### 迁移到其他平台

```bash
# 导出所有内容和元数据
miniflux-export --config config.yaml --output ./export
```

### 与其他工具集成

导出文章后可以：
- 导入到 **Obsidian** 进行知识管理
- 导入到 **Notion** 进行笔记整理
- 使用 **Hugo** 或 **Jekyll** 生成静态网站
- 使用 JSON 元数据进行自定义分析

## 🔧 开发

### 设置开发环境

```bash
# 克隆仓库
git clone https://github.com/bullishlee/miniflux-exporter.git
cd miniflux-exporter

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 以可编辑模式安装
pip install -e .
```

### 运行测试

```bash
pytest tests/
```

### 代码风格

```bash
# 格式化代码
black miniflux_exporter/

# 代码检查
flake8 miniflux_exporter/
pylint miniflux_exporter/
```

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加某个很棒的特性'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

更多详情请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Miniflux](https://miniflux.app/) - 极简主义的订阅阅读器
- [html2text](https://github.com/Alir3z4/html2text) - HTML 转 Markdown
- [Python Miniflux Client](https://github.com/miniflux/python-client) - 官方 Python 客户端

## 📞 支持

- 📖 [文档](docs/)
- 🐛 [问题追踪](https://github.com/bullishlee/miniflux-exporter/issues)
- 💬 [讨论区](https://github.com/bullishlee/miniflux-exporter/discussions)

## 📈 路线图

- [ ] Web UI，便于配置和监控
- [ ] 支持导出为其他格式（PDF、EPUB、HTML）
- [ ] 集成云存储服务
- [ ] 高级过滤和搜索功能
- [ ] 调度和自动化功能
- [ ] 自定义处理器插件系统

## ⭐ Star 历史

如果您觉得这个项目有用，请考虑给它一个 Star！

[![Star History Chart](https://api.star-history.com/svg?repos=bullishlee/miniflux-exporter&type=Date)](https://star-history.com/#bullishlee/miniflux-exporter&Date)

---

用 ❤️ 由 Miniflux Exporter 社区制作