---
name: api-design
description: 设计 RESTful API 规范。用于 API 端点定义、请求/响应格式、数据模型设计。
---

# API 设计技能

## 何时使用

当需要以下操作时使用此技能：
- 设计 RESTful API
- 定义请求/响应格式
- 设计数据模型
- 制定 API 规范文档

## 工作流程

### 第一步：理解业务需求
- 分析功能需求
- 识别资源（Resource）
- 定义操作（CRUD）

### 第二步：设计 API 端点
- 遵循 RESTful 约定
- 使用标准 HTTP 方法
- 设计清晰的 URL 结构

### 第三步：定义数据模型
- 识别核心实体
- 定义属性和类型
- 建立关系

### 第四步：编写 API 规范
- 使用 OpenAPI 格式
- 包含请求/响应示例
- 定义错误码

## 输出格式（OpenAPI）

```yaml
openapi: 3.0.0
info:
  title: [API 名称]
  version: 1.0.0

paths:
  /users:
    get:
      summary: 获取用户列表
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
```

## 最佳实践

1. **RESTful**：遵循 REST 设计原则
2. **版本控制**：在 URL 中包含版本号
3. **安全性**：使用 HTTPS，实施认证
4. **一致性**：保持命名和格式一致

---

## 📈 进化记录（自动生成）

_此章节由 Evolver 自动更新，记录从实际任务执行中学到的经验和最佳实践。_
