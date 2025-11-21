# 环境搭建

## 系统要求

- **操作系统**：Windows 10/11, Linux (Ubuntu 20.04+)
- **Node.js**：v18.0.0 或更高版本
- **Python**：3.8 或更高版本
- **Git**：用于版本控制
- **pnpm**：推荐的包管理器

## 安装步骤

### 1. 安装必要依赖

#### Node.js 和 pnpm

```bash
# 安装 Node.js
# 访问 https://nodejs.org/ 下载并安装 LTS 版本

# 安装 pnpm
npm install -g pnpm
```

### 2. 克隆项目仓库

```bash
git clone https://github.com/csplink/csp.git
cd csp
```

### 3. 安装项目依赖

```bash
# 安装前端和Electron依赖
pnpm install

# 安装Python后端依赖，至少需要 python3.10 以上版本
pnpm server:install
```

### 4. 启动

```bash
# 启动后端
pnpm server:dev

# 启动前端
pnpm dev
```

## 验证安装

- 主应用: 启动后会自动打开Electron窗口，显示CSP图形界面
