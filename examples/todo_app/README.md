# Todo App - 完整全栈应用示例

一个现代化的全栈待办事项管理应用，包含 React 前端和 Express 后端，采用 SQLite 数据库。

**⭐ 这是一个完整的学习示例，展示从需求分析到上线部署的整个开发流程。**

---

## 📋 功能特性

- ✅ 创建、查看、更新和删除待办事项
- ✅ 标记任务完成状态
- ✅ 按状态筛选任务（待办/已完成）
- ✅ 响应式设计，支持各种设备
- ✅ RESTful API 接口
- ✅ 完整的单元测试覆盖
- ✅ 数据库自动初始化

---

## 🛠️ 技术栈

### 前端
- **React** - UI 框架
- **TypeScript** - 类型安全
- **Jest** - 单元测试框架
- **Babel** - JavaScript 编译器

### 后端
- **Express.js** - Web 框架
- **SQLite3** - 轻量级数据库
- **Node.js** - 运行时环境
- **Mocha/Chai** - 单元测试框架

---

## 📂 项目结构

```
todo_app/
├── src/
│   ├── backend/               # 后端代码
│   │   ├── app.js            # Express 主程序
│   │   ├── init.js           # 数据库初始化
│   │   ├── api/
│   │   │   └── todos.js      # API 路由
│   │   ├── models/           # 数据模型
│   │   └── services/         # 业务逻辑
│   ├── frontend/              # 前端代码
│   │   ├── index.html        # HTML 入口
│   │   ├── TodoApp.tsx       # React 主组件
│   │   ├── components/       # React 组件
│   │   ├── styles/           # 样式文件
│   │   └── types/            # TypeScript 类型
│   └── data/                 # 数据存储
├── tests/                     # 测试文件
│   ├── test_todos.js         # 后端测试
│   └── frontend/             # 前端测试
├── docs/                      # 文档
│   ├── api/                  # API 文档
│   ├── prd/                  # 产品需求文档
│   ├── tech_designs/         # 技术设计文档
│   └── ...                   # 其他文档
├── start.sh                  # ⭐ 一键启动脚本
├── quick-start.sh            # 快速启动脚本
├── dev.sh                    # 开发启动脚本
├── SCRIPTS.md                # 脚本使用指南
├── package.json              # 项目配置
├── jest.config.js            # Jest 配置
└── babel.config.json         # Babel 配置
```

---

## 🎨 前端 UI 入口

### HTML 入口点

**文件位置**: `src/frontend/index.html`

这是应用的 UI 入口文件，负责：

- **页面结构**：定义 HTML 文档标准格式
- **样式系统**：包含完整的 CSS 设计系统（颜色变量、布局、动画等）
- **元数据**：设置页面标题、字符编码、视口配置
- **应用挂载点**：提供 React 应用的 DOM 容器 `<div id="root"></div>`
- **脚本加载**：加载编译后的 React 应用代码

### 页面特性

- 📱 **响应式设计**：完美支持桌面、平板、手机设备
- 🎨 **现代化样式**：渐变背景、卡片设计、流畅动画
- 🎯 **无障碍支持**：语义化 HTML、ARIA 属性
- ⚡ **性能优化**：系统字体栈、关键 CSS 内联加载

### 访问路径

启动应用后，访问：
```
http://localhost:3000
```

浏览器会自动加载 `src/frontend/index.html`，然后：
1. React 在 `<div id="root"></div>` 上初始化
2. 加载 `TodoApp.tsx` 主应用组件
3. 建立与后端 API 的连接
4. 渲染交互式 UI 界面

### 相关文件

| 文件 | 用途 |
|------|------|
| `src/frontend/index.html` | HTML 入口（您在这里） |
| `src/frontend/TodoApp.tsx` | React 主组件 |
| `src/frontend/components/` | React 子组件（表单、列表等） |
| `src/frontend/styles/` | CSS 样式文件 |
| `src/frontend/types/` | TypeScript 类型定义 |

---

## ⚡ 启动应用

### 一键启动 ⭐ 推荐

```bash
cd claude-dev-team/examples/todo_app/
./start.sh
```

**自动执行**:
- ✅ 检查 Node.js 和 npm
- ✅ 安装依赖（如需要）
- ✅ 初始化数据库
- ✅ 启动应用

**首次启动和后续启动都用这个脚本，它会自动判断是否需要安装依赖。**

### 开发模式

```bash
cd claude-dev-team/examples/todo_app/
./dev.sh
```

用于本地开发调试。

### 手动启动

```bash
npm install      # 安装依赖
npm run init-db  # 初始化数据库
npm start        # 启动应用
```

---

## 🌐 访问应用

启动后，打开浏览器访问：

```
http://localhost:3000
```

---

## 📖 使用教程

### 第一步：启动应用

```bash
cd claude-dev-team/examples/todo_app/
./start.sh
```

### 第二步：体验功能

1. **添加待办事项**：在表单中输入任务标题，点击"添加"
2. **标记完成**：点击任务前的复选框标记为完成
3. **删除任务**：点击"删除"按钮移除任务
4. **筛选任务**：使用状态筛选器查看待办或已完成的任务

### 第三步：查看代码

- **前端代码**: `src/frontend/` - React 组件
- **后端代码**: `src/backend/` - Express API
- **数据库**: `src/backend/models/database.js` - 数据模型

### 第四步：运行测试

```bash
npm test                    # 所有测试
npm run test:backend        # 后端测试
npm run test:frontend       # 前端测试
npm run test:watch         # 实时监听前端测试
```

---

## 📡 API 文档

### 获取所有待办事项

```bash
GET /api/todos
```

**响应示例**:
```json
[
  {
    "id": 1,
    "title": "完成项目文档",
    "status": "pending",
    "createdAt": "2026-01-18T10:00:00Z"
  }
]
```

### 创建待办事项

```bash
POST /api/todos
Content-Type: application/json

{
  "title": "学习 React",
  "description": "学习 React 框架基础"
}
```

### 更新待办事项

```bash
PUT /api/todos/1

{
  "title": "学习 React Hooks",
  "status": "completed"
}
```

### 删除待办事项

```bash
DELETE /api/todos/1
```

详细 API 文档见: `docs/api/todo_app.yaml`

---

## 🎓 学习路径

### 初级（理解应用）- 15 分钟
- [ ] 启动应用并体验功能
- [ ] 查看前端代码 `src/frontend/`
- [ ] 查看后端 API 代码 `src/backend/api/`

### 中级（修改代码）- 30 分钟
- [ ] 阅读产品需求文档
- [ ] 理解数据库模型
- [ ] 修改 UI 样式或布局
- [ ] 运行单元测试

### 高级（扩展功能）- 60 分钟+
- [ ] 阅读技术设计文档
- [ ] 添加新的 API 端点
- [ ] 实现新的 React 组件
- [ ] 编写新的测试用例

---

## 💡 学习建议

### 1. 尝试简单修改

**改变应用标题**:
- 编辑 `src/frontend/TodoApp.tsx`
- 修改标题文本

**改变按钮样式**:
- 编辑 `src/frontend/components/TodoForm.css`
- 修改颜色或大小

### 2. 理解典型工作流

**一个请求的完整流程**:
1. 用户在前端提交表单
2. 前端发送 API 请求
3. 后端处理并验证数据
4. 数据库存储/查询数据
5. 后端返回 JSON 响应
6. 前端更新 UI 显示结果

**关键文件**:
- API 处理: `src/backend/api/todos.js`
- 数据库查询: `src/backend/models/database.js`

### 3. 添加新功能

想添加"优先级"功能？
1. 修改数据库表（添加 priority 字段）
2. 更新后端 API（处理 priority 参数）
3. 更新前端表单（添加优先级选择器）
4. 编写测试用例

---

## 🔧 常用命令

```bash
# 启动应用
cd claude-dev-team/examples/todo_app/
./start.sh              # 完整启动 
npm start               # 直接启动

# 测试
npm test                # 运行所有测试
npm run test:backend    # 后端测试
npm run test:frontend   # 前端测试
npm run test:watch      # 实时监听

# 其他
npm run init-db         # 重新初始化数据库
```

---

## 🐛 常见问题

### Q: 应用无法启动？

**A**: 尝试以下步骤：
```bash
cd claude-dev-team/examples/todo_app/

rm -rf node_modules
npm install
npm run init-db
./start.sh
```

### Q: 端口被占用怎么办？

**A**: 编辑 `src/backend/app.js` 修改端口，或使用环境变量：
```bash
PORT=8080 npm start
```

### Q: 如何重置数据库？

**A**: 删除数据库文件并重新初始化：
```bash
rm src/data/todos.db
npm run init-db
```

### Q: Windows 系统可以使用脚本吗？

**A**: 
- ✅ Git Bash: 可以直接使用 `.sh` 脚本
- ✅ PowerShell: 需要调整脚本格式
- ✅ CMD: 建议使用 npm 命令：`npm install && npm run init-db && npm start`

---

## 📚 详细文档

| 文档 | 说明 |
|------|------|
| `SCRIPTS.md` | 启动脚本详细说明 |
| `docs/prd/todo_app.md` | 产品需求文档 - 功能规格 |
| `docs/tech_designs/todo_app.md` | 技术设计文档 - 系统架构 |
| `docs/api/todo_app.yaml` | OpenAPI 规范 - API 详细说明 |
| `docs/test_reports/todo_app.md` | 测试报告 - 测试覆盖率 |
| `docs/reviews/todo_app.md` | 代码评审 - 评审意见 |

---

**祝你使用愉快！** 🎉 