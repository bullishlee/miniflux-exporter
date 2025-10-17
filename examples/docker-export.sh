#!/bin/bash
# Miniflux Exporter - Docker 导出示例脚本

# 配置你的 Miniflux 信息
MINIFLUX_URL="https://miniflux.example.com"
MINIFLUX_API_KEY="your_api_key_here"

# 输出目录
OUTPUT_DIR="./miniflux_articles"

# Docker 镜像名称
IMAGE_NAME="miniflux-exporter:test"

echo "=========================================="
echo "Miniflux 文章导出工具"
echo "=========================================="
echo ""

# 选择操作
echo "请选择操作："
echo "1. 测试连接"
echo "2. 导出所有文章"
echo "3. 导出未读文章"
echo "4. 导出星标文章"
echo ""
read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "正在测试连接..."
        docker run --rm \
            -e MINIFLUX_URL="$MINIFLUX_URL" \
            -e MINIFLUX_API_KEY="$MINIFLUX_API_KEY" \
            $IMAGE_NAME \
            --test
        ;;

    2)
        echo ""
        echo "正在导出所有文章到: $OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"
        docker run --rm \
            -v "$(pwd)/$OUTPUT_DIR:/output" \
            -e MINIFLUX_URL="$MINIFLUX_URL" \
            -e MINIFLUX_API_KEY="$MINIFLUX_API_KEY" \
            $IMAGE_NAME \
            --url "$MINIFLUX_URL" \
            --api-key "$MINIFLUX_API_KEY" \
            --output /output \
            --organize-by-feed

        echo ""
        echo "导出完成！"
        echo "文章保存在: $OUTPUT_DIR"
        echo "文章数量: $(find "$OUTPUT_DIR" -name "*.md" | wc -l)"
        ;;

    3)
        echo ""
        echo "正在导出未读文章到: $OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"
        docker run --rm \
            -v "$(pwd)/$OUTPUT_DIR:/output" \
            -e MINIFLUX_URL="$MINIFLUX_URL" \
            -e MINIFLUX_API_KEY="$MINIFLUX_API_KEY" \
            $IMAGE_NAME \
            --url "$MINIFLUX_URL" \
            --api-key "$MINIFLUX_API_KEY" \
            --output /output \
            --status unread \
            --organize-by-feed

        echo ""
        echo "导出完成！"
        echo "文章保存在: $OUTPUT_DIR"
        ;;

    4)
        echo ""
        echo "正在导出星标文章到: $OUTPUT_DIR"
        mkdir -p "$OUTPUT_DIR"
        docker run --rm \
            -v "$(pwd)/$OUTPUT_DIR:/output" \
            -e MINIFLUX_URL="$MINIFLUX_URL" \
            -e MINIFLUX_API_KEY="$MINIFLUX_API_KEY" \
            $IMAGE_NAME \
            --url "$MINIFLUX_URL" \
            --api-key "$MINIFLUX_API_KEY" \
            --output /output \
            --starred \
            --organize-by-feed

        echo ""
        echo "导出完成！"
        echo "文章保存在: $OUTPUT_DIR"
        ;;

    *)
        echo "无效选项"
        exit 1
        ;;
esac

echo ""
