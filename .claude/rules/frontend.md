---
paths: main/frontend/**/*.{vue,ts,js}
---

# Frontend Development Rules

**更新时间**: 2026-01-24
**策略关键词**: frontend, vue, typescript, components

## 路径特定规则

此规则仅适用于 `main/frontend/` 下的 Vue、TypeScript 和 JavaScript 文件。

## 最佳实践

### ✅ 组件拆分策略
- **描述**: 按职责拆分组件，保持单一职责原则
- **证据**: 基于实际开发经验，需要持续改进
- **成功率**: 80%
- **适用场景**: 所有 Vue 组件开发
- **拆分原则**:
  1. **通用组件** (`components/common/`) - 可复用的 UI 组件（Button, Card, Modal）
  2. **业务组件** (`components/`) - 特定业务逻辑组件（UserCard, QuestionCard）
  3. **页面组件** (`pages/`) - 页面级别容器组件（Home, Learning, Profile）
  4. **布局组件** (`components/layout/`) - 布局相关组件（Header, Footer, Sidebar）

### ✅ Composition API 优先
- **描述**: 使用 Vue 3 Composition API 编写组件，避免 Options API
- **证据**: 项目标准要求（参考 project_standards.md）
- **成功率**: 95%
- **适用场景**: 所有新组件开发
- **优势**:
  - 更好的 TypeScript 支持
  - 逻辑复用更简单（composables）
  - 代码组织更灵活
- **示例**:
  ```vue
  <script setup lang="ts">
  import { ref, computed } from 'vue'

  // ✅ 正确：使用 Composition API
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)

  function increment() {
    count.value++
  }
  </script>
  ```

### ✅ TypeScript 类型安全
- **描述**: 为所有 props、emits、函数添加类型定义
- **证据**: 项目标准要求（参考 project_standards.md）
- **成功率**: 90%
- **适用场景**: 所有 TypeScript 文件
- **示例**:
  ```typescript
  // ✅ 正确：完整的类型定义
  interface Props {
    userId: number
    userName: string
    isActive?: boolean
  }

  const props = defineProps<Props>()

  const emit = defineEmits<{
    update: [userId: number]
    delete: [userId: number]
  }>()
  ```

### ✅ Pinia 状态管理
- **描述**: 使用 Pinia 管理跨组件状态，避免 prop drilling
- **证据**: 项目标准要求（参考 project_standards.md）
- **成功率**: 95%
- **适用场景**: 跨页面/组件的全局状态
- **何时使用 Pinia**:
  - 用户认证状态
  - 全局配置
  - 跨页面共享数据
  - 需要持久化的状态
- **何时不用 Pinia**:
  - 组件内部状态（用 `ref`/`reactive`）
  - 父子组件通信（用 props/emits）
  - 临时 UI 状态

### ✅ 自动导入配置
- **描述**: 使用 unplugin-auto-import 和 unplugin-vue-components 自动导入
- **证据**: 项目标准要求（参考 project_standards.md）
- **成功率**: 100%
- **适用场景**: 所有 Vue 组件和 composables
- **优势**:
  - 减少重复的 import 语句
  - 代码更简洁
  - AI 更容易理解项目结构

### ✅ 目录结构规范
- **描述**: 严格遵守前端目录结构（components, pages, stores, services, utils）
- **证据**: 项目标准强制约束（参考 project_standards.md）
- **成功率**: 100%
- **适用场景**: 所有新文件创建
- **目录职责**:
  - `components/` - Vue 组件（通用 + 业务）
  - `pages/` - 页面级别根容器组件
  - `stores/` - Pinia 全局状态
  - `services/` - HTTP 请求、数据转换
  - `utils/` - 通用函数、类型定义
  - `router/` - Vue Router 路由配置
  - `styles/` - 全局样式、主题配置

## 反模式

### ⚠️ 组件职责不清
- **问题**: 一个组件包含过多逻辑，难以维护和测试
- **正确做法**: 按职责拆分组件，保持单一职责
- **原因**: 提高代码可维护性和可测试性
- **影响**: 组件臃肿，难以复用

### ⚠️ 过度使用 Pinia
- **问题**: 所有状态都放 Pinia，导致状态管理复杂
- **正确做法**: 只有跨组件/页面的状态才用 Pinia
- **原因**: 避免过度设计，保持简单
- **影响**: 状态管理复杂，难以调试

### ⚠️ 缺少类型定义
- **问题**: Props、emits、函数缺少类型定义
- **正确做法**: 为所有 props、emits、函数添加类型
- **原因**: 提高代码可靠性，减少运行时错误
- **影响**: 类型错误在运行时才发现

### ⚠️ 直接操作 DOM
- **问题**: 使用 `document.querySelector` 等直接操作 DOM
- **正确做法**: 使用 Vue 的响应式系统和 ref
- **原因**: 保持 Vue 的响应式特性
- **影响**: 破坏 Vue 的响应式系统

### ⚠️ 业务逻辑写在组件中
- **问题**: 组件包含复杂的业务逻辑
- **正确做法**: 业务逻辑提取到 composables 或 services
- **原因**: 提高代码复用性和可测试性
- **影响**: 组件难以测试和复用

## 聚合经验（基于实际开发）

### 📊 统计数据
- **平均奖励**: 8.0/10
- **成功率**: 80%
- **常见问题**:
  1. 组件拆分不够细致（需要持续改进）
  2. 类型定义不完整
  3. 过度使用 Pinia

### 🔄 进化历史
- **2026-01-24**: 重构为官方标准格式，添加路径特定规则
- **2026-01-23**: 添加组件拆分策略和最佳实践

### 📈 改进方向
1. 补充 Composables 最佳实践
2. 添加性能优化指南（懒加载、虚拟滚动）
3. 补充测试策略（Vitest + Playwright）
4. 添加样式管理最佳实践（Tailwind CSS）

## 相关文档

- **项目标准**: `.claude/project_standards.md`
- **前端文档**: `main/frontend/README.md`
- **目录结构**: `.claude/project_standards.md` → 目录结构
- **命名约定**: `.claude/project_standards.md` → 命名约定

