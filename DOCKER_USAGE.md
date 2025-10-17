# Docker 使用快速指南

本指南帮助您快速使用 Docker 运行 Miniflux Exporter。

## 🚀 快速开始

### 1. 测试连接

```bash
docker run --rm \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --test
```

### 2. 导出所有文章

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --url https://miniflux.example.com \
  --api-key your_api_key_here \
  --output /output \
  --organize-by-feed
```

### 3. 导出未读文章

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --url https://miniflux.example.com \
  --api-key your_api_key_here \
  --output /output \
  --status unread \
  --organize-by-feed
```

### 4. 导出星标文章

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --url https://miniflux.example.com \
  --api-key your_api_key_here \
  --output /output \
  --starred \
  --organize-by-feed
```

---

## 📋 使用 Docker Compose

### 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  miniflux-exporter:
    image: miniflux-exporter:latest
    volumes:
      - ./articles:/output
    environment:
      - MINIFLUX_URL=https://miniflux.example.com
      - MINIFLUX_API_KEY=your_api_key_here
    command: >
      --url https://miniflux.example.com
      --api-key your_api_key_here
      --output /output
      --organize-by-feed
```

### 运行

```bash
# 导出文章
docker-compose up

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f
```

---

## 🔧 高级用法

### 使用配置文件

创建 `config.yaml`:

```yaml
miniflux_url: https://miniflux.example.com
api_key: your_api_key_here
output_dir: /output
organize_by_feed: true
organize_by_category: false
```

运行:

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  -v $(pwd)/config.yaml:/app/config.yaml:ro \
  miniflux-exporter:latest \
  --config /app/config.yaml
```

### 按分类和订阅源组织

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --url https://miniflux.example.com \
  --api-key your_api_key_here \
  --output /output \
  --organize-by-feed \
  --organize-by-category
```

### 静默模式（无进度输出）

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --url https://miniflux.example.com \
  --api-key your_api_key_here \
  --output /output \
  --quiet
```

---

## 🛠️ 构建自己的镜像

### 从源码构建

```bash
# 克隆仓库
git clone https://github.com/bullishlee/miniflux-exporter.git
cd miniflux-exporter

# 构建镜像
docker build -t miniflux-exporter:latest .

# 或使用 docker/ 目录的 Dockerfile
docker build -f docker/Dockerfile -t miniflux-exporter:latest .
```

### 多平台构建

```bash
# 创建 buildx 构建器
docker buildx create --name multiplatform --use

# 构建多平台镜像
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t miniflux-exporter:latest \
  --load \
  .
```

---

## 📊 查看结果

```bash
# 进入输出目录
cd articles

# 查看目录结构
tree -L 2

# 统计文章数量
find . -name "*.md" | wc -l

# 查看元数据
cat articles_metadata.json | jq .

# 搜索特定内容
grep -r "关键词" .
```

---

## 🔄 定时导出

### 使用 cron（Linux/macOS）

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天凌晨 2 点执行）
0 2 * * * cd /path/to/project && docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --url https://miniflux.example.com \
  --api-key your_api_key_here \
  --output /output
```

### 使用脚本

创建 `backup.sh`:

```bash
#!/bin/bash
cd /path/to/project

# 创建带日期的目录
DATE=$(date +%Y%m%d)
OUTPUT_DIR="./backup/$DATE"
mkdir -p "$OUTPUT_DIR"

# 运行导出
docker run --rm \
  -v "$(pwd)/backup/$DATE:/output" \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --url https://miniflux.example.com \
  --api-key your_api_key_here \
  --output /output \
  --organize-by-feed

echo "备份完成：$OUTPUT_DIR"
```

设置执行权限:

```bash
chmod +x backup.sh
```

---

## 💡 使用技巧

### 1. 保存命令为别名

在 `~/.bashrc` 或 `~/.zshrc` 中添加:

```bash
alias miniflux-export='docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest'
```

使用:

```bash
miniflux-export --test
miniflux-export --output /output --organize-by-feed
```

### 2. 使用 .env 文件

创建 `.env`:

```bash
MINIFLUX_URL=https://miniflux.example.com
MINIFLUX_API_KEY=your_api_key_here
```

使用:

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  --env-file .env \
  miniflux-exporter:latest \
  --output /output
```

### 3. 增量导出

脚本会自动跳过已存在的文件，所以可以定期运行相同命令进行增量导出。

---

## ❓ 常见问题

### Q: 权限问题

如果遇到权限错误:

```bash
# 修改输出目录权限
chmod -R 755 articles/

# 或以当前用户身份运行
docker run --rm \
  -v $(pwd)/articles:/output \
  -u $(id -u):$(id -g) \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  miniflux-exporter:latest \
  --output /output
```

### Q: 中文文件名乱码

确保使用 UTF-8 编码:

```bash
docker run --rm \
  -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://miniflux.example.com \
  -e MINIFLUX_API_KEY=your_api_key_here \
  -e LANG=C.UTF-8 \
  miniflux-exporter:latest \
  --output /output
```

### Q: 镜像拉取慢

使用国内镜像加速器，或本地构建:

```bash
# 本地构建
docker build -t miniflux-exporter:latest .
```

---

## 🧹 清理

### 清理输出目录

```bash
rm -rf articles/
```

### 清理 Docker 镜像

```bash
# 删除镜像
docker rmi miniflux-exporter:latest

# 清理未使用的镜像
docker image prune -a
```

### 清理 Docker 构建缓存

```bash
docker builder prune -f
```

---

## 📚 更多信息

- 完整文档：`README.md`
- 配置选项：`examples/config.example.yaml`
- Python API：直接使用 `pip install miniflux-exporter`

---

**提示**: 不要将包含真实 API 密钥的脚本提交到版本控制系统！