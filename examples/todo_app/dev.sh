#!/bin/bash

# ============================================
# Todo App 开发启动脚本
# ============================================
# 此脚本用于开发，会启动多个开发工具
# - 后端服务器（自动重启）
# - 前端测试监听（实时运行测试）

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${MAGENTA}╔════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║  Todo App 开发启动 (Dev Mode)         ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════╝${NC}"
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

# 检查依赖是否已安装
if [ ! -d "node_modules" ]; then
    echo -e "${RED}✗ 错误: node_modules 不存在${NC}"
    echo -e "${YELLOW}请先运行: ./start.sh${NC}"
    exit 1
fi

# 初始化数据库
echo -e "${YELLOW}→ 初始化数据库...${NC}"
npm run init-db
echo -e "${GREEN}✓ 数据库初始化完成${NC}"
echo ""

echo -e "${MAGENTA}╔════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║     开发环境启动成功！                 ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}后端服务器${NC}: http://localhost:3000"
echo -e "${YELLOW}按 Ctrl+C 停止${NC}"
echo ""

# 启动后端服务器
npm start
