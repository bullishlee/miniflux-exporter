# Miniflux Exporter - 项目结构说明

本文档详细说明了项目的完整结构和每个文件的用途。

## 📁 完整目录结构

```
miniflux-exporter/
├── .github/                          # GitHub 配置目录
│   └── workflows/                    # GitHub Actions 工作流
│       ├── test.yml                  # 测试工作流（多版本、多平台）
│       ├── release.yml               # 发布工作流（PyPI + Docker）
│       └── docker.yml                # Docker 构建和安全扫描
│
├── miniflux_exporter/                # 主程序包
│   ├── __init__.py                   # 包初始化（版本信息、导出）
│   ├── __main__.py                   # 模块入口点（python -m 支持）
│   ├── cli.py                        # 命令行接口（参数解析、交互式设置）
│   ├── exporter.py                   # 核心导出逻辑
│   ├── config.py                     # 配置管理（YAML/JSON/环境变量）
│   └── utils.py                      # 工具函数（文件名清理、进度条等）
│
├── docker/                           # Docker 相关文件
│   ├── Dockerfile                    # 多阶段构建，多平台支持
│   └── docker-compose.yml            # Docker Compose 配置示例
│
├── docs/                             # 文档目录（可扩展）
│   ├── installation.md               # 安装指南
│   ├── configuration.md              # 配置详解
│   └── examples.md                   # 使用示例
│
├── examples/                         # 示例文件
│   ├── config.example.yaml           # YAML 配置示例（带详细注释）
│   ├── config.example.json           # JSON 配置示例
│   └── basic_export.py               # Python API 使用示例
│
├── tests/                            # 测试套件
│   ├── __init__.py                   # 测试包初始化
│   ├── test_exporter.py              # 导出器测试
│   ├── test_config.py                # 配置管理测试
│   ├── test_utils.py                 # 工具函数测试
│   └── conftest.py                   # pytest 配置和 fixtures
│
├── .gitignore                        # Git 忽略规则
├── .dockerignore                     # Docker 构建忽略规则
├── LICENSE                           # MIT 许可证
├── README.md                         # 英文说明文档
├── README_CN.md                      # 中文说明文档
├── CONTRIBUTING.md                   # 贡献指南
├── CHANGELOG.md                      # 变更日志
├── RELEASE.md                        # 发布流程指南
├── PUBLISH_GUIDE.md                  # 开源发布完整指南
├── PROJECT_STRUCTURE.md              # 本文件
│
├── setup.py                          # 安装配置（setuptools）
├── pyproject.toml                    # 项目配置（PEP 518）
├── requirements.txt                  # 运行时依赖
├── requirements-dev.txt              # 开发依赖
├── MANIFEST.in                       # 包含/排除文件规则
│
└── .pre-commit-config.yaml           # pre-commit 钩子配置（可选）
```

---

## 📄 核心文件说明

### 根目录文件

#### README.md & README_CN.md
- **用途**：项目主要说明文档（英文/中文）
- **包含内容**：
  - 项目简介和特性
  - 快速开始指南
  - 安装说明
  - 使用示例
  - 配置选项
  - Docker 使用
  - 贡献指南链接
  - 许可证信息

#### LICENSE
- **用途**：MIT 开源许可证
- **重要性**：⭐⭐⭐⭐⭐ 必需
- **说明**：定义项目的使用、修改和分发条款

#### CONTRIBUTING.md
- **用途**：贡献者指南
- **包含内容**：
  - 行为准则
  - 开发环境设置
  - 编码标准
  - 提交 PR 流程
  - Issue 报告模板

#### CHANGELOG.md
- **用途**：版本变更记录
- **格式**：遵循 [Keep a Changelog](https://keepachangelog.com/)
- **示例**：
  ```markdown
  ## [1.0.0] - 2024-01-15
  ### Added
  - 新功能 X
  ### Changed
  - 改进 Y
  ### Fixed
  - 修复 Z
  ```

#### setup.py
- **用途**：Python 包安装配置
- **功能**：
  - 定义包元数据
  - 指定依赖
  - 配置入口点（CLI 命令）
  - PyPI 分类标签

#### requirements.txt
- **用途**：运行时依赖列表
- **包含**：
  - `miniflux>=0.0.7`
  - `html2text>=2020.1.16`
  - `PyYAML>=5.4.0`
  - `requests>=2.25.0`

#### requirements-dev.txt
- **用途**：开发和测试依赖
- **包含**：
  - 测试框架（pytest）
  - 代码格式化（black）
  - 代码检查（flake8, pylint）
  - 类型检查（mypy）
  - 构建工具（build, twine）

---

## 🐍 Python 包结构

### miniflux_exporter/

#### `__init__.py`
```python
# 包初始化文件
- 版本号定义
- 公共 API 导出
- 包级文档字符串
```

**导出内容**：
- `__version__`
- `MinifluxExporter`
- `Config`

#### `cli.py`
```python
# 命令行接口模块
- argparse 参数定义
- 交互式设置向导
- 命令执行逻辑
- 进度显示
```

**功能**：
- 解析命令行参数
- 运行交互式配置向导
- 测试连接
- 执行导出
- 错误处理和用户友好的输出

**主要函数**：
- `main()` - CLI 入口点
- `interactive_setup()` - 交互式向导
- `test_connection()` - 连接测试
- `run_export()` - 运行导出

#### `exporter.py`
```python
# 核心导出逻辑
- MinifluxExporter 类
- Miniflux API 交互
- 文章获取和处理
- 文件保存
```

**主要类/方法**：
- `MinifluxExporter` 类
  - `connect()` - 连接到 Miniflux
  - `export()` - 导出文章
  - `test_connection()` - 测试连接
  - `get_feeds_info()` - 获取订阅源信息
  - `_save_entry()` - 保存单篇文章

#### `config.py`
```python
# 配置管理模块
- Config 类
- 配置验证
- 多种格式支持（YAML/JSON/环境变量）
```

**功能**：
- 加载配置文件（YAML/JSON）
- 环境变量支持
- 配置验证
- 默认值管理
- 配置保存

**主要方法**：
- `Config.from_file()` - 从文件加载
- `validate()` - 验证配置
- `to_file()` - 保存到文件

#### `utils.py`
```python
# 工具函数集合
- 文件名清理
- Markdown 转换辅助
- 进度条显示
- 路径处理
```

**主要函数**：
- `sanitize_filename()` - 清理文件名
- `create_markdown_frontmatter()` - 创建元数据头
- `format_filename()` - 格式化文件名
- `get_save_path()` - 获取保存路径
- `print_progress_bar()` - 显示进度条

#### `__main__.py`
```python
# 模块入口点
- 支持 python -m miniflux_exporter
```

---

## 🐳 Docker 文件

### docker/Dockerfile
- **类型**：多阶段构建
- **平台支持**：
  - linux/amd64
  - linux/arm64
  - linux/arm/v7
- **特性**：
  - 非 root 用户运行
  - 最小化镜像大小
  - 健康检查
  - 卷支持

### docker/docker-compose.yml
- **用途**：快速启动配置
- **环境变量**：
  - `MINIFLUX_URL`
  - `MINIFLUX_API_KEY`
  - `MINIFLUX_OUTPUT_DIR`
- **卷挂载**：`./articles:/output`

---

## ⚙️ GitHub Actions 工作流

### .github/workflows/test.yml
**触发条件**：
- Push 到 main/develop
- Pull request
- 手动触发

**任务**：
1. **test** - 多版本/多平台测试
   - Python 3.6-3.12
   - Ubuntu, macOS, Windows
   - 代码覆盖率
   - 上传到 Codecov

2. **lint** - 代码质量检查
   - flake8, pylint
   - isort（导入排序）
   - bandit（安全扫描）

3. **docs** - 文档检查
   - README 存在性
   - 必需文件检查

### .github/workflows/release.yml
**触发条件**：
- 推送 `v*.*.*` 标签

**任务**：
1. **build** - 构建发行包
2. **test-install** - 测试安装
3. **publish-pypi** - 发布到 PyPI
4. **create-release** - 创建 GitHub Release
5. **build-docker** - 构建并推送 Docker 镜像

### .github/workflows/docker.yml
**触发条件**：
- Push 到 main/develop
- Pull request

**任务**：
1. **docker-build** - 构建 Docker 镜像
2. **docker-scan** - Trivy 安全扫描

---

## 📚 文档文件

### docs/ 目录
- `installation.md` - 详细安装指南
- `configuration.md` - 配置选项说明
- `examples.md` - 使用示例集合
- `api.md` - Python API 文档（如果需要）

### 特殊文档

#### PUBLISH_GUIDE.md
**用途**：开源发布完整指南
**包含**：
- 发布前准备
- GitHub 设置
- PyPI 发布流程
- Docker 发布流程
- CI/CD 配置
- 注意事项和最佳实践

#### RELEASE.md
**用途**：版本发布流程
**包含**：
- 版本管理
- 发布检查清单
- 构建和发布步骤
- 回滚程序

---

## 🧪 测试文件

### tests/ 目录

#### conftest.py
- pytest 配置
- 共享 fixtures
- 测试工具函数

#### test_exporter.py
```python
# 测试导出器功能
- 连接测试
- 文章获取测试
- 文件保存测试
- 错误处理测试
```

#### test_config.py
```python
# 测试配置管理
- 配置加载测试
- 验证测试
- 环境变量测试
```

#### test_utils.py
```python
# 测试工具函数
- 文件名清理测试
- 路径处理测试
- 格式化测试
```

---

## 📋 配置和元数据文件

### .gitignore
**忽略内容**：
- Python 缓存（`__pycache__/`, `*.pyc`）
- 虚拟环境（`venv/`, `env/`）
- 构建文件（`dist/`, `build/`, `*.egg-info/`）
- 敏感文件（`config.yaml`, `*.backup`）
- 输出目录（`miniflux_articles/`）
- IDE 配置（`.vscode/`, `.idea/`）

### .dockerignore
**忽略内容**：
- Git 文件
- 测试文件
- 文档
- 开发工具配置
- 示例文件

### pyproject.toml
**用途**：现代 Python 项目配置（PEP 518）
**配置内容**：
- 构建系统要求
- Black 配置
- isort 配置
- pytest 配置
- mypy 配置

### MANIFEST.in
**用途**：指定包含在发行包中的非 Python 文件
**包含**：
- README 文件
- LICENSE
- requirements.txt
- 示例配置文件

---

## 🚀 使用场景和对应文件

### 场景 1：首次使用
**需要文件**：
1. `README.md` 或 `README_CN.md` - 阅读说明
2. `examples/config.example.yaml` - 复制为 `config.yaml`
3. `miniflux_exporter/cli.py` - 运行交互式设置

**命令**：
```bash
pip install miniflux-exporter
miniflux-export --setup
```

### 场景 2：开发贡献
**需要文件**：
1. `CONTRIBUTING.md` - 阅读贡献指南
2. `requirements-dev.txt` - 安装开发依赖
3. `tests/` - 运行和编写测试
4. `.github/workflows/` - 了解 CI/CD 流程

**命令**：
```bash
git clone https://github.com/bullishlee/miniflux-exporter.git
pip install -r requirements-dev.txt
pytest tests/
```

### 场景 3：Docker 使用
**需要文件**：
1. `docker/Dockerfile` - 构建镜像
2. `docker/docker-compose.yml` - 快速启动
3. `README.md` - Docker 使用说明

**命令**：
```bash
docker-compose up
# 或
docker run -v $(pwd)/articles:/output \
  -e MINIFLUX_URL=https://your-instance.com \
  -e MINIFLUX_API_KEY=your_key \
  miniflux-exporter
```

### 场景 4：发布新版本
**需要文件**：
1. `RELEASE.md` - 发布流程
2. `CHANGELOG.md` - 更新变更日志
3. `miniflux_exporter/__init__.py` - 更新版本号
4. `setup.py` - 更新版本号

**命令**：
```bash
# 更新版本号和 CHANGELOG
git commit -m "chore(release): prepare version 1.1.0"
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

---

## 🔄 文件依赖关系

```
setup.py
  ├── miniflux_exporter/__init__.py (版本号)
  ├── requirements.txt (依赖)
  └── README.md (描述)

cli.py
  ├── exporter.py (核心功能)
  ├── config.py (配置管理)
  └── utils.py (工具函数)

exporter.py
  ├── config.py (配置)
  └── utils.py (工具)

Dockerfile
  ├── requirements.txt (依赖)
  └── setup.py (安装)

.github/workflows/release.yml
  ├── setup.py (构建)
  ├── requirements.txt (依赖)
  └── docker/Dockerfile (Docker)
```

---

## 📊 文件优先级

### ⭐⭐⭐⭐⭐ 必需（不可缺少）
- `miniflux_exporter/*.py` - 核心代码
- `setup.py` - 安装配置
- `requirements.txt` - 依赖
- `README.md` - 说明文档
- `LICENSE` - 许可证

### ⭐⭐⭐⭐ 重要（强烈推荐）
- `README_CN.md` - 中文文档
- `CONTRIBUTING.md` - 贡献指南
- `CHANGELOG.md` - 变更日志
- `.gitignore` - Git 配置
- `docker/Dockerfile` - Docker 支持
- `.github/workflows/` - CI/CD

### ⭐⭐⭐ 推荐（提升质量）
- `tests/` - 测试套件
- `examples/` - 示例文件
- `requirements-dev.txt` - 开发依赖
- `RELEASE.md` - 发布指南
- `.dockerignore` - Docker 配置

### ⭐⭐ 可选（增强功能）
- `docs/` - 详细文档
- `pyproject.toml` - 现代配置
- `MANIFEST.in` - 包配置
- `PUBLISH_GUIDE.md` - 发布指南

---

## 🔍 快速查找指南

**我想...**

- **安装使用** → `README.md` 或 `README_CN.md`
- **贡献代码** → `CONTRIBUTING.md`
- **查看变更** → `CHANGELOG.md`
- **了解许可** → `LICENSE`
- **发布版本** → `RELEASE.md` + `PUBLISH_GUIDE.md`
- **配置项目** → `examples/config.example.yaml`
- **运行测试** → `tests/` + `requirements-dev.txt`
- **使用 Docker** → `docker/Dockerfile` + `docker-compose.yml`
- **了解 CI/CD** → `.github/workflows/`
- **查看 API** → `miniflux_exporter/*.py` 的 docstrings

---

## 📝 维护检查清单

### 定期维护（每月）
- [ ] 更新依赖版本（`requirements.txt`）
- [ ] 检查安全漏洞（`pip-audit`）
- [ ] 审查 Issues 和 PRs
- [ ] 更新文档（如有 API 变更）

### 发布前检查
- [ ] 更新 `CHANGELOG.md`
- [ ] 更新版本号（`__init__.py`, `setup.py`）
- [ ] 运行所有测试
- [ ] 更新文档
- [ ] 检查 `README.md` 准确性

### 年度审查
- [ ] 审查整体架构
- [ ] 考虑重大重构
- [ ] 更新示例和教程
- [ ] 审查社区反馈
- [ ] 规划路线图

---

## 🎓 学习路径

### 初学者
1. 阅读 `README.md`
2. 查看 `examples/config.example.yaml`
3. 运行 `miniflux-export --setup`
4. 阅读生成的文件

### 开发者
1. 阅读 `CONTRIBUTING.md`
2. 浏览 `miniflux_exporter/` 代码
3. 查看 `tests/` 了解测试
4. 阅读 `.github/workflows/` 了解 CI/CD

### 维护者
1. 阅读 `RELEASE.md`
2. 阅读 `PUBLISH_GUIDE.md`
3. 了解所有配置文件
4. 熟悉发布流程

---

## 📞 获取帮助

- **使用问题** → Issues 或 README
- **开发问题** → CONTRIBUTING.md
- **发布问题** → RELEASE.md 或 PUBLISH_GUIDE.md
- **配置问题** → examples/ 或 docs/

---

**本项目结构遵循 Python 社区最佳实践，旨在提供清晰、可维护、易于贡献的代码库。**

最后更新：2024-01-15
版本：1.0.0