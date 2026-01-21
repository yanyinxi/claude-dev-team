#!/bin/bash

# =====================================================
# AI 日报系统启动脚本
# =====================================================
# 功能：启动 Celery Worker 和 Celery Beat 定时任务
# 用途：每天早上 9:00 自动生成 AI 日报
# =====================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  AI 日报系统启动脚本${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}[1/5] 检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3: $(python3 --version)${NC}"

# 检查 Celery 是否安装
echo -e "\n${YELLOW}[2/5] 检查 Celery...${NC}"
if ! python3 -c "import celery" 2>/dev/null; then
    echo -e "${RED}❌ Celery 未安装，正在安装...${NC}"
    pip install celery sqlalchemy
fi
echo -e "${GREEN}✅ Celery 已安装${NC}"

# 检查 Claude Code CLI
echo -e "\n${YELLOW}[3/5] 检查 Claude Code CLI...${NC}"
if ! command -v claude &> /dev/null; then
    echo -e "${RED}❌ Claude Code CLI 未安装${NC}"
    echo -e "   请访问: https://github.com/anthropics/claude-code"
    exit 1
fi
echo -e "${GREEN}✅ Claude Code CLI 已安装${NC}"

# 创建日志目录
mkdir -p logs

# 获取项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 启动 Celery Worker
echo -e "\n${YELLOW}[4/5] 启动 Celery 服务...${NC}"
echo -e "${GREEN}启动 Celery Worker...${NC}"
PYTHONPATH="$PROJECT_ROOT" celery -A main.backend.tasks.ai_digest.task worker \
    --loglevel=info \
    --logfile=logs/celery_worker.log \
    --detach

sleep 2

# 启动 Celery Beat
echo -e "${GREEN}启动 Celery Beat (定时调度器)...${NC}"
PYTHONPATH="$PROJECT_ROOT" celery -A main.backend.tasks.ai_digest.task beat \
    --loglevel=info \
    --logfile=logs/celery_beat.log \
    --detach

sleep 2

# 检查进程
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  启动完成！${NC}"
echo -e "${GREEN}========================================${NC}"

echo -e "\n${YELLOW}运行中的进程：${NC}"
ps aux | grep -E "celery.*(worker|beat)" | grep -v grep

echo -e "\n${YELLOW}定时任务配置：${NC}"
echo -e "  ⏰ 每天早上 9:00 自动执行 AI 日报生成"

echo -e "\n${YELLOW}日志文件：${NC}"
echo -e "  📄 Worker 日志: logs/celery_worker.log"
echo -e "  📄 Beat 日志: logs/celery_beat.log"
echo -e "  📄 任务日志: logs/ai_digest_YYYYMMDD.log"

echo -e "\n${YELLOW}手动执行任务：${NC}"
echo -e "  ${GREEN}claude -p \"执行 /ai-digest\"${NC}"

echo -e "\n${YELLOW}停止服务：${NC}"
echo -e "  ${GREEN}./scripts/stop_ai_digest.sh${NC}"

echo -e "\n${YELLOW}查看日报：${NC}"
echo -e "  ${GREEN}cat main/docs/ai_digest/\$(date +%Y-%m-%d).md${NC}"

echo -e "\n${GREEN}✅ AI 日报系统已启动！${NC}\n"
