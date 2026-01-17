# 技术设计文档：Todo List 应用

## 1. 架构概述

### 1.1 架构模式
- **客户端-服务器架构**（前后端分离）
- **RESTful API** 通信方式

### 1.2 系统组件
```
┌─────────────────┐      HTTPS       ┌─────────────────┐
│                 │ ←──────────────→ │                 │
│   React Frontend │                  │  Node.js Backend│
│    (浏览器)       │                  │   (Express)     │
│                 │                  │                 │
└─────────────────┘                  └─────────────────┘
                                                 │
                                                 ↓
                                        ┌─────────────────┐
                                        │   SQLite 数据库  │
                                        └─────────────────┘
```

### 1.3 技术栈
- **前端**：React 18 + TypeScript + Vite
- **后端**：Node.js + Express + SQLite3
- **数据库**：SQLite
- **API 格式**：JSON

## 2. API 设计

### 2.1 API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/todos | 获取所有待办事项 |
| POST | /api/todos | 创建待办事项 |
| GET | /api/todos/:id | 获取单个待办事项 |
| PUT | /api/todos/:id | 更新待办事项 |
| DELETE | /api/todos/:id | 删除待办事项 |

### 2.2 请求/响应格式

**创建待办事项 (POST /api/todos)**

请求体：
```json
{
  "title": "学习 React",
  "description": "学习 React 基础知识和Hooks",
  "dueDate": "2024-01-20"
}
```

响应：
```json
{
  "id": 1,
  "title": "学习 React",
  "description": "学习 React 基础知识和Hooks",
  "dueDate": "2024-01-20",
  "status": "pending",
  "createdAt": "2024-01-15T10:00:00Z",
  "updatedAt": "2024-01-15T10:00:00Z"
}
```

## 3. 数据库设计

### 3.1 数据表

**todos 表**

| 字段 | 类型 | 约束 | 描述 |
|------|------|------|------|
| id | INTEGER | PRIMARY KEY | 主键 |
| title | TEXT | NOT NULL | 标题 |
| description | TEXT | | 描述 |
| dueDate | DATETIME | | 截止日期 |
| status | TEXT | DEFAULT 'pending' | 状态 |
| createdAt | DATETIME | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updatedAt | DATETIME | DEFAULT CURRENT_TIMESTAMP | 更新时间 |

## 4. 风险评估

### 4.1 已识别风险
- **数据库并发**：SQLite 不适合高并发场景 → 缓解：此应用为个人使用，并发低
- **数据安全**：本地 SQLite 文件可能丢失 → 缓解：实现数据备份机制

### 4.2 安全考虑
- 输入验证和清理
- 防止 SQL 注入（使用参数化查询）
- 安全的错误处理（不暴露敏感信息）
