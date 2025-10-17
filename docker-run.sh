#!/bin/bash
# Miniflux Exporter - Docker 快速启动脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 显示使用说明
show_usage() {
    cat << EOF
Miniflux Exporter - Docker 启动脚本

用法: $0 [选项]

选项:
    --url URL               Miniflux 实例 URL (必需)
    --api-key KEY          API 密钥 (必需)
    --output DIR           输出目录 (默认: ./articles)
    --test                 仅测试连接
    --status STATUS        过滤状态: read, unread
    --starred              仅导出星标文章
    --organize-by-feed     按订阅源组织
    --organize-by-category 按分类组织
    --image IMAGE          Docker 镜像 (默认: miniflux-exporter:latest)
    --help                 显示此帮助信息

环境变量:
    MINIFLUX_URL           Miniflux 实例 URL
    MINIFLUX_API_KEY       API 密钥

示例:
    # 测试连接
    $0 --url https://miniflux.example.com --api-key YOUR_KEY --test

    # 导出所有文章
    $0 --url https://miniflux.example.com --api-key YOUR_KEY

    # 导出未读文章到指定目录
    $0 --url https://miniflux.example.com --api-key YOUR_KEY \\
       --output ./my-articles --status unread

    # 使用环境变量
    export MINIFLUX_URL=https://miniflux.example.com
    export MINIFLUX_API_KEY=your_key
    $0

EOF
}

# 默认值
OUTPUT_DIR="./articles"
IMAGE="miniflux-exporter:latest"
MINIFLUX_URL="${MINIFLUX_URL:-}"
API_KEY="${MINIFLUX_API_KEY:-}"
TEST_ONLY=false
DOCKER_ARGS=()
EXPORT_ARGS=()

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --url)
            MINIFLUX_URL="$2"
            shift 2
            ;;
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --test)
            TEST_ONLY=true
            EXPORT_ARGS+=("--test")
            shift
            ;;
        --status)
            EXPORT_ARGS+=("--status" "$2")
            shift 2
            ;;
        --starred)
            EXPORT_ARGS+=("--starred")
            shift
            ;;
        --organize-by-feed)
            EXPORT_ARGS+=("--organize-by-feed")
            shift
            ;;
        --organize-by-category)
            EXPORT_ARGS+=("--organize-by-category")
            shift
            ;;
        --image)
            IMAGE="$2"
            shift 2
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        *)
            print_error "未知选项: $1"
            show_usage
            exit 1
            ;;
    esac
done

# 验证必需参数
if [[ -z "$MINIFLUX_URL" ]]; then
    print_error "缺少 Miniflux URL"
    echo ""
    echo "请使用 --url 参数或设置 MINIFLUX_URL 环境变量"
    echo ""
    show_usage
    exit 1
fi

if [[ -z "$API_KEY" ]]; then
    print_error "缺少 API 密钥"
    echo ""
    echo "请使用 --api-key 参数或设置 MINIFLUX_API_KEY 环境变量"
    echo ""
    show_usage
    exit 1
fi

# 显示配置信息
echo ""
print_info "Miniflux Exporter Docker 启动"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  URL:    $MINIFLUX_URL"
echo "  输出:   $OUTPUT_DIR"
echo "  镜像:   $IMAGE"
if [[ "$TEST_ONLY" == "true" ]]; then
    echo "  模式:   测试连接"
else
    echo "  模式:   导出文章"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查 Docker 是否运行
if ! docker info > /dev/null 2>&1; then
    print_error "Docker 未运行，请先启动 Docker"
    exit 1
fi

# 检查镜像是否存在
if ! docker image inspect "$IMAGE" > /dev/null 2>&1; then
    print_warning "镜像 $IMAGE 不存在"
    print_info "正在构建镜像..."

    # 尝试构建镜像
    if [[ -f "Dockerfile" ]]; then
        docker build -t "$IMAGE" .
        print_success "镜像构建完成"
    else
        print_error "找不到 Dockerfile，请先构建镜像"
        echo ""
        echo "构建命令: docker build -t $IMAGE ."
        exit 1
    fi
fi

# 创建输出目录
if [[ "$TEST_ONLY" == "false" ]]; then
    mkdir -p "$OUTPUT_DIR"
    print_info "输出目录: $(cd "$OUTPUT_DIR" && pwd)"
fi

# 构建 Docker 运行命令
DOCKER_CMD=(
    docker run --rm
    -e MINIFLUX_URL="$MINIFLUX_URL"
    -e MINIFLUX_API_KEY="$API_KEY"
)

# 如果不是测试模式，挂载输出目录
if [[ "$TEST_ONLY" == "false" ]]; then
    DOCKER_CMD+=(-v "$(pwd)/$OUTPUT_DIR:/output")
    EXPORT_ARGS+=("--output" "/output")
fi

# 添加镜像名称
DOCKER_CMD+=("$IMAGE")

# 添加导出参数
DOCKER_CMD+=("${EXPORT_ARGS[@]}")

# 显示将要执行的命令（用于调试）
if [[ "${DEBUG:-false}" == "true" ]]; then
    echo ""
    print_info "执行命令:"
    echo "${DOCKER_CMD[@]}"
    echo ""
fi

# 运行 Docker 容器
print_info "开始运行..."
echo ""

if "${DOCKER_CMD[@]}"; then
    echo ""
    print_success "完成！"

    if [[ "$TEST_ONLY" == "false" ]]; then
        echo ""
        print_info "文章已导出到: $OUTPUT_DIR"

        # 统计导出的文件
        if [[ -d "$OUTPUT_DIR" ]]; then
            FILE_COUNT=$(find "$OUTPUT_DIR" -type f -name "*.md" | wc -l | tr -d ' ')
            print_success "导出了 $FILE_COUNT 篇文章"

            # 显示目录结构
            echo ""
            print_info "目录结构预览:"
            tree -L 2 "$OUTPUT_DIR" 2>/dev/null || ls -la "$OUTPUT_DIR"
        fi
    fi
else
    echo ""
    print_error "运行失败"
    exit 1
fi

echo ""
