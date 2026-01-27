# Customer-Service 配置和环境文档

## 1. 概述

Customer-Service 使用 YAML 格式的配置文件，配置文件位于 `internal/conf/` 目录。系统支持多环境配置，通过环境变量或配置文件切换。

## 2. 配置文件结构

### 2.1 主配置文件

**文件路径**: `internal/conf/cfg.yaml`

**配置结构**:

```yaml
app:
  page_size: 10
  jwt_secret: "2334456"
  casbin_model_path: "./conf/model.conf"
  domain_server: ""
  domain_client: ""
  super_username: "xuqingsong"
  ding_web_hook: ""
  ding_secret: ""

mysql:
  host: "hostname"
  port: 3306
  user: "username"
  password: "password"
  database: "database_name"

anti_addiction:
  access:
    - cloud_id: "3"
      access_id: "xxx"
      secret_key: "xxx"

sdk_access:
  - cloud_id: "1"
    access_id: "xxx"
    secret_key: "xxx"
```

---

## 3. 配置项详解

### 3.1 app - 应用配置

| 配置项 | 类型 | 说明 | 示例 |
| -------- | ------ | ------ | ------ |
| page_size | int | 分页大小，默认每页显示数量 | 10 |
| jwt_secret | string | JWT Token 签名密钥 | "2334456" |
| casbin_model_path | string | Casbin 权限模型文件路径 | "./conf/model.conf" |
| domain_server | string | 服务端域名 | "" |
| domain_client | string | 客户端域名 | "" |
| super_username | string | 超级管理员用户名 | "xuqingsong" |
| ding_web_hook | string | 钉钉 Webhook 地址 | "" |
| ding_secret | string | 钉钉签名密钥 | "" |

**说明**:

- `jwt_secret` 生产环境必须使用强密码
- `casbin_model_path` 指向 Casbin 权限模型文件
- `ding_web_hook` 和 `ding_secret` 用于钉钉通知

---

### 3.2 mysql - MySQL 数据库配置

| 配置项 | 类型 | 说明 | 示例 |
| -------- | ------ | ------ | ------ |
| host | string | 数据库主机地址 | "localhost" |
| port | int | 数据库端口 | 3306 |
| user | string | 数据库用户名 | "root" |
| password | string | 数据库密码 | "password" |
| database | string | 数据库名称 | "customer_service" |

**说明**:

- 支持主从配置（如果配置了读写分离）
- 连接池大小在代码中配置
- 生产环境建议使用环境变量管理敏感信息

---

### 3.3 anti_addiction - 防沉迷配置

**配置项**: `anti_addiction.access` 数组

每个元素包含:

| 配置项 | 类型 | 说明 |
| -------- | ------ | ------ |
| cloud_id | string | 云 ID（项目标识） |
| access_id | string | 访问 ID |
| secret_key | string | 密钥 |

**示例**:

```yaml
anti_addiction:
  access:
    - cloud_id: "3"
      access_id: "15e0d56b999a2394"
      secret_key: "tZP01TGVtyNNSj4yLKmhQjFwjcsqlNzR"
```

**说明**:

- 每个项目（cloud_id）对应一组访问凭证
- 用于调用防沉迷系统的接口
- 支持多项目配置

---

### 3.4 sdk_access - SDK 访问配置

**配置项**: `sdk_access` 数组

每个元素包含:

| 配置项 | 类型 | 说明 |
| -------- | ------ | ------ |
| cloud_id | string | 云 ID（项目标识） |
| access_id | string | 访问 ID |
| secret_key | string | 密钥 |

**示例**:

```yaml
sdk_access:
  - cloud_id: "1"
    access_id: "wa15a79da9101b3ac6"
    secret_key: "9kQLYmnEaTYjhubOo2IelCvNtwBXX0ST"
```

**说明**:

- 用于游戏服务器 SDK 认证
- 支持多项目配置
- 与 `anti_addiction` 类似，但用于不同的服务

---

## 4. 配置加载

### 4.1 配置初始化

**代码位置**: `internal/conf/init.go`

```go
func InitConfig() error {
    // 读取配置文件
    config, err := os.ReadFile("internal/conf/cfg.yaml")
    if err != nil {
        return err
    }
    
    // 解析 YAML
    if err := yaml.Unmarshal(config, &Config); err != nil {
        return err
    }
    
    return nil
}
```

### 4.2 配置监听器

**代码位置**: `internal/conf/config_listener.go`

**功能**:

- 监听配置文件变化
- 热更新配置（不需要重启服务）
- 支持动态配置更新

---

## 5. 环境配置

### 5.1 开发环境

**配置文件**: `internal/conf/cfg.yaml`

**特点**:

- 使用本地数据库
- 日志级别为 Debug
- 启用 Swagger 文档
- 启用性能分析（pprof）

**启动方式**:

```bash
go run main.go
```

---

### 5.2 测试环境

**配置文件**: `internal/conf/cfg.test.yaml`

**特点**:

- 使用测试数据库
- 日志级别为 Info
- 启用 Swagger 文档
- 可能启用部分监控

**启动方式**:

```bash
ENV=test go run main.go
```

---

### 5.3 生产环境

**配置文件**: `internal/conf/cfg.prod.yaml`

**特点**:

- 使用生产数据库
- 日志级别为 Warn 或 Error
- 禁用 Swagger 文档
- 禁用性能分析
- 启用所有监控和告警

**启动方式**:

```bash
ENV=prod go run main.go
```

**部署方式**:

- 使用 Docker 容器
- 通过环境变量注入配置
- Kubernetes ConfigMap 管理

---

## 6. 环境变量

### 6.1 系统环境变量

| 变量名 | 说明 | 示例 |
| -------- | ------ | ------ |
| ENV | 运行环境 | dev/test/prod |
| PORT | 服务端口 | 8010 |
| LOG_LEVEL | 日志级别 | debug/info/warn/error |

### 6.2 数据库环境变量

| 变量名 | 说明 | 示例 |
| -------- | ------ | ------ |
| DB_HOST | 数据库主机 | localhost |
| DB_PORT | 数据库端口 | 3306 |
| DB_USER | 数据库用户名 | root |
| DB_PASSWORD | 数据库密码 | password |
| DB_NAME | 数据库名称 | customer_service |

**优先级**: 环境变量 > 配置文件 > 默认值

---

## 7. 配置管理最佳实践

### 7.1 敏感信息管理

**不要**:

- ❌ 将密码、密钥等敏感信息提交到 Git
- ❌ 在配置文件中使用明文密码

**应该**:

- ✅ 使用环境变量管理敏感信息
- ✅ 使用密钥管理系统（如 Kubernetes Secrets）
- ✅ 生产环境使用加密配置

---

### 7.2 配置文件命名

```bash
internal/conf/
├── cfg.yaml              # 默认配置（开发环境）
├── cfg.test.yaml         # 测试环境配置
├── cfg.prod.yaml         # 生产环境配置
└── model.conf            # Casbin 权限模型
```

---

### 7.3 配置验证

在启动时验证配置项:

```go
func ValidateConfig() error {
    if Config.MySQL.Host == "" {
        return errors.New("mysql host is required")
    }
    if Config.App.JwtSecret == "" {
        return errors.New("jwt secret is required")
    }
    return nil
}
```

---

## 8. 特殊配置模块

### 8.1 充值类型配置

**文件**: `internal/conf/charge_type.go`

**功能**:

- 定义充值类型
- 配置充值规则
- 关联支付渠道

---

### 8.2 客户端 ID 配置

**文件**: `internal/conf/client_id.go`

**功能**:

- 管理客户端 ID 映射
- 支持多客户端
- 客户端认证配置

---

### 8.3 云 ID 配置

**文件**: `internal/conf/conf_cloud_id.go`

**功能**:

- 云 ID（项目 ID）管理
- 项目与云 ID 的映射
- 多项目支持

---

### 8.4 CRM 配置

**文件**: `internal/conf/crm_config.go`

**功能**:

- CRM 系统集成配置
- 数据同步配置
- CRM API 配置

---

### 8.5 礼包码配置

**文件**: `internal/conf/gift_code_config.go`

**功能**:

- 礼包码规则配置
- 奖励配置
- 使用限制配置

---

### 8.6 SNS 配置

**文件**: `internal/conf/sns.go`

**功能**:

- 社交媒体集成配置
- 第三方登录配置
- 消息推送配置

---

### 8.7 Worker 配置

**文件**: `internal/conf/worker.go`

**功能**:

- 后台任务 Worker 配置
- 任务队列配置
- 并发控制配置

---

## 9. 配置热更新

### 9.1 配置监听器

**功能**:

- 监听配置文件变化
- 自动重新加载配置
- 不影响正在处理的请求

**实现**:

```go
func StartConfigListener() {
    watcher, err := fsnotify.NewWatcher()
    if err != nil {
        log.Fatal(err)
    }
    
    err = watcher.Add("internal/conf/cfg.yaml")
    if err != nil {
        log.Fatal(err)
    }
    
    go func() {
        for {
            select {
            case event, ok := <-watcher.Events:
                if !ok {
                    return
                }
                if event.Op&fsnotify.Write == fsnotify.Write {
                    ReloadConfig()
                }
            }
        }
    }()
}
```

---

## 10. 部署配置

### 10.1 Docker 配置

**Dockerfile**: `build/Dockerfile.customer-service`

```dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY . .
RUN go mod download
RUN go build -o customer-service main.go

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/customer-service .
COPY internal/conf/cfg.yaml internal/conf/
EXPOSE 8010
CMD ["./customer-service"]
```

---

### 10.2 Kubernetes 配置

**ConfigMap 示例**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: customer-service-config
data:
  cfg.yaml: |
    app:
      page_size: 10
      jwt_secret: "${JWT_SECRET}"
    mysql:
      host: "${DB_HOST}"
      port: 3306
      user: "${DB_USER}"
      password: "${DB_PASSWORD}"
      database: "${DB_NAME}"
```

**Secret 示例**:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: customer-service-secret
type: Opaque
stringData:
  JWT_SECRET: "your-secret-key"
  DB_PASSWORD: "your-db-password"
```

---

## 11. 配置调试

### 11.1 查看当前配置

```go
func PrintConfig() {
    fmt.Printf("App Config: %+v\n", Config.App)
    fmt.Printf("MySQL Config: %+v\n", Config.MySQL)
}
```

### 11.2 配置验证

启动时验证所有必需配置项:

```go
func main() {
    if err := conf.InitConfig(); err != nil {
        log.Fatal("Failed to load config:", err)
    }
    
    if err := conf.ValidateConfig(); err != nil {
        log.Fatal("Config validation failed:", err)
    }
    
    // 启动服务
}
```

---

## 12. 常见问题

### 12.1 配置文件找不到

**错误**: `open internal/conf/cfg.yaml: no such file or directory`

**解决**:

- 确保配置文件路径正确
- 检查工作目录是否正确
- 使用绝对路径或相对路径

---

### 12.2 JWT Secret 为空

**错误**: `jwt secret is required`

**解决**:

- 在配置文件中设置 `jwt_secret`
- 或使用环境变量 `JWT_SECRET`

---

### 12.3 数据库连接失败

**错误**: `failed to connect to database`

**解决**:

- 检查数据库配置（host, port, user, password）
- 确认数据库服务是否运行
- 检查网络连接

---

## 13. 相关文档

- [系统架构文档](./ARCHITECTURE.md)
- [目录结构详解](./STRUCTURE.md)
- [核心模块说明](./MODULES.md)
- [数据模型文档](./MODELS.md)
- [API路由文档](./ROUTES.md)
- [开发指南](./DEVELOPMENT.md)
