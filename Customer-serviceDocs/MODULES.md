# Customer-Service 核心模块说明

## 1. 模块概述

Customer-Service 系统采用模块化设计，按业务域划分各个服务模块。每个模块负责特定的业务功能，模块之间通过清晰的接口进行交互。

## 2. 模块分类

### 2.1 用户和权限管理模块

#### admin - 管理员和用户管理

**路径**: `internal/service/admin/`

**功能**:

- 用户登录认证（JWT Token 生成）
- 用户信息管理（创建、更新、查询）
- 角色管理（CRUD）
- 权限管理（URL 权限配置）
- 项目管理（项目配置）
- 项目配置查询

**主要接口**:

- `/admin/v1/auth/` - 管理员登录
- `/admin/v1/user/` - 用户管理
- `/admin/v1/role/` - 角色管理
- `/admin/v1/permission/` - 权限管理
- `/admin/v1/project/` - 项目管理
- `/admin/v1/project/config/` - 项目配置查询

**关联组件**:

- Model: `user.go`, `role.go`, `project.go`
- DAO: 对应的 DAO 层
- 外部服务: 权限验证中间件

---

#### web_user_manage - Web 用户管理

**路径**: `internal/service/web_user_manage/`

**功能**:

- Web 端用户管理
- 用户信息查询
- 用户操作记录

**主要接口**:

- `/api/customer-service-api/web_user_manage/*` - 用户管理相关接口

---

### 2.2 游戏管理模块

#### game - 游戏相关服务

**路径**: `internal/service/game/`

**功能**:

- 游戏服务器通信
- 游戏内数据查询
- 发票通知处理

**主要接口**:

- `/api/customer-service-api/web_game/*` - Web 游戏接口
- `/api/customer-service-api/proxy` - 代理转发请求
- `/api/customer-service-api/invoice/notify` - 发票通知

**关联组件**:

- External: `pkg/game_server` - 游戏服务器 SDK

---

#### gm - GM 工具

**路径**: `internal/service/gm/`

**功能**:

- GM 工具功能
- 物品管理（发送、查询）
- 玩家操作（封禁、解禁）
- 游戏数据查询
- 游戏内通知发送

**主要接口**:

- `/gm/v1/*` - GM 工具相关接口

**关联组件**:

- DAO: `internal/dao/dao_item_modify/item_dao.go`
- Model: `item_record.go`
- External: `pkg/game_server`

---

#### external_game_api - 游戏服务器外部接口

**路径**: `internal/service/external_game_api/`

**功能**:

- 游戏服务器调用的外部接口
- 游戏内事件回调
- 游戏数据同步

**主要接口**:

- 无需 JWT 认证，通过签名验证

**关联组件**:

- Middleware: `sign_verify` - 签名验证中间件

---

### 2.3 订单和支付模块

#### order_manage - 订单管理

**路径**: `internal/service/order_manage/`

**功能**:

- 订单查询（按用户、订单号、时间等）
- 订单详情获取
- 订单状态更新
- 订单统计
- 订单导出

**主要接口**:

- `/order_manage/v1/*` - 订单管理相关接口

**关联组件**:

- Model: 订单相关模型
- DAO: 订单 DAO
- External: `pkg/item_server` - 物品服务

---

#### pay - 支付服务

**路径**: `internal/service/pay/`

**功能**:

- 支付订单创建
- 支付回调处理
- 支付状态查询
- 支付退款
- 支付风控

**主要接口**:

- `/pay/v1/*` - 支付相关接口

**关联组件**:

- Model: 支付相关模型
- DAO: 支付 DAO
- External: 支付网关 SDK

---

#### invoice - 发票管理

**路径**: `internal/service/invoice/`

**功能**:

- 发票申请
- 发票查询
- 发票开具
- 发票下载
- 发票记录管理

**主要接口**:

- `/invoice/v1/*` - 发票相关接口
- `/api/customer-service-api/invoice/notify` - 发票通知回调

**关联组件**:

- Model: `model_invoice/` 目录下模型
- External: `pkg/invoice_server` - 发票服务 SDK

---

#### exchange - 兑换码管理

**路径**: `internal/service/exchange/`

**功能**:

- 兑换码生成
- 兑换码验证
- 兑换码使用
- 兑换记录查询
- 兑换码状态管理

**主要接口**:

- `/exchange/v1/*` - 兑换码相关接口

**关联组件**:

- Model: `vouch_history.go`
- SQL: `sql/exchange.sql`

---

### 2.4 工单和投诉模块

#### work_order - 工单管理

**路径**: `internal/service/work_order/`

**功能**:

- 工单创建
- 工单分配
- 工单处理
- 工单状态跟踪
- 工单评价
- 工单统计

**主要接口**:

- `/work_order/v1/*` - 工单相关接口

**关联组件**:

- Model: `work_order.go`
- DAO: 工单 DAO
- 测试: `internal/service/work_order/work_test.go`

---

#### complaint - 投诉处理

**路径**: `internal/service/complaint/`

**功能**:

- 投诉创建
- 投诉处理
- 投诉查询
- 未成年人退款
- 退款配置管理

**主要接口**:

- `/complaint/v1/*` - 投诉相关接口
- `/complaint/v1/refund/config/*` - 退款配置接口

**关联组件**:

- Model: `complaint.go`, `refund_underage_record.go`
- DAO: `complaint_dao.go`, `complaint_option_dao.go`

---

### 2.5 内容审核模块

#### content_audit - 内容审核

**路径**: `internal/service/content_audit/`

**功能**:

- 内容审核配置（队列、标签、处罚规则）
- 审核核心数据处理
- 审核任务管理
- 审核结果处理
- 处罚记录管理
- QA 过滤配置

**主要接口**:

- `/queue_config/*` - 队列配置
- `/tag_config/*` - 标签配置
- `/punishment_config/*` - 处罚配置
- `/qa_filter_config/*` - QA 过滤配置
- `/audit_core/*` - 审核核心
- `/audit_punishment/*` - 处罚记录

**关联组件**:

- Model: `model_content_audit/` 目录
- DAO: `internal/dao/dao_content_audit/` 目录
- Worker: `internal/worker/content_audit/` - 后台审核 Worker
- 子模块: `content-lib/` - 内容库（Git 子模块）

**审核流程**:

1. 内容提交到审核队列
2. Worker 从队列拉取任务
3. 人工审核或机器审核
4. 审核结果处理（通过/驳回）
5. 根据规则执行处罚

---

### 2.6 通知和消息模块

#### notify - 通知推送

**路径**: `internal/service/notify/`

**功能**:

- 通知创建
- 通知发送（站内信、邮件、短信）
- 通知查询
- 通知模板管理
- 通知推送记录

**主要接口**:

- `/notify/v1/*` - 通知相关接口
- `/api/customer-service/notify/*` - 通知服务注册

**关联组件**:

- Model: `notify.go`
- Worker: 通知发送 Worker
- External: `pkg/msg_server` - 消息服务 SDK

---

#### email - 邮件服务

**路径**: `internal/service/email/`

**功能**:

- 邮件发送
- 邮件模板管理
- 邮件记录查询
- 邮件状态跟踪

**主要接口**:

- `/email/v1/*` - 邮件相关接口

**关联组件**:

- Model: `email_record.go`, `email_sub_record.go`
- DAO: `email_record_dao.go`
- External: `pkg/email_server`, `pkg/smtp_util`

---

#### ai_help - AI 客服帮助

**路径**: `internal/service/ai_help/`

**功能**:

- AI 聊天日志管理
- AI 问题库管理
- AI 客服集成
- 聊天日志审核

**主要接口**:

- `/ai/v1/*` - AI 帮助相关接口
- `/ai/v1/chat_log/reviewed/push/` - 推送已审核聊天日志

**关联组件**:

- Model: `ai_chat_log.go`, `ai_question.go`
- External: `pkg/ai_help_server` - AI 帮助服务 SDK

---

### 2.7 VIP 管理模块

#### vip - VIP 管理

**路径**: `internal/service/vip/`

**功能**:

- VIP 用户管理
- VIP 等级管理
- VIP 权益配置
- VIP 记录查询
- VIP 统计

**主要接口**:

- `/vip/v1/*` - VIP 相关接口

**关联组件**:

- Model: `model_vip/` 目录
- Constants: `internal/constants/vip.go`
- External: `pkg/vip_admin` - VIP 管理 SDK

---

#### vip_scrm - VIP CRM 管理

**路径**: `internal/service/vip_scrm/`

**功能**:

- VIP 客户关系管理
- VIP 客户画像
- VIP 行为分析
- VIP 营销活动

**主要接口**:

- `/vip_scrm/v1/*` - VIP CRM 相关接口

**关联组件**:

- Model: `model_vip_scrm/` 目录

---

#### vip_white - VIP 白名单

**路径**: `internal/service/vip_white/`

**功能**:

- VIP 白名单管理
- 白名单添加/删除
- 白名单查询

**主要接口**:

- `/vip_white/v1/*` - VIP 白名单相关接口

**关联组件**:

- Model: `vip_white_record.go`

---

### 2.8 礼品和奖励模块

#### gift_code - 礼包码管理

**路径**: `internal/service/gift_code/`

**功能**:

- 礼包码生成
- 礼包码发放
- 礼包码兑换
- 礼包码查询
- 礼包码统计

**主要接口**:

- `/gift_code/v1/*` - 礼包码相关接口

**关联组件**:

- Model: `gift_code_record.go`, `model_gift_code/` 目录
- External: `pkg/gift_code_server` - 礼包码服务 SDK

---

### 2.9 注销和申诉模块

#### cancel - 注销服务

**路径**: `internal/service/cancel/`

**功能**:

- 账号注销申请
- 注销审核
- 注销记录查询
- 注销配置

**主要接口**:

- `/cancel/v1/*` - 注销相关接口

**关联组件**:

- Model: `account_cancel_record.go`
- DAO: `account_cancel_record_dao.go`

---

#### client_cancel - 客户端注销

**路径**: `internal/service/client_cancel/`

**功能**:

- 客户端注销流程
- 手机号验证码
- 签名验证
- 注销状态查询

**主要接口**:

- `/client_cancel/v2/*` - 客户端注销相关接口
- `/client_cancel/v2/check_sign/` - 验证签名
- `/client_cancel/v2/mobile_code/` - 获取验证码
- `/client_cancel/v2/check_status/` - 检查状态
- `/client_cancel/v2/save_info/` - 保存信息
- `/client_cancel/v2/remove/` - 取消申请

**关联组件**:

- Model: `account_cancel_record.go`

---

#### web_forbidden_appeal - Web 封禁申诉

**路径**: `internal/service/web_forbidden_appeal/`

**功能**:

- 封禁申诉提交
- 申诉处理
- 申诉查询
- 申诉记录管理

**主要接口**:

- `/api/customer-service/api/web_appeal/*` - 封禁申诉接口

**关联组件**:

- Model: `forbidden_appeal_record.go`, `forbidden.go`

---

### 2.10 运营和数据模块

#### operation - 运营管理

**路径**: `internal/service/operation/`

**功能**:

- 运营数据统计
- 运营活动管理
- 运营报表

**主要接口**:

- `/operation/v1/*` - 运营相关接口

---

#### dict - 字典管理

**路径**: `internal/service/dict/`

**功能**:

- 字典数据管理
- 字典查询
- 字典批量导入
- GA 事件字典管理

**主要接口**:

- `/dict/v1/*` - 字典相关接口
- `/dict/v1/dict/batch` - 批量导入事件字典

**关联组件**:

- Model: `dict.go`

---

#### query_tool - 查询工具

**路径**: `internal/service/query_tool/`

**功能**:

- 玩家数据查询
- 游戏数据查询
- 自定义查询
- 数据导出
- GDSS 玩币配置和查询

**主要接口**:

- `/query_tool/v2/*` - 查询工具接口
- `/query_tool/v2/gdss/play_coin/*` - GDSS 玩币查询

**关联组件**:

- Custom API: `pkg/custom/api` - 支持动态字段的查询工具 v2

---

### 2.11 Web 服务模块

#### web_basic - Web 基础服务

**路径**: `internal/service/web_basic/`

**功能**:

- Web 端基础服务
- 公共接口

**主要接口**:

- `/api/customer-service-api/web_basic/*` - Web 基础接口

---

#### web_game - Web 游戏服务

**路径**: `internal/service/web_game/`

**功能**:

- Web 端游戏相关服务
- 游戏数据查询

**主要接口**:

- `/api/customer-service-api/web_game/*` - Web 游戏接口

---

#### web_wechat_official - 微信公众号服务

**路径**: `internal/service/web_wechat_official/`

**功能**:

- 微信公众号集成
- 微信用户管理
- 微信消息推送
- 微信事件处理

**主要接口**:

- `/api/customer-service-api/web_wechat_official/*` - 微信公众号接口

**关联组件**:

- Model: `wechat_official.go`
- External: `pkg/wechat` - 微信 SDK

---

### 2.12 外部 API 模块

#### external_api - 外部 API

**路径**: `internal/service/external_api/`

**功能**:

- 第三方系统调用接口
- 外呼记录管理
- 呼叫中心坐席查询

**主要接口**:

- `/external/*` - 外部 API 接口
- `/tmp/v1/process/notice/` - 临时处理通知
- `/query_tool/v2/user/outbound/` - 添加外呼记录
- `/query_tool/v2/cticloud/monitor_agent/` - 获取坐席列表

**关联组件**:

- Model: `outbound_call_record.go`
- External: `pkg/cticloud` - 呼叫中心集成

---

### 2.13 其他模块

#### home - 首页服务

**路径**: `internal/service/home/`

**功能**:

- 首页数据聚合
- Dashboard 数据展示

**主要接口**:

- `/home/v1/*` - 首页相关接口

---

#### job_service - 定时任务服务

**路径**: `internal/service/job_service/`

**功能**:

- 定时任务管理
- 任务调度
- 任务执行记录

**主要接口**:

- `/job_service/v1/*` - 定时任务接口

**关联组件**:

- 定时任务: `internal/gcron/`

---

#### vn - 越南业务

**路径**: `internal/service/vn/`

**功能**:

- 越南市场特定业务
- 越南用户管理

**主要接口**:

- `/vn/v1/*` - 越南业务接口
- `/vn/v1/auth` - 越南用户认证

**关联组件**:

- Middleware: `jwt.VNJWT()` - 越南 JWT 中间件

---

#### common - 公共服务

**路径**: `internal/service/common/`

**功能**:

- 公共工具方法
- 通用业务逻辑

**主要接口**:

- `/common/v1/*` - 公共接口

---

## 3. 模块依赖关系

### 3.1 核心依赖

```yaml
所有 Service 模块
  ├─> DAO 层 (数据访问)
  │    └─> Model 层 (数据模型)
  ├─> pkg/* (外部服务集成)
  └─> util/* (工具函数)
```

### 3.2 外部服务依赖

| 模块 | 依赖的外部服务 | pkg 包 |
| ------ | -------------- | -------- |
| game | 游戏服务器 | game_server |
| email | 邮件服务 | email_server, smtp_util |
| sms | 短信服务 | sms |
| notify | 消息服务 | msg_server |
| invoice | 发票服务 | invoice_server |
| gift_code | 礼包码服务 | gift_code_server |
| item | 物品服务 | item_server |
| ai_help | AI 帮助服务 | ai_help_server |
| vip | VIP 管理 | vip_admin |
| cticloud | 呼叫中心 | cticloud |
| wechat | 微信 | wechat |
| dingtalk | 钉钉 | dingtalk |
| es | Elasticsearch | es |

## 4. 模块间通信

### 4.1 HTTP API

- 模块间通过 HTTP API 调用
- 使用 Gin 框架路由
- 支持 RESTful 风格

### 4.2 消息队列

- 使用 Kafka 进行异步通信
- 主要用于：
  - 内容审核任务
  - 通知推送
  - 数据同步

### 4.3 数据库共享

- 各模块共享数据库
- 通过事务保证数据一致性

## 5. 模块开发规范

### 5.1 新增模块步骤

1. **创建目录**: 在 `internal/service/` 下创建新模块目录
2. **定义 Model**: 在 `internal/model/` 下定义数据模型
3. **创建 DAO**: 在 `internal/dao/` 下创建数据访问层
4. **实现 Service**: 在模块目录下实现业务逻辑
5. **注册路由**: 在 `internal/api/server.go` 中注册路由
6. **编写测试**: 在模块目录下创建 `*_test.go` 文件
7. **生成文档**: 添加 Swagger 注解

### 5.2 代码规范

- 使用 Go 官方代码风格
- 函数命名遵循 Go 命名规范
- 添加必要的注释
- 错误处理要完善
- 避免循环依赖

### 5.3 测试规范

- 单元测试覆盖核心逻辑
- 使用 table-driven tests
- Mock 外部依赖
- 测试文件与源文件放在一起

## 6. 相关文档

- [系统架构文档](./ARCHITECTURE.md)
- [目录结构详解](./STRUCTURE.md)
- [数据模型文档](./MODELS.md)
- [API路由文档](./ROUTES.md)
- [配置和环境文档](./CONFIG.md)
- [开发指南](./DEVELOPMENT.md)
