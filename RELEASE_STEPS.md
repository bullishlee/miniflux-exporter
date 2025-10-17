# 🚀 Miniflux Exporter 发布步骤

本文档提供清晰、简洁的发布步骤。

---

## 📋 准备工作（发布前必做）

### 1️⃣ 清理敏感信息

```bash
# 赋予脚本执行权限
chmod +x cleanup-sensitive-data.sh

# 运行清理脚本
./cleanup-sensitive-data.sh
```

手动检查：
```bash
# 确保没有敏感信息
grep -r "你的真实URL" . --include="*.md" --include="*.py" --include="*.sh"
grep -r "真实API密钥" . --include="*.md" --include="*.py" --include="*.sh"
```

### 2️⃣ 删除测试数据

```bash
# 删除所有测试输出
rm -rf miniflux_articles/
rm -rf test-articles/
rm -rf articles/

# 删除临时文件
find . -name "*.backup" -delete
find . -name "*.bak" -delete
find . -name ".DS_Store" -delete
```

### 3️⃣ 更新 GitHub 用户名占位符

在以下文件中将 `bullishlee` 替换为您的 GitHub 用户名：

```bash
# 批量替换（macOS）
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.yml" \) \
  -exec sed -i '' 's/bullishlee/YOUR_GITHUB_USERNAME/g' {} +

# 批量替换（Linux）
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.yml" \) \
  -exec sed -i 's/bullishlee/YOUR_GITHUB_USERNAME/g' {} +
```

或手动编辑这些文件：
- `README.md`
- `README_CN.md`
- `setup.py`
- `.github/workflows/*.yml`

### 4️⃣ 测试安装

```bash
# 测试 Python 安装
python3 -m venv test-env
source test-env/bin/activate
pip install -e .
miniflux-export --version
miniflux-export --help
deactivate
rm -rf test-env

# 测试 Docker 构建
docker build -t miniflux-exporter:test .
docker run --rm miniflux-exporter:test --version
```

---

## 🐙 发布到 GitHub

### 步骤 1：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`miniflux-exporter`
3. 描述：`Export your Miniflux articles to Markdown format`
4. 可见性：**Public**
5. ⚠️ **不要**勾选 "Initialize this repository with a README"
6. 点击 **Create repository**

### 步骤 2：推送代码

```bash
# 在项目目录中
cd miniflux-exporter

# 初始化 Git
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "feat: initial release of miniflux-exporter v1.0.0"

# 连接到 GitHub（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/miniflux-exporter.git

# 推送代码
git branch -M main
git push -u origin main
```

### 步骤 3：配置 GitHub Secrets

#### 3.1 PyPI API Token

1. 访问 https://pypi.org/account/register/ 注册账号
2. 进入 Account settings → API tokens → Add API token
3. Token name: `miniflux-exporter-github`
4. Scope: **Entire account**（首次发布必须）
5. **复制生成的 token**
6. 在 GitHub 仓库：
   - Settings → Secrets and variables → Actions → New repository secret
   - Name: `PYPI_API_TOKEN`
   - Secret: 粘贴 token
   - 点击 Add secret

#### 3.2 Docker Hub Credentials（可选）

1. 访问 https://hub.docker.com/ 注册账号
2. Account Settings → Security → New Access Token
3. Token description: `miniflux-exporter`
4. **复制生成的 token**
5. 在 GitHub 仓库添加两个 secrets：
   - Name: `DOCKERHUB_USERNAME`, Secret: 你的 Docker Hub 用户名
   - Name: `DOCKERHUB_TOKEN`, Secret: 粘贴 token

### 步骤 4：创建首个 Release

#### 方式 1：通过命令行（推荐）

```bash
# 确保代码已推送
git push origin main

# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0
```

这会自动触发 GitHub Actions：
- ✅ 运行所有测试
- ✅ 构建 Python 包
- ✅ 发布到 PyPI
- ✅ 构建 Docker 镜像
- ✅ 创建 GitHub Release

#### 方式 2：通过 GitHub 网页

1. 访问仓库页面
2. 点击 **Releases** → **Create a new release**
3. Tag version: `v1.0.0`
4. Release title: `Release v1.0.0`
5. Description（从 CHANGELOG.md 复制）:
   ```markdown
   ## 🎉 Miniflux Exporter v1.0.0
   
   首个稳定版本发布！
   
   ### ✨ 特性
   
   - 📄 导出 Miniflux 文章为 Markdown 格式
   - 🗂️ 灵活的文件组织方式（按订阅源/分类）
   - 🔍 智能过滤（状态/星标）
   - 📊 完整元数据保留
   - 🐳 Docker 支持
   - 🔄 增量导出
   - 🎨 可自定义配置
   
   ### 📦 安装
   
   ```bash
   pip install miniflux-exporter
   ```
   
   ### 🐳 Docker
   
   ```bash
   docker pull YOUR_USERNAME/miniflux-exporter:latest
   ```
   
   ### 📖 文档
   
   完整文档请查看 [README.md](README.md)
   ```
6. 点击 **Publish release**

---

## ✅ 验证发布

### 验证 PyPI

等待 5-10 分钟后：

```bash
# 访问 PyPI 页面
# https://pypi.org/project/miniflux-exporter/

# 测试安装
pip install miniflux-exporter
miniflux-export --version
```

### 验证 Docker

```bash
# 拉取镜像
docker pull YOUR_USERNAME/miniflux-exporter:latest

# 测试运行
docker run --rm YOUR_USERNAME/miniflux-exporter:latest --version
```

### 验证 GitHub

检查：
- ✅ Actions 工作流全部通过（绿色✓）
- ✅ Releases 页面有 v1.0.0
- ✅ README 正常显示
- ✅ 所有 badges 显示正确

---

## 📢 宣传项目

### GitHub

- 添加 Topics：`miniflux`, `rss`, `markdown`, `export`, `backup`, `python`, `cli`
- 设置仓库描述
- 启用 Issues 和 Discussions

### 社交媒体

**Twitter/X 示例：**
```
🚀 刚刚开源了 Miniflux Exporter v1.0.0！

将 Miniflux 文章导出为 Markdown 格式：
✨ 灵活组织
🔍 智能过滤
🐳 Docker 支持
📦 零依赖

pip install miniflux-exporter

#Python #RSS #Miniflux #OpenSource
https://github.com/YOUR_USERNAME/miniflux-exporter
```

**Reddit 推荐：**
- r/selfhosted
- r/Python
- r/opensource
- r/commandline

**Hacker News：**
```
Show HN: Miniflux Exporter – Export RSS articles to Markdown
https://github.com/YOUR_USERNAME/miniflux-exporter
```

---

## 🔄 后续版本发布

### 发布补丁版本（bug 修复）

```bash
# 1. 修改版本号
# miniflux_exporter/__init__.py: __version__ = "1.0.1"
# setup.py: version='1.0.1'

# 2. 更新 CHANGELOG.md
# 添加 ## [1.0.1] - 2024-01-XX 部分

# 3. 提交并打标签
git add .
git commit -m "fix: 修复某个问题"
git push origin main
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

### 发布小版本（新功能）

```bash
# 版本号改为 1.1.0
git commit -m "feat: 添加新功能"
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

### 发布大版本（重大变更）

```bash
# 版本号改为 2.0.0
git commit -m "feat!: 重大变更"
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

---

## ❓ 常见问题

### Q: PyPI 发布失败？

```bash
# 检查 GitHub Actions 日志
# Settings → Secrets → 确认 PYPI_API_TOKEN 正确

# 本地测试发布（使用 TestPyPI）
pip install build twine
python -m build
twine upload --repository testpypi dist/*
```

### Q: Docker 构建失败？

```bash
# 本地测试构建
docker build --no-cache -t miniflux-exporter:test .

# 查看详细日志
docker build --progress=plain -t miniflux-exporter:test .
```

### Q: 如何撤销发布？

PyPI 不允许删除版本，但可以：

```bash
# Yank 版本（阻止新安装）
pip install twine
twine yank miniflux-exporter 1.0.0
```

然后发布修复版本。

### Q: 忘记配置 Secrets？

1. 推送代码后再配置 Secrets
2. 重新推送标签触发工作流：
   ```bash
   git tag -d v1.0.0
   git push origin :refs/tags/v1.0.0
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

---

## 📋 快速检查清单

发布前：
- [ ] 敏感信息已清理
- [ ] 测试数据已删除
- [ ] 用户名占位符已替换
- [ ] 本地安装测试通过
- [ ] Docker 构建测试通过

发布时：
- [ ] GitHub 仓库已创建
- [ ] 代码已推送
- [ ] PyPI Secret 已配置
- [ ] 标签已推送（或 Release 已创建）

发布后：
- [ ] PyPI 页面正常
- [ ] Docker 镜像可拉取
- [ ] GitHub Actions 全部通过
- [ ] README 正常显示

---

## 🎉 完成！

恭喜您成功发布了开源项目！

接下来：
- 📊 监控 GitHub Issues
- 🔄 响应社区反馈
- 📝 持续改进文档
- 🚀 规划新功能

---

**上次更新**: 2024-01-15
**版本**: 1.0.0