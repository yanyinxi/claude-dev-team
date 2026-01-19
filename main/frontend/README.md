# KET备考系统 - 前端

## 技术栈

- Vue 3 (Composition API)
- TypeScript 5.x
- Vite 5.x
- Pinia 2.x (状态管理)
- Vue Router 4.x (路由)
- Tailwind CSS 3.x (样式)
- Axios (HTTP请求)

## 项目结构

```
src/
├── components/           # UI组件
│   ├── common/          # 通用组件
│   │   ├── Button.vue
│   │   └── Card.vue
│   ├── learning/        # 学习相关组件
│   │   ├── QuestionCard.vue
│   │   ├── AnswerOptions.vue
│   │   └── RewardAnimation.vue
│   └── achievement/     # 成就相关组件
│       └── ScoreDisplay.vue
├── pages/               # 页面组件
│   ├── Login.vue        # 登录页
│   ├── Learning.vue     # 学习页
│   └── Profile.vue      # 个人主页
├── stores/              # Pinia状态管理
│   ├── userStore.ts     # 用户状态
│   ├── questionStore.ts # 题目状态
│   └── progressStore.ts # 进度状态
├── services/            # API服务
│   ├── request.ts       # Axios封装
│   ├── authService.ts   # 认证服务
│   └── questionService.ts # 题目服务
├── router/              # 路由配置
│   └── index.ts
├── styles/              # 样式文件
│   ├── global.css
│   └── tailwind.css
├── App.vue              # 根组件
└── main.ts              # 入口文件
```

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`:

```bash
cp .env.example .env
```

### 3. 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:5173

### 4. 构建生产版本

```bash
npm run build
```

## 核心功能

### 登录功能
- 学生快速登录（输入昵称）
- 管理员登录（用户名/密码）
- JWT Token认证

### 学习功能
- 随机获取题目
- 答题并显示结果
- 答对显示星星动画
- 连击显示特效
- 实时显示积分和连击数

### 个人主页
- 显示基本信息
- 学习进度统计
- 今日目标进度
- 成就徽章展示

## API对接

前端通过 Axios 与后端 API 对接，所有请求自动添加 JWT Token。

API Base URL: `http://localhost:8000/api/v1`

主要接口:
- `POST /auth/login/student` - 学生登录
- `POST /auth/login/admin` - 管理员登录
- `GET /questions/random` - 获取随机题目
- `POST /answers` - 提交答案
- `GET /progress` - 获取学习进度
- `GET /achievements` - 获取成就列表

## 状态管理

使用 Pinia 管理全局状态:

- **userStore**: 用户信息、登录状态、积分、徽章
- **questionStore**: 当前题目、答题历史、错题本
- **progressStore**: 总题数、正确数、连击数、每日目标

## 路由守卫

使用 Vue Router 的路由守卫实现权限控制:

- 未登录用户访问需要认证的页面会自动跳转到登录页
- Token 失效时自动退出登录

## UI设计

- 活泼可爱的色彩（蓝色、黄色、绿色、粉色）
- 大字体、清晰的按钮（适合小学生）
- 流畅的动画效果
- 响应式设计

## 开发规范

- 使用 TypeScript 确保类型安全
- 使用 Composition API 编写组件
- 使用 Tailwind CSS 编写样式
- 组件职责单一，易于维护

## 注意事项

1. 确保后端服务已启动（http://localhost:8000）
2. 首次运行需要安装依赖
3. 开发环境使用 Vite 代理转发 API 请求
4. 生产环境需要配置 Nginx 反向代理

## 后续优化

- 添加单元测试
- 添加 E2E 测试
- 优化动画性能
- 添加错误边界处理
- 添加离线缓存
