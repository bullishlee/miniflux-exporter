# 🚀 快速发布指南

5 步完成开源发布！

---

## 📋 开始前

确保您在项目目录：
```bash
cd "HTML_ summarize/miniflux-exporter"
```

---

## 🎯 步骤 1：一键准备（2 分钟）

```bash
# 赋予脚本执行权限
chmod +x prepare-release.sh

# 运行准备脚本（会提示您确认每个步骤）
./prepare-release.sh
```

这个脚本会：
- ✅ 清理所有敏感信息
- ✅ 删除测试数据
- ✅ 更新 GitHub 用户名
- ✅ 测试安装和 Docker 构建

---

## 🐙 步骤 2：创建 GitHub 仓库（1 分钟）

1. 访问：https://github.com/new
2. 仓库名：`miniflux-exporter`
3. 描述：`Export your Miniflux articles to Markdown format`
4. 可见性：**Public**
5. ⚠️ **不要**勾选 "Initialize this repository with a README"
6. 点击 **Create repository**

---

## 📤 步骤 3：推送代码（1 分钟）

```bash
# 初始化 Git
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "feat: initial release of miniflux-exporter v1.0.0"

# 连接到 GitHub（替换 YOUR_USERNAME 为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/miniflux-exporter.git

# 推送代码
git branch -M main
git push -u origin main
```

---

## 🔑 步骤 4：配置 PyPI Secret（5 分钟）

### 获取 PyPI API Token

1. 访问 https://pypi.org/account/register/ 注册
2. 登录后进入：Account settings → API tokens
3. 点击 **Add API token**
4. Token name: `miniflux-exporter-github`
5. Scope: **Entire account**
6. 点击 **Add token**
7. **立即复制 token**（只显示一次！）

### 添加到 GitHub

1. 进入您的仓库：`https://github.com/YOUR_USERNAME/miniflux-exporter`
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Secret: 粘贴刚才复制的 token
6. 点击 **Add secret**

---

## 🎉 步骤 5：创建 Release（1 分钟）

```bash
# 创建标签
git tag -a v1.0.0 -m "Release version 1.0.0"

# 推送标签
git push origin v1.0.0
```

**完成！** GitHub Actions 会自动：
- ✅ 运行所有测试
- ✅ 构建 Python 包
- ✅ 发布到 PyPI
- ✅ 构建 Docker 镜像
- ✅ 创建 GitHub Release

---

## ✅ 验证发布（5 分钟后）

### 检查 GitHub Actions

访问：`https://github.com/YOUR_USERNAME/miniflux-exporter/actions`

确保所有工作流都显示绿色 ✓

### 检查 PyPI

访问：`https://pypi.org/project/miniflux-exporter/`

测试安装：
```bash
pip install miniflux-exporter
miniflux-export --version
```

### 检查 Release

访问：`https://github.com/YOUR_USERNAME/miniflux-exporter/releases`

应该看到 v1.0.0 release

---

## 🐳 可选：配置 Docker Hub

如果想发布 Docker 镜像到 Docker Hub：

1. 访问 https://hub.docker.com/ 注册
2. Account Settings → Security → **New Access Token**
3. Description: `miniflux-exporter`
4. 复制 token
5. 在 GitHub 仓库添加两个 secrets：
   - `DOCKERHUB_USERNAME`：你的 Docker Hub 用户名
   - `DOCKERHUB_TOKEN`：刚才的 token

---

## 📢 宣传项目

### 添加仓库 Topics

在 GitHub 仓库主页，点击 ⚙️ 设置图标，添加：

```
miniflux rss feed export markdown backup python cli docker
```

### 社交媒体

**Twitter/X：**
```
🚀 刚开源了 Miniflux Exporter！

将 Miniflux 文章导出为 Markdown：
✨ 灵活组织
🔍 智能过滤  
🐳 Docker 支持

pip install miniflux-exporter

#Python #RSS #Miniflux #OpenSource
```

**Reddit：**
- r/selfhosted
- r/Python
- r/opensource

---

## ❓ 遇到问题？

### Actions 失败

1. 检查 `PYPI_API_TOKEN` 是否正确配置
2. 查看 Actions 日志获取详细错误

### PyPI 发布失败

```bash
# 本地测试发布
pip install build twine
python -m build
twine check dist/*
```

### Docker 构建失败

```bash
# 本地测试构建
docker build --no-cache -t test .
```

---

## 📚 详细文档

- **RELEASE_STEPS.md** - 详细发布步骤
- **PUBLISH_GUIDE.md** - 完整发布指南
- **PROJECT_STRUCTURE.md** - 项目结构说明

---

## ✅ 完成检查清单

- [ ] 准备脚本已运行
- [ ] GitHub 仓库已创建
- [ ] 代码已推送
- [ ] PyPI Secret 已配置
- [ ] Release 标签已创建
- [ ] GitHub Actions 全部通过
- [ ] PyPI 可以安装
- [ ] README 正常显示

---

## 🎊 恭喜！

您的开源项目已成功发布！

**项目地址：**
- GitHub: `https://github.com/YOUR_USERNAME/miniflux-exporter`
- PyPI: `https://pypi.org/project/miniflux-exporter/`

**安装命令：**
```bash
pip install miniflux-exporter
```

**Docker 命令：**
```bash
docker pull YOUR_USERNAME/miniflux-exporter:latest
```

---

**预计总用时：15 分钟**

**准备好了吗？从步骤 1 开始！** 🚀