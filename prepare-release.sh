#!/bin/bash
# Miniflux Exporter - 一键准备发布脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo "=========================================="
echo "  Miniflux Exporter - 发布准备工具"
echo "=========================================="
echo ""

# 打印带颜色的消息
print_step() {
    echo -e "${BLUE}[步骤 $1]${NC} $2"
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

# 询问确认
confirm() {
    read -p "$(echo -e ${YELLOW}?${NC}) $1 (y/N): " response
    [[ "$response" =~ ^[Yy]$ ]]
}

# 步骤 1: 清理敏感信息
print_step "1/6" "清理敏感信息"
echo ""

if confirm "是否要清理敏感信息"; then
    echo ""

    # 定义敏感信息
    SENSITIVE_PATTERNS=(
        "miniflux.example.com"
        "your_api_key_here"
    )

    # 查找包含敏感信息的文件
    echo "正在扫描敏感信息..."
    FOUND_FILES=()

    for pattern in "${SENSITIVE_PATTERNS[@]}"; do
        while IFS= read -r file; do
            if [[ ! " ${FOUND_FILES[@]} " =~ " ${file} " ]]; then
                FOUND_FILES+=("$file")
            fi
        done < <(grep -rl "$pattern" . --include="*.md" --include="*.py" --include="*.sh" --include="*.yaml" --include="*.yml" 2>/dev/null || true)
    done

    if [ ${#FOUND_FILES[@]} -eq 0 ]; then
        print_success "未发现敏感信息"
    else
        print_warning "发现包含敏感信息的文件："
        for file in "${FOUND_FILES[@]}"; do
            echo "  - $file"
        done
        echo ""

        if confirm "是否自动替换为占位符"; then
            for file in "${FOUND_FILES[@]}"; do
                # 创建备份
                cp "$file" "${file}.backup"

                # 替换敏感信息
                sed -i.tmp 's/rss\.bullishlee\.eu\.org/miniflux.example.com/g' "$file"
                sed -i.tmp 's/your_api_key_here/your_api_key_here/g' "$file"
                rm -f "${file}.tmp"

                echo "  ✓ 已处理: $file"
            done
            print_success "敏感信息已替换"
        fi
    fi
else
    print_warning "跳过敏感信息清理"
fi

echo ""

# 步骤 2: 删除测试数据
print_step "2/6" "删除测试数据和临时文件"
echo ""

if confirm "是否删除测试输出和临时文件"; then
    echo ""

    # 测试输出目录
    TEST_DIRS=(
        "miniflux_articles"
        "test-articles"
        "articles"
        "test-output"
        "backup"
    )

    for dir in "${TEST_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            rm -rf "$dir"
            print_success "已删除: $dir/"
        fi
    done

    # 临时文件
    find . -name "*.backup" -delete 2>/dev/null && print_success "已删除: *.backup 文件"
    find . -name "*.bak" -delete 2>/dev/null && print_success "已删除: *.bak 文件"
    find . -name ".DS_Store" -delete 2>/dev/null && print_success "已删除: .DS_Store 文件"
    find . -name "*.pyc" -delete 2>/dev/null && print_success "已删除: *.pyc 文件"
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null && print_success "已删除: __pycache__/ 目录"

    # 配置文件
    CONFIG_FILES=(
        "config.yaml"
        "config.yml"
        "config.json"
        "test_config.yaml"
    )

    for file in "${CONFIG_FILES[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
            print_success "已删除: $file"
        fi
    done

else
    print_warning "跳过删除测试数据"
fi

echo ""

# 步骤 3: 删除不需要的文档
print_step "3/6" "清理不需要的文档"
echo ""

DOCS_TO_REMOVE=(
    "快速开始.md"
    "开始导出.md"
    "开始导出_您的实例.md"
    "使用指南.md"
    "Miniflux导出指南.md"
    "GET_STARTED.md"
    "cleanup-sensitive-data.sh"
    "PRE_RELEASE_CHECKLIST.md"
)

if confirm "是否删除临时文档文件"; then
    echo ""
    for doc in "${DOCS_TO_REMOVE[@]}"; do
        if [ -f "$doc" ]; then
            rm -f "$doc"
            print_success "已删除: $doc"
        fi
    done
else
    print_warning "跳过删除文档"
fi

echo ""

# 步骤 4: 更新 GitHub 用户名
print_step "4/6" "更新 GitHub 用户名"
echo ""

echo "当前所有 'yourusername' 占位符需要替换为您的 GitHub 用户名"
read -p "请输入您的 GitHub 用户名 (留空跳过): " GITHUB_USERNAME

if [ -n "$GITHUB_USERNAME" ]; then
    echo ""
    echo "正在替换用户名..."

    # 查找需要替换的文件
    FILES_WITH_PLACEHOLDER=$(grep -rl "yourusername" . --include="*.md" --include="*.py" --include="*.yml" 2>/dev/null || true)

    if [ -n "$FILES_WITH_PLACEHOLDER" ]; then
        while IFS= read -r file; do
            sed -i.tmp "s/yourusername/$GITHUB_USERNAME/g" "$file"
            rm -f "${file}.tmp"
            print_success "已更新: $file"
        done <<< "$FILES_WITH_PLACEHOLDER"
    else
        print_success "没有需要替换的文件"
    fi
else
    print_warning "跳过用户名替换"
fi

echo ""

# 步骤 5: 测试安装
print_step "5/6" "测试安装"
echo ""

if confirm "是否测试 Python 安装"; then
    echo ""
    echo "创建测试环境..."

    # 创建虚拟环境
    python3 -m venv .test-env
    source .test-env/bin/activate

    # 安装
    echo "安装包..."
    pip install -q -e .

    # 测试命令
    echo ""
    echo "测试命令..."
    if miniflux-export --version > /dev/null 2>&1; then
        print_success "miniflux-export --version 工作正常"
    else
        print_error "miniflux-export --version 失败"
    fi

    if miniflux-export --help > /dev/null 2>&1; then
        print_success "miniflux-export --help 工作正常"
    else
        print_error "miniflux-export --help 失败"
    fi

    # 清理
    deactivate
    rm -rf .test-env
    print_success "测试环境已清理"
else
    print_warning "跳过安装测试"
fi

echo ""

# 步骤 6: Docker 测试
print_step "6/6" "测试 Docker 构建"
echo ""

if confirm "是否测试 Docker 构建"; then
    echo ""
    echo "构建 Docker 镜像..."

    if docker build -t miniflux-exporter:test . > /dev/null 2>&1; then
        print_success "Docker 镜像构建成功"

        # 测试命令
        if docker run --rm miniflux-exporter:test --version > /dev/null 2>&1; then
            print_success "Docker 容器运行正常"
        else
            print_error "Docker 容器运行失败"
        fi
    else
        print_error "Docker 镜像构建失败"
    fi
else
    print_warning "跳过 Docker 测试"
fi

echo ""
echo "=========================================="
echo "  准备工作完成！"
echo "=========================================="
echo ""

# 最终检查清单
print_step "✓" "发布前检查清单"
echo ""
echo "请确认以下事项："
echo ""
echo "  [ ] 所有敏感信息已清理"
echo "  [ ] 测试数据已删除"
echo "  [ ] GitHub 用户名已更新"
echo "  [ ] Python 安装测试通过"
echo "  [ ] Docker 构建测试通过"
echo "  [ ] README.md 内容正确"
echo "  [ ] 版本号正确 (miniflux_exporter/__init__.py 和 setup.py)"
echo ""

if confirm "是否查看发布步骤"; then
    echo ""
    echo "=========================================="
    echo "  下一步：发布到 GitHub"
    echo "=========================================="
    echo ""
    echo "1. 创建 GitHub 仓库："
    echo "   https://github.com/new"
    echo ""
    echo "2. 初始化并推送代码："
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m \"feat: initial release of miniflux-exporter v1.0.0\""
    echo "   git remote add origin https://github.com/$GITHUB_USERNAME/miniflux-exporter.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    echo "3. 配置 GitHub Secrets："
    echo "   - PYPI_API_TOKEN (从 https://pypi.org/manage/account/token/ 获取)"
    echo "   - DOCKERHUB_USERNAME (可选)"
    echo "   - DOCKERHUB_TOKEN (可选)"
    echo ""
    echo "4. 创建 Release："
    echo "   git tag -a v1.0.0 -m \"Release version 1.0.0\""
    echo "   git push origin v1.0.0"
    echo ""
    echo "详细步骤请查看: RELEASE_STEPS.md"
    echo ""
fi

echo ""
print_success "准备工作全部完成！"
echo ""
echo "运行以下命令开始发布："
echo ""
echo "  git init"
echo "  git add ."
echo "  git commit -m \"feat: initial release of miniflux-exporter v1.0.0\""
echo ""
