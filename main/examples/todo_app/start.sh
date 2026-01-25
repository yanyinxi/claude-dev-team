#!/bin/bash

# ============================================
# Todo App 启动脚本
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Todo App 一键启动脚本             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# 进入项目目录
cd "$PROJECT_DIR"

# 清理占用端口 3000 的进程
echo -e "${YELLOW}→ 检查并清理端口 3000...${NC}"
if lsof -i :3000 > /dev/null 2>&1; then
    echo -e "${YELLOW}→ 发现端口 3000 被占用，正在清理...${NC}"
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
    sleep 1
    echo -e "${GREEN}✓ 端口已清理${NC}"
else
    echo -e "${GREEN}✓ 端口 3000 已空闲${NC}"
fi
echo ""

# 检查 Node.js 是否已安装
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ 错误: 未检测到 Node.js${NC}"
    echo "请先安装 Node.js (https://nodejs.org)"
    exit 1
fi

echo -e "${GREEN}✓ Node.js 已安装: $(node --version)${NC}"
echo -e "${GREEN}✓ npm 已安装: $(npm --version)${NC}"
echo ""

# 检查是否需要安装依赖
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}→ node_modules 不存在，正在安装依赖...${NC}"
    npm install
    echo -e "${GREEN}✓ 依赖安装完成${NC}"
    echo ""
else
    echo -e "${GREEN}✓ 依赖已安装${NC}"
fi

# 初始化数据库
echo -e "${YELLOW}→ 正在初始化数据库...${NC}"
npm run init-db
echo -e "${GREEN}✓ 数据库初始化完成${NC}"
echo ""

# 启动应用
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     应用启动成功！                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}应用运行在:${NC} http://localhost:3000"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止应用${NC}"
echo ""

# 启动应用
npm start
