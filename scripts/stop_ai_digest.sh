#!/bin/bash

# =====================================================
# AI 日报系统停止脚本
# =====================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}停止 AI 日报系统...${NC}"

# 停止 Celery Worker
echo -e "\n${YELLOW}停止 Celery Worker...${NC}"
pkill -f "celery.*worker" || echo -e "${YELLOW}Worker 未运行${NC}"

# 停止 Celery Beat
echo -e "${YELLOW}停止 Celery Beat...${NC}"
pkill -f "celery.*beat" || echo -e "${YELLOW}Beat 未运行${NC}"

sleep 2

# 检查是否还有进程
if ps aux | grep -E "celery.*(worker|beat)" | grep -v grep > /dev/null; then
    echo -e "${RED}❌ 部分进程未停止，强制终止...${NC}"
    pkill -9 -f "celery"
else
    echo -e "${GREEN}✅ 所有服务已停止${NC}"
fi

echo -e "\n${GREEN}AI 日报系统已停止${NC}\n"
