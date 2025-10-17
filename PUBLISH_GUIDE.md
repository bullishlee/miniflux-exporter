# Miniflux Exporter - 开源发布完整指南

本文档提供完整的开源发布准备、发布流程和注意事项。

## 📋 目录

1. [发布前准备](#发布前准备)
2. [GitHub 仓库设置](#github-仓库设置)
3. [发布到 PyPI](#发布到-pypi)
4. [发布 Docker 镜像](#发布-docker-镜像)
5. [持续集成/持续部署](#持续集成持续部署)
6. [注意事项和最佳实践](#注意事项和最佳实践)
7. [发布后维护](#发布后维护)

---

## 🎯 发布前准备

### 1. 代码审查清单

- [x] 代码已重构为标准 Python 包结构
- [x] 所有功能模块化，易于维护
- [x] 添加了完整的类型注解
- [x] 代码符合 PEP 8 标准
- [x] 移除了所有硬编码的 API 密钥和敏感信息
- [x] 添加了配置文件支持（YAML/JSON）
- [x] 环境变量支持

**检查命令：**

```bash
# 检查是否有遗留的敏感信息
grep -r "api_key.*=" --include="*.py" miniflux_exporter/
grep -r "password.*=" --include="*.py" miniflux_exporter/
grep -r "secret" --include="*.py" miniflux_exporter/

# 确保配置示例中没有真实密钥
grep -r "your_api_key_here" examples/
```

### 2. 文档完整性检查

- [x] README.md（英文）
- [x] README_CN.md（中文）
- [x] CONTRIBUTING.md
- [x] LICENSE
- [x] CHANGELOG.md
- [x] 配置示例文件
- [x] 使用指南和教程

**必需的 README 章节：**
- 项目简介和特性
- 快速开始
- 安装说明
- 使用示例
- 配置说明
- 贡献指南链接
- 许可证信息

### 3. 依赖管理

**检查 requirements.txt：**
```bash
pip-compile requirements.in  # 如果使用 pip-tools
pip list --outdated
```

**固定版本号策略：**
- 核心依赖：使用 `>=` 指定最低版本
- 开发依赖：可以更宽松
- 避免固定到具体补丁版本（除非有已知问题）

```txt
# 推荐格式
miniflux>=0.0.7
html2text>=2020.1.16
PyYAML>=5.4.0
```

### 4. 测试覆盖率

```bash
# 运行测试并生成覆盖率报告
pytest tests/ --cov=miniflux_exporter --cov-report=html --cov-report=term

# 目标：>80% 覆盖率
```

---

## 🐙 GitHub 仓库设置

### 1. 创建仓库

1. 登录 GitHub
2. 点击 "New repository"
3. 仓库名：`miniflux-exporter`
4. 描述：`Export your Miniflux articles to Markdown format`
5. 选择 Public
6. **不要**初始化 README（我们已经有了）

### 2. 推送代码

```bash
# 在项目目录中初始化 Git
cd miniflux-exporter
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "feat: initial release of miniflux-exporter"

# 添加远程仓库（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/miniflux-exporter.git

# 推送到 main 分支
git branch -M main
git push -u origin main
```

### 3. 仓库设置配置

#### 设置 GitHub Secrets（用于 CI/CD）

进入：Settings → Secrets and variables → Actions → New repository secret

需要添加的 Secrets：

| Secret Name | 用途 | 如何获取 |
|-------------|------|---------|
| `PYPI_API_TOKEN` | PyPI 发布 | https://pypi.org/manage/account/token/ |
| `DOCKERHUB_USERNAME` | Docker Hub 登录 | 你的 Docker Hub 用户名 |
| `DOCKERHUB_TOKEN` | Docker Hub 发布 | https://hub.docker.com/settings/security |

#### 启用 GitHub Pages（可选）

Settings → Pages → Source → GitHub Actions

#### 设置分支保护规则（推荐）

Settings → Branches → Add rule

对 `main` 分支：
- ✅ Require a pull request before merging
- ✅ Require status checks to pass
- ✅ Require conversation resolution before merging

### 4. 添加主题标签

在仓库主页点击设置图标，添加标签：

```
miniflux rss feed export markdown backup python cli tool
```

---

## 📦 发布到 PyPI

### 1. 注册 PyPI 账号

- 主站：https://pypi.org/account/register/
- 测试站（可选）：https://test.pypi.org/account/register/

### 2. 创建 API Token

1. 登录 PyPI
2. Account settings → API tokens
3. Add API token
   - Token name: `miniflux-exporter-github-actions`
   - Scope: Entire account（首次）或指定项目
4. **复制 token**（只显示一次！）
5. 添加到 GitHub Secrets: `PYPI_API_TOKEN`

### 3. 本地测试构建

```bash
# 安装构建工具
pip install build twine

# 清理旧的构建文件
rm -rf build dist *.egg-info

# 构建发行包
python -m build

# 检查生成的包
twine check dist/*

# 预期输出：
# dist/
#   ├── miniflux_exporter-1.0.0-py3-none-any.whl
#   └── miniflux-exporter-1.0.0.tar.gz
```

### 4. 上传到 TestPyPI（可选但推荐）

```bash
# 上传到测试服务器
twine upload --repository testpypi dist/*

# 测试安装
pip install --index-url https://test.pypi.org/simple/ miniflux-exporter

# 测试功能
miniflux-export --version
miniflux-export --help
```

### 5. 上传到正式 PyPI

**方式 1：手动上传**

```bash
twine upload dist/*
```

**方式 2：通过 GitHub Release（推荐）**

创建 Git 标签会自动触发发布：

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

GitHub Actions 会自动：
- 运行测试
- 构建包
- 上传到 PyPI

### 6. 验证发布

1. 访问：https://pypi.org/project/miniflux-exporter/
2. 检查版本号、描述、标签
3. 测试安装：

```bash
# 创建新的虚拟环境测试
python -m venv test-env
source test-env/bin/activate
pip install miniflux-exporter
miniflux-export --version
deactivate
rm -rf test-env
```

---

## 🐳 发布 Docker 镜像

### 1. 注册 Docker Hub

- 访问：https://hub.docker.com/signup
- 创建账号
- 创建访问令牌：Account Settings → Security → New Access Token

### 2. 本地测试 Docker 构建

```bash
cd docker

# 构建镜像
docker build -t miniflux-exporter:test .

# 测试运行
docker run --rm miniflux-exporter:test --version
docker run --rm miniflux-exporter:test --help

# 测试完整流程（需要真实 API）
docker run --rm \
  -v $(pwd)/test-output:/output \
  -e MINIFLUX_URL=https://your-instance.com \
  -e MINIFLUX_API_KEY=your_key \
  miniflux-exporter:test
```

### 3. 配置多平台构建

```bash
# 创建构建器
docker buildx create --name multiplatform --use

# 构建多平台镜像（测试）
docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t bullishlee/miniflux-exporter:test \
  --load \
  .
```

### 4. 推送到 Docker Hub

**方式 1：手动推送**

```bash
# 登录
docker login

# 标记镜像
docker tag miniflux-exporter:test bullishlee/miniflux-exporter:1.0.0
docker tag miniflux-exporter:test bullishlee/miniflux-exporter:latest

# 推送
docker push bullishlee/miniflux-exporter:1.0.0
docker push bullishlee/miniflux-exporter:latest
```

**方式 2：通过 GitHub Actions（推荐）**

推送标签会自动触发 Docker 构建和发布：

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 5. 发布到 GitHub Container Registry（可选）

镜像会自动发布到：
- Docker Hub: `docker.io/bullishlee/miniflux-exporter`
- GHCR: `ghcr.io/bullishlee/miniflux-exporter`

---

## 🔄 持续集成/持续部署

### 已配置的 GitHub Actions 工作流

#### 1. test.yml - 测试工作流

**触发条件：**
- Push 到 main/develop 分支
- Pull request 到 main/develop
- 手动触发

**功能：**
- 多 Python 版本测试（3.6-3.12）
- 多操作系统测试（Ubuntu, macOS, Windows）
- 代码质量检查（flake8, black, mypy）
- 测试覆盖率报告
- 上传到 Codecov

#### 2. release.yml - 发布工作流

**触发条件：**
- 推送带 `v*.*.*` 格式的标签

**功能：**
- 构建 Python 包
- 测试安装
- 发布到 PyPI
- 创建 GitHub Release
- 构建并推送 Docker 镜像（多平台）

#### 3. docker.yml - Docker 构建工作流

**触发条件：**
- Push 到 main/develop
- Pull request
- 手动触发

**功能：**
- 构建 Docker 镜像
- 安全扫描（Trivy）
- 推送到 Docker Hub 和 GHCR

### 配置 Codecov（可选）

1. 访问：https://codecov.io/
2. 使用 GitHub 登录
3. 添加仓库
4. 获取 token（可能需要）
5. 添加 badge 到 README

```markdown
[![codecov](https://codecov.io/gh/bullishlee/miniflux-exporter/branch/main/graph/badge.svg)](https://codecov.io/gh/bullishlee/miniflux-exporter)
```

---

## ⚠️ 注意事项和最佳实践

### 安全注意事项

#### 1. 敏感信息处理

**绝对不要提交：**
- ❌ API 密钥
- ❌ 密码
- ❌ 私有配置
- ❌ `.env` 文件

**确保 .gitignore 包含：**
```gitignore
# Sensitive files
config.yaml
config.yml
config.json
*.local.*
.env
.env.local

# API keys
*api_key*
*secret*
```

#### 2. 示例文件命名

使用明显的示例后缀：
- ✅ `config.example.yaml`
- ✅ `settings.sample.json`
- ✅ `.env.template`

#### 3. 文档中的安全提示

在 README 中明确说明：
```markdown
## ⚠️ Security

Never commit your API keys or credentials to version control.
Always use environment variables or separate configuration files.
```

### 版本控制最佳实践

#### 语义化版本

遵循 [SemVer](https://semver.org/)：

- `1.0.0` - 首次稳定版本
- `1.0.1` - 补丁修复
- `1.1.0` - 新功能（向后兼容）
- `2.0.0` - 重大变更（不兼容旧版）

#### 标签规范

```bash
# 生产版本
v1.0.0, v1.1.0, v2.0.0

# 预发布版本
v1.0.0-alpha.1
v1.0.0-beta.1
v1.0.0-rc.1
```

#### 分支策略

- `main` - 稳定版本
- `develop` - 开发分支
- `feature/*` - 功能分支
- `hotfix/*` - 紧急修复分支

### 许可证选择

**MIT License（推荐，已使用）：**
- ✅ 简单宽松
- ✅ 允许商业使用
- ✅ 社区接受度高
- ✅ 与大多数项目兼容

**其他选项：**
- Apache 2.0 - 更详细的专利保护
- GPL v3 - 强制开源衍生作品
- BSD - 类似 MIT，稍有不同

### README 质量标准

**必须包含的徽章：**
```markdown
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)](https://www.python.org)
[![PyPI version](https://badge.fury.io/py/miniflux-exporter.svg)](https://pypi.org/project/miniflux-exporter/)
[![Downloads](https://pepy.tech/badge/miniflux-exporter)](https://pepy.tech/project/miniflux-exporter)
[![CI Status](https://github.com/bullishlee/miniflux-exporter/workflows/Tests/badge.svg)](https://github.com/bullishlee/miniflux-exporter/actions)
```

**质量检查清单：**
- [ ] 简洁的项目描述
- [ ] 清晰的特性列表
- [ ] 快速开始指南（< 5 分钟）
- [ ] 安装说明
- [ ] 使用示例（多个场景）
- [ ] 配置说明
- [ ] 截图或演示（如果适用）
- [ ] 贡献指南链接
- [ ] 许可证信息
- [ ] 支持和联系方式

### 社区建设

#### Issue 模板

创建 `.github/ISSUE_TEMPLATE/`：

1. **bug_report.md** - 错误报告模板
2. **feature_request.md** - 功能请求模板
3. **question.md** - 问题咨询模板

#### Pull Request 模板

创建 `.github/pull_request_template.md`

#### 行为准则

创建 `CODE_OF_CONDUCT.md`（可使用 GitHub 模板）

---

## 📢 发布后维护

### 1. 宣传发布

#### GitHub

- [ ] 创建详细的 Release 说明
- [ ] 添加变更日志
- [ ] 在 Discussions 中宣布

#### 社交媒体

- [ ] Twitter/X 发布
- [ ] Reddit（r/Python, r/selfhosted）
- [ ] Hacker News（Show HN:）
- [ ] Dev.to 博客文章

**发布模板：**

```
🚀 Introducing Miniflux Exporter v1.0.0!

Export your Miniflux articles to Markdown format with:
✅ Flexible organization options
✅ Smart filtering
✅ Metadata preservation
✅ Docker support

Install: pip install miniflux-exporter
Docs: https://github.com/bullishlee/miniflux-exporter

#Python #RSS #Miniflux #OpenSource
```

#### Miniflux 社区

- [ ] Miniflux GitHub Discussions
- [ ] Miniflux 相关论坛

### 2. 监控和反馈

#### 监控工具

- **PyPI 统计**：https://pypistats.org/packages/miniflux-exporter
- **Docker Hub 统计**：Docker Hub Dashboard
- **GitHub Insights**：仓库 Insights 标签

#### 响应社区

- 定期检查 Issues
- 回复 Pull Requests
- 参与 Discussions
- 更新文档基于反馈

### 3. 持续改进

#### 定期任务

**每周：**
- 检查新 issues
- 审查 pull requests
- 更新依赖（如有安全更新）

**每月：**
- 检查依赖更新
- 审查性能指标
- 计划新特性

**每季度：**
- 更新文档
- 重构代码（如需要）
- 发布小版本更新

#### 版本发布节奏

建议：
- **补丁版本**：按需发布（bug 修复）
- **小版本**：1-2 个月（新功能）
- **大版本**：6-12 个月（重大变更）

### 4. 维护者指南

#### 接受贡献的标准

- ✅ 符合代码风格
- ✅ 包含测试
- ✅ 更新文档
- ✅ 通过 CI 检查
- ✅ 签署 CLA（如有）

#### 标签系统

为 Issues 使用标签：
- `bug` - 错误报告
- `enhancement` - 功能请求
- `documentation` - 文档改进
- `good first issue` - 适合新贡献者
- `help wanted` - 需要帮助
- `priority: high` - 高优先级

---

## 🎓 学习资源

### Python 打包

- [Python Packaging Guide](https://packaging.python.org/)
- [setuptools 文档](https://setuptools.pypa.io/)
- [PyPI 帮助](https://pypi.org/help/)

### Docker

- [Docker 官方文档](https://docs.docker.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### GitHub Actions

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Awesome Actions](https://github.com/sdras/awesome-actions)

### 开源最佳实践

- [Open Source Guides](https://opensource.guide/)
- [Producing OSS by Karl Fogel](https://producingoss.com/)

---

## ✅ 最终检查清单

### 发布前

- [ ] 代码无敏感信息
- [ ] 所有测试通过
- [ ] 文档完整且更新
- [ ] CHANGELOG 已更新
- [ ] 版本号已更新
- [ ] LICENSE 文件存在
- [ ] README 包含所有必要信息
- [ ] 配置示例文件完整
- [ ] .gitignore 配置正确

### GitHub 仓库

- [ ] 仓库创建并设置为 Public
- [ ] 代码已推送
- [ ] Secrets 已配置
- [ ] 主题标签已添加
- [ ] 描述清晰简洁
- [ ] 仓库 URL 已更新到所有文档中

### PyPI

- [ ] 账号已注册
- [ ] API Token 已创建
- [ ] Token 已添加到 GitHub Secrets
- [ ] 包已成功上传
- [ ] 安装测试通过

### Docker

- [ ] Docker Hub 账号已注册
- [ ] 访问令牌已创建
- [ ] Credentials 已添加到 GitHub Secrets
- [ ] 镜像构建成功
- [ ] 多平台支持已测试

### CI/CD

- [ ] GitHub Actions 工作流正常运行
- [ ] 测试自动化工作
- [ ] 发布自动化工作
- [ ] Docker 自动构建工作

### 社区

- [ ] Issue 模板已创建
- [ ] PR 模板已创建
- [ ] CONTRIBUTING.md 存在
- [ ] CODE_OF_CONDUCT.md 存在

---

## 🎉 恭喜！

如果您完成了以上所有步骤，您的项目已经准备好开源发布了！

**下一步：**

1. 推送代码到 GitHub
2. 创建第一个 Release（v1.0.0）
3. 宣传您的项目
4. 响应社区反馈
5. 持续改进

**记住：**
- 开源不是一次性的，而是一个持续的过程
- 积极响应社区反馈
- 保持耐心和友好
- 享受开源的乐趣！

---

## 📞 需要帮助？

如果在发布过程中遇到问题：

1. 查看本指南的相关章节
2. 搜索相关文档和教程
3. 在 GitHub Discussions 中提问
4. 加入 Python 和开源社区寻求帮助

**祝您的开源项目取得成功！** 🚀🎊