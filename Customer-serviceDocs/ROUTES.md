# Customer-Service API 路由文档

## 1. 概述

Customer-Service 使用 Gin 框架构建 RESTful API，所有路由定义在 `internal/api/server.go` 和 `internal/api/api.go` 中。API 分为多个路由组，每组应用不同的中间件进行权限控制和限流。

## 2. 服务端口

- **主 API 服务**: 8010
- **API 服务**: 8010（共享端口，不同路由前缀）

## 3. 公共路由

### 3.1 健康检查

```yaml
GET /health
```

**说明**: 服务健康检查端点，返回 200 OK

---

### 3.2 Swagger 文档（仅开发环境）

```yaml
GET /swagger/*any
```

**说明**: Swagger API 文档访问地址
**示例**: <http://localhost:8010/swagger/index.html>

---

### 3.3 文档服务（仅开发环境）

```yaml
GET /docs/*
```

**说明**: 访问 Markdown 格式的 API 文档
**挂载路径**: `./docs/apis`

---

## 4. 路由分组详解

### 4.1 无认证路由组 (apiNoJwt)

**路由前缀**: `/api/customer-service`

**中间件**: 无

**说明**: 此路由组不需要 JWT 认证，包括登录接口、临时接口等

#### 4.1.1 管理员登录

```yaml
POST /api/customer-service/admin/v1/auth/
```

**Handler**: `admin.PostAuth`
**说明**: 管理员登录，返回 JWT Token

---

#### 4.1.2 越南用户认证

```yaml
POST /api/customer-service/vn/v1/auth
```

**Handler**: `admin.PostVNAuth`
**说明**: 越南市场用户认证

---

#### 4.1.3 临时系统接口

```yaml
GET  /api/customer-service/tmp/v1/login/
POST /api/customer-service/tmp/v1/create/
GET  /api/customer-service/tmp/v1/delete/
POST /api/customer-service/tmp/v1/process/notice/
```

**Handler**:

- `tmp.GetTmpLogin`
- `tmp.PostTmpCreate`
- `tmp.GetTmpDelete`
- `external_api.TmpProcessNotice`

**说明**: 临时系统相关接口

---

#### 4.1.4 版本查询

```yaml
GET /api/customer-service/tools/v1/version
```

**Handler**: `service.Version`
**说明**: 查询服务版本信息

---

#### 4.1.5 通知服务注册

```yaml
/api/customer-service/notify/* (由 Protobuf 生成)
```

**Handler**: `notify.Service{}`
**中间件**: `apiOnlyJwt` (需 JWT)
**说明**: 通知相关接口（Protobuf 生成）

---

#### 4.1.6 申诉解禁接口

```yaml
/api/customer-service/web_appeal/* (由 Protobuf 生成)
```

**Handler**: `web_forbidden_appeal.WebService{}`
**中间件**: `apiWebJwt` (Web 限流)
**说明**: 封禁申诉相关接口

---

#### 4.1.7 游戏服务器接口

```yaml
/api/customer-service/external_game/* (由 Protobuf 生成)
```

**Handler**: `external_game_api.Service{}`
**说明**: 游戏服务器调用的外部接口

---

#### 4.1.8 客户端注销接口

```yaml
POST /api/customer-service/client_cancel/v2/check_sign/
GET  /api/customer-service/client_cancel/v2/mobile_code/
GET  /api/customer-service/client_cancel/v2/check_status/
POST /api/customer-service/client_cancel/v2/save_info/
POST /api/customer-service/client_cancel/v2/remove/
```

**Handler**: `client_cancel`
**说明**: 客户端账号注销流程接口

---

#### 4.1.9 外呼记录和坐席查询

```yaml
POST /api/customer-service/query_tool/v2/user/outbound/
GET  /api/customer-service/query_tool/v2/cticloud/monitor_agent/
```

**Handler**: `external_api`
**说明**: 外呼记录管理和坐席监控

---

#### 4.1.10 字典批量导入

```yaml
POST /api/customer-service/dict/v1/dict/batch
```

**Handler**: `dict.BatchAddEventDict`
**说明**: 批量导入 GA 事件字典

---

#### 4.1.11 AI 聊天日志推送

```yaml
POST /api/customer-service/ai/v1/chat_log/reviewed/push/
```

**Handler**: `ai_help.PushReviewedChatLog`
**说明**: 推送已审核的 AI 聊天日志

---

#### 4.1.12 GDSS 玩币配置

```yaml
POST /api/customer-service/query_tool/v2/gdss/play_coin/config/
POST /api/customer-service/query_tool/v2/gdss/play_coin/
POST /api/customer-service/query_tool/v2/gdss/play_coin/download/
```

**Handler**: `query_tool`
**说明**: GDSS 玩币配置和查询接口

---

#### 4.1.13 退款配置

```yaml
GET  /api/customer-service/complaint/v1/refund/config/dropdown/
POST /api/customer-service/complaint/v1/refund/config/project/
POST /api/customer-service/complaint/v1/refund/config/common/
```

**Handler**: `complaint`
**说明**: 未成年人退款配置管理

---

### 4.2 JWT 认证路由组 (apiOnlyJwt)

**路由前缀**: `/api/customer-service`

**中间件**:

- `jwt.JWT()` - JWT Token 验证
- `guarder.RequireURLPermission` - URL 权限验证

**说明**: 需要 JWT 认证的路由，用于管理后台

#### 4.2.1 用户管理

```yaml
/api/customer-service/user/* (由 Protobuf 生成)
```

**Handler**: `admin.UserService{}`
**说明**: 用户 CRUD 操作

---

#### 4.2.2 角色管理

```yaml
/api/customer-service/role/* (由 Protobuf 生成)
```

**Handler**: `admin.RoleService{}`
**说明**: 角色 CRUD 操作

---

#### 4.2.3 权限管理

```yaml
/api/customer-service/permission/* (由 Protobuf 生成)
```

**Handler**: `admin.PermissionService{}`
**说明**: 权限管理接口

---

#### 4.2.4 项目管理

```yaml
/api/customer-service/project/* (由 Protobuf 生成)
GET /api/customer-service/admin/v1/project/config/
```

**Handler**:

- `admin.ProjectService{}`
- `admin.GetProjectConfig`

**说明**: 项目管理和配置查询

---

#### 4.2.5 首页服务

```yaml
/api/customer-service/home/* (由 Protobuf 生成)
```

**Handler**: `home.Service{}`
**说明**: 首页数据和 Dashboard

---

#### 4.2.6 定时任务服务

```yaml
/api/customer-service/job_service/* (由 Protobuf 生成)
```

**Handler**: `job_service.Service{}`
**说明**: 定时任务管理

---

#### 4.2.7 公共服务

```yaml
/api/customer-service/common/* (由 Protobuf 生成)
```

**Handler**: `common.Service{}`
**说明**: 公共工具接口

---

### 4.3 JWT + 项目权限路由组 (projectJwt)

**路由前缀**: `/api/customer-service`

**中间件**:

- `jwt.JWT()` - JWT Token 验证
- `guarder.RequireURLPermission` - URL 权限验证
- `project_permission.RequireProjectPermission()` - 项目权限验证
- `action_record.LogParams()` - 记录请求参数

**说明**: 需要认证和项目权限的完整业务路由

#### 4.3.1 订单管理

```yaml
/api/customer-service/order_manage/* (由 Protobuf 生成)
```

**Handler**: `order_manage.Service{}`
**说明**: 订单查询和管理

---

#### 4.3.2 查询工具

```yaml
/api/customer-service/query_tool/* (由 Protobuf 生成)
```

**Handler**: `query_tool.Service{}`
**说明**: 数据查询工具

---

#### 4.3.3 查询工具 v2 (支持动态字段)

```yaml
/api/customer-service/query_tool_v2/* (由 Protobuf 生成)
```

**Handler**: `query_tool.Service{}`
**注册**: `customapi.RegisterQueryToolV2HttpHandler`
**说明**: 支持动态字段的查询工具 v2

---

#### 4.3.4 字典管理

```yaml
/api/customer-service/dict/* (由 Protobuf 生成)
```

**Handler**: `dict.Service{}`
**说明**: 字典数据管理

---

#### 4.3.5 GM 工具

```yaml
/api/customer-service/gm/* (由 Protobuf 生成)
```

**Handler**: `gm.Service{}`
**说明**: GM 工具相关接口

---

#### 4.3.6 支付服务

```yaml
/api/customer-service/pay/* (由 Protobuf 生成)
```

**Handler**: `pay.Service{}`
**说明**: 支付相关接口

---

#### 4.3.7 投诉处理

```yaml
/api/customer-service/complaint/* (由 Protobuf 生成)
```

**Handler**: `complaint.Service{}`
**说明**: 投诉处理接口

---

#### 4.3.8 注销服务

```yaml
/api/customer-service/cancel/* (由 Protobuf 生成)
```

**Handler**: `cancel.Service{}`
**说明**: 账号注销管理

---

#### 4.3.9 邮件服务

```yaml
/api/customer-service/email/* (由 Protobuf 生成)
```

**Handler**: `email.Service{}`
**说明**: 邮件发送和管理

---

#### 4.3.10 工单管理

```yaml
/api/customer-service/work_order/* (由 Protobuf 生成)
```

**Handler**: `work_order.Service{}`
**说明**: 工单管理接口

---

#### 4.3.11 礼包码管理

```yaml
/api/customer-service/gift_code/* (由 Protobuf 生成)
```

**Handler**: `gift_code.Service{}`
**说明**: 礼包码管理

---

#### 4.3.12 AI 帮助服务

```yaml
/api/customer-service/ai_help/* (由 Protobuf 生成)
```

**Handler**: `ai_help.Service{}`
**说明**: AI 客服帮助

---

#### 4.3.13 发票管理

```yaml
/api/customer-service/invoice/* (由 Protobuf 生成)
```

**Handler**: `invoice.Service{}`
**说明**: 发票管理接口

---

#### 4.3.14 兑换码管理

```yaml
/api/customer-service/exchange/* (由 Protobuf 生成)
```

**Handler**: `exchange.Service{}`
**说明**: 兑换码管理

---

#### 4.3.15 内容审核配置

```yaml
/api/customer-service/queue_config/* (由 Protobuf 生成)
/api/customer-service/tag_config/* (由 Protobuf 生成)
/api/customer-service/punishment_config/* (由 Protobuf 生成)
/api/customer-service/qa_filter_config/* (由 Protobuf 生成)
```

**Handler**: `content_audit.ConfigService{}`
**说明**: 内容审核配置（队列、标签、处罚、QA 过滤）

---

#### 4.3.16 审核核心

```yaml
/api/customer-service/audit_core/* (由 Protobuf 生成)
```

**Handler**: `content_audit.AuditCoreService{}`
**说明**: 审核核心数据处理

---

#### 4.3.17 审核处罚记录

```yaml
/api/customer-service/audit_punishment/* (由 Protobuf 生成)
```

**Handler**: `content_audit.AuditPunishmentService{}`
**说明**: 处罚记录管理

---

#### 4.3.18 运营管理

```yaml
/api/customer-service/operation/* (由 Protobuf 生成)
```

**Handler**: `operation.Service{}`
**说明**: 运营数据管理

---

#### 4.3.19 VIP 管理

```yaml
/api/customer-service/vip/* (由 Protobuf 生成)
```

**Handler**: `vip.Service{}`
**中间件**: 额外添加 `LimitBody()` (请求体限制 100MB)
**说明**: VIP 管理接口

---

#### 4.3.20 VIP 白名单

```yaml
/api/customer-service/vip_white/* (由 Protobuf 生成)
```

**Handler**: `vip_white.Service{}`
**中间件**: `LimitBody()`
**说明**: VIP 白名单管理

---

#### 4.3.21 VIP CRM

```yaml
/api/customer-service/vip_scrm/* (由 Protobuf 生成)
```

**Handler**: `vip_scrm.Service{}`
**中间件**: `LimitBody()`
**说明**: VIP 客户关系管理

---

### 4.4 签名验证路由组 (apiSign)

**路由前缀**: `/api/customer-service`

**中间件**:

- `sign_verify.SignVerify()` - 签名验证

**说明**: 用于直播系统等第三方调用，通过签名验证而非 JWT

#### 4.4.1 外部服务接口

```yaml
/api/customer-service/external/* (由 Protobuf 生成)
```

**Handler**: `external_api.Service{}`
**说明**: 第三方系统调用接口

---

### 4.5 越南 JWT 路由组 (apiVNJwt)

**路由前缀**: `/api/customer-service`

**中间件**:

- `jwt.VNJWT()` - 越南市场专用 JWT 验证

**说明**: 越南市场专用路由

#### 4.5.1 越南业务

```yaml
/api/customer-service/vn/* (由 Protobuf 生成)
```

**Handler**: `vn.Service{}`
**说明**: 越南市场业务接口

---

### 4.6 Web 限流路由组 (apiWebJwt)

**路由前缀**: `/api/customer-service`

**中间件**:

- `web_limit.WebLimit()` - Web 端限流（IP 限制、请求频率限制、请求大小限制）

**说明**: 用于 Web 端调用的接口，有严格的限流控制

#### 4.6.1 Web 基础服务

```yaml
/api/customer-service-api/web_basic/* (由 Protobuf 生成)
```

**Handler**: `web_basic.WebService{}`
**说明**: Web 端基础服务

---

#### 4.6.2 申诉解禁

```yaml
/api/customer-service-api/web_appeal/* (由 Protobuf 生成)
```

**Handler**: `web_forbidden_appeal.WebService{}`
**说明**: 封禁申诉 Web 接口

---

### 4.7 Web JWT 路由组 (apiWebLogin)

**路由前缀**: `/api/customer-service-api`

**中间件**:

- `web_limit.JWT()` - Web JWT 验证

**说明**: Web 端需要 JWT 认证的路由

#### 4.7.1 Web 用户管理

```yaml
/api/customer-service-api/web_user_manage/* (由 Protobuf 生成)
```

**Handler**: `web_user_manage.WebService{}`
**说明**: Web 端用户管理

---

### 4.8 Web 游戏路由组 (apiLogin)

**路由前缀**: `/api/customer-service-api`

**中间件**: 无特殊中间件

**说明**: Web 端游戏相关接口

#### 4.8.1 Web 游戏服务

```yaml
/api/customer-service-api/web_game/* (由 Protobuf 生成)
```

**Handler**: `web_game.WebService{}`
**说明**: Web 端游戏服务

---

#### 4.8.2 代理转发

```yaml
POST /api/customer-service-api/proxy
ANY  /api/customer-service-api/proxy
```

**Handler**: `web_game.ForwardRequest`
**说明**: 代理转发请求

---

#### 4.8.3 发票通知回调

```yaml
POST /api/customer-service-api/invoice/notify
```

**Handler**: `game.InvoiceNotifyHandler`
**说明**: 发票系统通知回调

---

### 4.9 微信路由组 (apiWx)

**路由前缀**: `/api/customer-service-api`

**中间件**:

- `web_limit.JWT()` - JWT 验证
- `web_limit.WxLimit()` - 微信专用限流

**说明**: 微信公众号相关接口

#### 4.9.1 微信公众号服务

```yaml
/api/customer-service-api/web_wechat_official/* (由 Protobuf 生成)
```

**Handler**: `web_wechat_official.WebService{}`
**说明**: 微信公众号接口

---

### 4.10 API 服务无认证路由组 (apiNoJwt - API Server)

**路由前缀**: `/api/customer-service-api`

**中间件**: 无

**说明**: API 服务器的无认证路由

#### 4.10.1 版本查询

```yaml
GET /api/customer-service-api/tools/v1/version
```

**Handler**: `service.Version`
**说明**: 查询 API 服务版本

---

#### 4.10.2 临时通知处理

```yaml
POST /api/customer-service-api/tmp/v1/process/notice/
```

**Handler**: `external_api.TmpProcessNotice`
**说明**: 临时处理通知

---

### 4.11 API 服务限流路由组 (apiWebJwt - API Server)

**路由前缀**: `/api/customer-service-api`

**中间件**: `web_limit.WebLimit()`

**说明**: API 服务器的限流路由

#### 4.11.1 通知服务

```yaml
/api/customer-service-api/notify/* (由 Protobuf 生成)
```

**Handler**: `notify.Service{}`
**说明**: 通知推送接口

---

## 5. 中间件详解

### 5.1 JWT 中间件

**路径**: `middleware/jwt/`

**功能**:

- 验证请求头中的 JWT Token
- 提取 Token 中的用户信息
- 将用户信息注入到上下文

**使用方式**:

```go
apiJwt := engine.Group("/api/customer-service", jwt.JWT())
```

**越南专用 JWT**:

```go
apiVNJwt := engine.Group("/api/customer-service", jwt.VNJWT())
```

---

### 5.2 CORS 中间件

**路径**: `middleware/cors/`

**功能**:

- 处理跨域请求
- 添加 CORS 响应头

**说明**: 全局应用

---

### 5.3 恢复中间件

**路径**: `middleware/recovery/`

**功能**:

- 捕获 panic 异常
- 返回统一的错误响应
- 记录错误日志

**说明**: 全局应用，在最顶层

---

### 5.4 项目权限中间件

**路径**: `middleware/project_permission/`

**功能**:

- 验证用户是否有访问指定项目的权限
- 从 Token 中提取项目信息
- 检查用户权限列表

**使用方式**:

```go
projectJwt := engine.Group("/api/customer-service", 
    jwt.JWT(), 
    guarder.RequireURLPermission,
    project_permission.RequireProjectPermission()
)
```

---

### 5.5 行为记录中间件

**路径**: `middleware/action_record/`

**功能**:

- 记录用户请求参数
- 记录操作日志
- 用于审计和追溯

**使用方式**:

```go
projectJwt.Use(action_record.LogParams())
```

---

### 5.6 签名验证中间件

**路径**: `middleware/sign_verify/`

**功能**:

- 验证请求签名
- 防止请求被篡改
- 用于第三方系统调用

**使用方式**:

```go
apiSign := engine.Group("/api/customer-service", sign_verify.SignVerify())
```

---

### 5.7 Web 限流中间件

**路径**: `middleware/web_limit/`

**功能**:

- IP 限流
- 请求频率限制
- 请求大小限制
- Web JWT 验证
- 微信专用限流

**使用方式**:

```go
apiWebJwt := engine.Group("/api/customer-service", web_limit.WebLimit())
apiWx := engine.Group("/api/customer-service-api", 
    web_limit.JWT(), 
    web_limit.WxLimit()
)
```

---

### 5.8 URL 权限中间件

**路径**: `guarder.RequireURLPermission`

**功能**:

- 验证用户是否有访问 URL 的权限
- 基于角色的访问控制 (RBAC)

**说明**: 来自 `tygit.tuyoo.com/gocomponents/guarder`

---

### 5.9 请求体限制中间件

**功能**:

- 限制请求体最大为 100MB
- 防止大文件攻击

**使用方式**:

```go
projectJwt.Use(LimitBody())

func LimitBody() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, 100*1024*1024)
        c.Next()
    }
}
```

---

## 6. Protobuf 生成的路由

大部分业务路由通过 Protobuf 定义自动生成，存放在 `pkg/gen/api/` 目录。

### 6.1 生成流程

1. 在 `proto/http/` 目录下定义 `.proto` 文件
2. 运行 `make gen` 命令
3. 生成 Go 代码和路由 Handler
4. 在 `server.go` 中注册 Handler

### 6.2 注册示例

```go
api.RegisterUserServiceHttpHandler(apiJwt, admin.UserService{})
api.RegisterWorkOrderServiceHttpHandler(projectJwt, work_order.Service{})
```

---

## 7. 响应格式

### 7.1 成功响应

```json
{
    "code": 0,
    "message": "success",
    "data": {
        // 业务数据
    }
}
```

### 7.2 错误响应

```json
{
    "code": 1001,
    "message": "参数错误",
    "data": null
}
```

---

## 8. 常见状态码

| 状态码 | 说明 |
| -------- | ------ |
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 未登录 |
| 1003 | 权限不足 |
| 1004 | Token 过期 |
| 1005 | 签名验证失败 |
| 2001 | 业务错误 |
| 5000 | 服务器内部错误 |

---

## 9. 路由命名规范

### 9.1 RESTful 风格

- 获取列表: `GET /resource/`
- 获取详情: `GET /resource/:id`
- 创建: `POST /resource/`
- 更新: `PUT /resource/:id`
- 删除: `DELETE /resource/:id`

### 9.2 版本控制

- v1 版本: `/v1/`
- v2 版本: `/v2/`

### 9.3 路由前缀

- 管理后台: `/admin/`
- 用户操作: `/user/`
- 工具类: `/tools/`
- 查询类: `/query_tool/`

---

## 10. 相关文档

- [系统架构文档](./ARCHITECTURE.md)
- [目录结构详解](./STRUCTURE.md)
- [核心模块说明](./MODULES.md)
- [数据模型文档](./MODELS.md)
- [配置和环境文档](./CONFIG.md)
- [开发指南](./DEVELOPMENT.md)
