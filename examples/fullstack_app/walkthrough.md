# 企业级电商系统 - 步骤说明

## 使用方式

1. 在 Claude Code 中输入：
   ```
   "实现完整的电商系统，包括用户管理、商品管理、订单管理、购物车、支付、物流等模块，要求支持万级并发、99.9% 可用性"
   ```

2. 系统会自动：
   - 分析复杂需求
   - 进行架构设计和优化
   - 分配多个开发者（动态）
   - 并行开发多个模块
   - 集成和压力测试
   - 性能优化和调优
   - 安全审查
   - 交付生产级代码

## 预期输出

```
.claude/output/ecommerce_system/
├── prd/
│   ├── product_overview.md          # 产品概览
│   ├── user_management.md           # 用户管理模块
│   ├── product_management.md        # 商品管理模块
│   ├── order_management.md          # 订单管理模块
│   ├── payment.md                   # 支付模块
│   ├── logistics.md                 # 物流模块
│   └── user_stories.md              # 用户故事
├── design/
│   ├── architecture.md              # 系统架构
│   ├── microservices.md             # 微服务设计
│   ├── database_design.md           # 数据库设计
│   ├── api_design.md                # API 设计
│   ├── security.md                  # 安全方案
│   ├── performance.md               # 性能优化
│   └── task_assignment.json         # 任务分配
├── code/
│   ├── user_service/                # 用户服务
│   ├── product_service/             # 商品服务
│   ├── order_service/               # 订单服务
│   ├── payment_service/             # 支付服务
│   ├── logistics_service/           # 物流服务
│   ├── api_gateway/                 # API 网关
│   ├── database/
│   │   ├── schemas/                 # 数据库表设计
│   │   ├── migrations/              # 迁移脚本
│   │   └── seeds/                   # 测试数据
│   └── shared/
│       ├── constants/               # 常量定义
│       ├── utils/                   # 工具函数
│       └── middlewares/             # 中间件
├── tests/
│   ├── unit_tests/                  # 单元测试
│   ├── integration_tests/           # 集成测试
│   ├── performance_tests/           # 性能测试
│   ├── security_tests/              # 安全测试
│   ├── load_tests/                  # 负载测试
│   └── test_report.json             # 完整测试报告
├── reviews/
│   ├── code_review.json             # 代码审查
│   ├── architecture_review.md       # 架构审查
│   ├── security_review.md           # 安全审查
│   └── performance_review.md        # 性能审查
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile              # Docker 镜像
│   │   └── docker-compose.yml      # 容器编排
│   ├── kubernetes/
│   │   ├── deployment.yaml         # Kubernetes 部署
│   │   ├── service.yaml            # 服务配置
│   │   └── ingress.yaml            # 入口配置
│   ├── ci_cd/
│   │   ├── jenkins.yml             # CI/CD 流程
│   │   └── github_actions.yml      # 自动化工作流
│   └── deployment_guide.md         # 部署指南
├── operations/
│   ├── monitoring.md               # 监控方案
│   ├── logging.md                  # 日志方案
│   ├── alerting.md                 # 告警规则
│   ├── disaster_recovery.md        # 灾备方案
│   └── runbook.md                  # 运维手册
└── reports/
    ├── development_report.md       # 开发报告
    ├── performance_report.md       # 性能报告
    ├── security_report.md          # 安全报告
    └── delivery_report.md          # 交付报告
```

## 查看结果

```bash
# 查看产品概览
cat .claude/output/ecommerce_system/prd/product_overview.md

# 查看系统架构
cat .claude/output/ecommerce_system/design/architecture.md

# 查看微服务设计
cat .claude/output/ecommerce_system/design/microservices.md

# 查看数据库设计
cat .claude/output/ecommerce_system/design/database_design.md

# 查看 API 设计
cat .claude/output/ecommerce_system/design/api_design.md

# 查看安全方案
cat .claude/output/ecommerce_system/design/security.md

# 查看性能优化
cat .claude/output/ecommerce_system/design/performance.md

# 查看各服务代码
ls .claude/output/ecommerce_system/code/

# 查看测试报告
cat .claude/output/ecommerce_system/tests/test_report.json

# 查看性能测试结果
cat .claude/output/ecommerce_system/tests/performance_tests/

# 查看安全审查
cat .claude/output/ecommerce_system/reviews/security_review.md

# 查看部署指南
cat .claude/output/ecommerce_system/deployment/deployment_guide.md

# 查看监控方案
cat .claude/output/ecommerce_system/operations/monitoring.md

# 查看最终报告
cat .claude/output/ecommerce_system/reports/delivery_report.md
```

## 学习要点

通过这个案例，你可以学到：

1. **复杂需求分析** - 如何分解复杂系统需求
2. **微服务架构** - 微服务设计和服务边界划分
3. **数据库设计** - 大规模系统的数据库设计
4. **API 网关** - 统一的 API 入口管理
5. **支付集成** - 第三方支付系统集成
6. **性能优化** - 缓存、索引、查询优化等
7. **安全防护** - 认证、授权、数据加密等
8. **容器化部署** - Docker 和 Kubernetes 部署
9. **自动化流程** - CI/CD 和自动化测试
10. **运维方案** - 监控、日志、告警、灾备
11. **团队协作** - 大规模团队并行开发
12. **生产就绪** - 从开发到生产的完整流程
