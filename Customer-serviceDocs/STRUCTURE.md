# Customer-Service 目录结构详解

## 1. 根目录结构

```yaml
customer-service/
├── main.go                    # 程序入口点
├── go.mod                     # Go 模块依赖定义
├── go.sum                     # Go 模块依赖锁定
├── makefile                   # 构建和开发命令集合
├── Jenkinsfile                # CI/CD 配置
├── Dockerfile                 # Docker 镜像构建配置
├── .gitignore                 # Git 忽略规则
├── .gitmodules                # Git 子模块配置
├── README.md                  # 项目说明文档
├── AGENTS.md                  # 仓库开发指南
├── customer-audit.md          # 审核相关说明
│
├── cmd/                       # 命令行工具和启动脚本
├── internal/                  # 系统内部模块（私有代码）
├── middleware/                # HTTP 中间件
├── pkg/                       # 可重用的公共包
├── proto/                     # Protobuf 定义文件
├── docs/                      # 自动生成的文档
├── util/                      # 工具函数库
├── sql/                       # SQL 脚本
├── scripts/                   # 脚本工具
├── tools/                     # 编译工具和二进制文件
├── build/                     # 构建相关文件
├── run/                       # 运行时文件（日志等）
└── content-lib/               # 内容库子模块（Git 子模块）
```

## 2. 核心目录详解

### 2.1 cmd/ - 命令行工具和启动脚本

**功能**: 提供程序启动入口和命令行工具

```yaml
cmd/
├── root.go                    # Cobra 命令根定义
├── api.go                     # API 服务启动命令
├── permission/                # 权限管理工具
│   └── main.go                # 权限数据处理脚本
└── client_permission/         # 客户端权限工具
    └── main.go                # 客户端权限规范脚本
```

**说明**:

- 使用 Cobra 框架构建命令行界面
- `root.go` 定义主命令结构和子命令
- `permission/` 用于生成和维护权限数据
- `client_permission/` 处理客户端权限相关逻辑

### 2.2 internal/ - 内部业务模块

**功能**: 包含所有内部业务逻辑，不对外暴露

```yaml
internal/
├── run.go                     # 服务启动和生命周期管理
├── api/                       # HTTP API 服务器
├── service/                   # 业务服务层
├── dao/                       # 数据访问层
├── model/                     # 数据模型层
├── conf/                      # 配置管理
├── module/                    # 模块定义
├── constants/                 # 常量定义
├── worker/                    # 后台任务 Worker
├── rdb/                       # Redis 操作
├── ga/                        # 统计分析相关
├── gcron/                     # 定时任务
└── tools/                     # 内部工具
```

#### 2.2.1 internal/api/ - API 服务器

```yaml
internal/api/
├── server.go                  # 主 API 服务器（端口 8010）
└── api.go                     # 专用 API 服务器
```

**说明**:

- `server.go`: 注册所有业务路由和中间件
- `api.go`: 处理特定业务场景的 API 调用
- 使用 Gin 框架构建 RESTful API
- 支持 Swagger 文档自动生成

#### 2.2.2 internal/service/ - 业务服务层

**功能**: 实现各业务域的业务逻辑

```yaml
internal/service/
├── common.go                  # 公共服务
├── tools.go                   # 工具服务
│
├── admin/                     # 用户和权限管理
├── ai_help/                   # AI 客服帮助
├── cancel/                    # 注销服务
├── client_cancel/             # 客户端注销服务
├── common/                    # 公共服务
├── complaint/                 # 投诉处理
├── content_audit/            # 内容审核
├── dict/                     # 字典管理
├── email/                    # 邮件服务
├── exchange/                 # 兑换码管理
├── external_api/             # 外部 API 接口
├── external_game_api/        # 游戏服务器外部接口
├── game/                     # 游戏相关
├── gift_code/                # 礼包码管理
├── gm/                       # GM 工具
├── home/                     # 首页服务
├── invoice/                  # 发票管理
├── job_service/              # 定时任务服务
├── notify/                   # 通知推送
├── operation/                # 运营管理
├── order_manage/             # 订单管理
├── pay/                      # 支付服务
├── query_tool/               # 查询工具
├── vip/                      # VIP 管理
├── vip_scrm/                 # VIP CRM 管理
├── vip_white/                # VIP 白名单
├── vn/                       # 越南业务
├── web_basic/                # Web 基础服务
├── web_forbidden_appeal/     # 封禁申诉
├── web_game/                 # Web 游戏服务
├── web_user_manage/          # Web 用户管理
├── web_wechat_official/      # 微信公众号服务
└── work_order/               # 工单管理
```

**主要职责**:

- 接收 HTTP 请求参数
- 执行业务逻辑处理
- 调用 DAO 层进行数据操作
- 调用 pkg 中的外部服务集成
- 返回格式化的响应数据

#### 2.2.3 internal/dao/ - 数据访问层

**功能**: 封装数据库操作，提供 CRUD 接口

```yaml
internal/dao/
├── account_cancel_record_dao.go      # 账号注销记录
├── anti_rent_operate_record.go        # 反代租操作记录
├── batch_supplement_order_record_dao.go  # 批量补单记录
├── change_password_record_dao.go      # 修改密码记录
├── complaint_dao.go                    # 投诉 DAO
├── complaint_option_dao.go             # 投诉选项 DAO
├── dao_item_modify/                   # 物品修改 DAO
│   └── item_dao.go
├── dao_content_audit/                 # 内容审核 DAO
│   ├── audit_punishment_dao.go
│   └── ...
└── ... (其他 DAO 文件)
```

**主要职责**:

- 封装 GORM 数据库操作
- 提供复杂查询方法
- 管理数据库事务
- 数据验证和转换

#### 2.2.4 internal/model/ - 数据模型层

**功能**: 定义数据库表结构和业务实体

```yaml
internal/model/
├── account_cancel_record.go           # 账号注销记录模型
├── ai_chat_log.go                      # AI 聊天日志
├── ai_question.go                      # AI 问题
├── anti_rent_operate_record.go         # 反代租操作记录
├── batch_supplement_order.go           # 批量补单
├── channel_bind.go                     # 渠道绑定
├── complaint.go                        # 投诉模型
├── dict.go                             # 字典模型
├── email_record.go                     # 邮件记录
├── email_sub_record.go                 # 邮件子记录
├── forbidden_appeal_record.go          # 封禁申诉记录
├── forbidden.go                        # 封禁模型
├── gift_code_record.go                 # 礼包码记录
├── init.go                             # 模型初始化
├── item_record.go                      # 物品记录
├── jp_real_name_operate_record.go      # 日本实名操作记录
├── mobile_bind_record.go               # 手机绑定记录
├── model.go                            # 基础模型定义
├── mongo_cdc_order.go                  # MongoDB CDC 订单
├── notify.go                           # 通知模型
├── outbound_call_record.go             # 外呼记录
├── pay_risk_strategy_records.go       # 支付风控策略记录
├── project.go                          # 项目模型
├── refund_underage_record.go           # 未成年人退款记录
├── role.go                             # 角色模型
├── set_game_name_record.go             # 设置游戏名记录
├── sms_code_temp.go                    # 短信验证码模板
├── sms.go                              # 短信模型
├── user.go                             # 用户模型
├── vip_white_record.go                 # VIP 白名单记录
├── vouch_history.go                    # 兑换历史
├── wechat_official.go                  # 微信公众号
├── work_order.go                       # 工单模型
├── wx_deduct_balance_record.go         # 微信扣款记录
├── wx_order_record.go                  # 微信订单记录
│
├── init_data/                          # 初始化数据
├── model_bi/                           # BI 数据模型
├── model_content_audit/               # 内容审核模型
├── model_gift_code/                    # 礼包码模型
├── model_invoice/                      # 发票模型
├── model_vip/                          # VIP 模型
├── model_vip_scrm/                     # VIP CRM 模型
├── model_web/                          # Web 模型
└── ...
```

**主要职责**:

- 定义数据库表结构（使用 GORM 标签）
- 定义业务实体结构体
- 定义数据验证规则
- 定义表关联关系

#### 2.2.5 internal/conf/ - 配置管理

**功能**: 管理系统配置

```yaml
internal/conf/
├── cfg.yaml                    # 配置文件
├── charge_type.go              # 充值类型配置
├── client_id.go               # 客户端 ID 配置
├── conf_cloud_id.go           # 云 ID 配置
├── conf_judge.go              # 判断配置
├── conf_manage.go             # 管理配置
├── conf_test.go               # 测试配置
├── conf.go                    # 配置结构定义
├── config_listener.go         # 配置监听器
├── crm_config.go              # CRM 配置
├── gift_code_config.go        # 礼包码配置
├── init.go                    # 配置初始化
├── plugin.go                  # 插件配置
├── sns.go                     # SNS 配置
└── worker.go                  # Worker 配置
```

**说明**:

- 使用 YAML 格式存储配置
- 支持配置热更新（通过监听器）
- 不同环境使用不同配置文件

#### 2.2.6 internal/constants/ - 常量定义

```yaml
internal/constants/
├── common.go                  # 公共常量
├── content_audit.go           # 内容审核常量
└── vip.go                     # VIP 常量
```

#### 2.2.7 internal/worker/ - 后台任务 Worker

**功能**: 处理异步任务和定时任务

```yaml
internal/worker/
└── content_audit/             # 内容审核 Worker
    ├── manager.go             # Worker 管理器
    └── ...
```

#### 2.2.8 其他 internal 目录

- **internal/rdb/**: Redis 操作封装
- **internal/ga/**: 统计分析相关
- **internal/gcron/**: 定时任务管理
- **internal/tools/**: 内部工具函数
- **internal/module/**: 模块定义和初始化

### 2.3 middleware/ - HTTP 中间件

**功能**: 处理 HTTP 请求的中间件

```yaml
middleware/
├── action_record/            # 行为记录中间件
├── cors/                     # 跨域处理中间件
├── jwt/                      # JWT 认证中间件
├── project_permission/       # 项目权限验证中间件
├── recovery/                 # 异常恢复中间件
├── sign_verify/              # 签名验证中间件
└── web_limit/                # Web 限流中间件
```

**说明**:

- 使用 Gin 中间件机制
- 按需组合使用
- 支持自定义中间件

### 2.4 pkg/ - 可重用的公共包

**功能**: 提供可重用的功能包，可被其他项目引用

```yaml
pkg/
├── ai_help_server/           # AI 帮助服务 SDK
├── ai_td_server/             # AI TD 服务 SDK
├── anti_addition/            # 防沉迷
├── content/                  # 内容库集成
├── contextx/                 # 上下文扩展
├── crawler/                  # 爬虫工具
├── cticloud/                 # 呼叫中心集成
├── custom/                   # 自定义功能
├── db/                       # 数据库初始化
├── dingtalk/                 # 钉钉集成
├── docs/                     # 文档工具
├── email_server/             # 邮件服务 SDK
├── es/                       # Elasticsearch 操作
├── game_server/              # 游戏服务器 SDK
├── gen/                      # 生成代码（Protobuf）
├── gift_code_server/         # 礼包码服务 SDK
├── invoice_server/           # 发票服务 SDK
├── item_server/              # 物品服务 SDK
├── msg_server/               # 消息服务 SDK
├── obs/                      # 对象存储
├── permission/               # 权限管理
├── sdk/                      # SDK 集成
├── short_link/               # 短链接生成
├── sms/                      # 短信服务 SDK
├── smtp_util/                # SMTP 工具
├── tmp/                      # 临时系统
├── user_punish/              # 用户处罚
├── vip_admin/                # VIP 管理 SDK
└── wechat/                   # 微信集成
```

**说明**:

- 这些包可以在其他 Go 项目中引用
- 封装了外部服务的 SDK
- 提供通用功能组件

### 2.5 proto/ - Protobuf 定义文件

**功能**: 定义 RPC 接口和数据结构

```yaml
proto/
└── http/                     # HTTP 协议定义
    ├── common.proto          # 公共定义
    ├── admin.proto           # 管理相关
    ├── game.proto            # 游戏相关
    └── ... (其他 proto 文件)
```

**说明**:

- 使用 Protobuf 定义 API 接口
- 通过 `make gen` 生成 Go 代码
- 生成的代码存放在 `pkg/gen/`

### 2.6 docs/ - 自动生成的文档

**功能**: 存放自动生成的 API 文档

```yaml
docs/
├── docs.go                   # Swagger 文档入口
├── swagger.yaml              # Swagger YAML 格式
├── customer-service.swagger.yaml  # 完整 Swagger 文档
├── exchange_api.md           # 兑换 API 文档
└── apis/                     # 手写的 API 文档
    ├── api-doc-common-header.md
    ├── api-doc-template.md
    ├── README.md
    ├── apis-pay/
    └── apis-query_tool/
```

**说明**:

- 使用 Swaggo 自动生成 Swagger 文档
- 支持在线查看和测试 API
- `apis/` 目录存放手动编写的 API 说明文档

### 2.7 util/ - 工具函数库

**功能**: 提供通用工具函数

```yaml
util/
├── common.go                 # 公共工具函数
├── double_map.go             # 双重 Map
├── excel.go                  # Excel 操作
├── file.go                   # 文件操作
├── id_card.go                # 身份证工具
├── jwt.go                    # JWT 工具
├── jwt_test.go               # JWT 测试
├── crypt_util/               # 加密工具
├── field_util/               # 字段工具
├── order_common/             # 订单通用工具
├── sign_util/                # 签名工具
├── slice_util/               # 切片工具
└── time_util/                # 时间工具
```

**说明**:

- 提供项目内使用的工具函数
- 不对外暴露，仅供内部使用

### 2.8 sql/ - SQL 脚本

**功能**: 存放数据库脚本

```yaml
sql/
├── config_qa_filter.sql      # QA 过滤配置
├── exchange.sql              # 兑换相关表
└── mobile_bind_query.sql     # 手机绑定查询
```

### 2.9 scripts/ - 脚本工具

**功能**: 存放各种脚本和测试工具

```yaml
scripts/
├── README.md                 # 脚本说明
├── create_audit_punishment_tables.go  # 创建审核处罚表
├── create_vip_info_test.go   # 创建 VIP 信息测试
├── update_vip_base_info_test.go      # 更新 VIP 基础信息测试
└── integration_tests/        # 集成测试
```

### 2.10 tools/ - 编译工具

**功能**: 存放编译工具和二进制文件

```yaml
tools/
├── protoc                    # Protobuf 编译器
├── protoc-gen-bic            # 自定义 Protobuf 生成器
├── protoc-gen-go             # Go Protobuf 生成器
├── protoc-go-inject-tag      # Protobuf 标签注入工具
└── swag                      # Swagger 文档生成器
```

**说明**:

- 这些工具通常通过 Makefile 中的 `make gen` 命令调用
- 用于代码生成和文档生成

### 2.11 build/ - 构建相关

```yaml
build/
├── Dockerfile.customer-service         # 主服务 Dockerfile
└── Dockerfile.customer-service-api     # API 服务 Dockerfile
```

### 2.12 run/ - 运行时文件

```yaml
run/
└── logs/                    # 日志文件目录
```

### 2.13 content-lib/ - 内容库子模块

**功能**: 内容审核相关的独立模块（Git 子模块）

```yaml
content-lib/
├── go.mod                    # Go 模块定义
├── go.sum                    # 依赖锁定
├── README.md                 # 模块说明
├── INTEGRATION.md            # 集成文档
├── SHARDING.md               # 分片文档
├── api/                      # API 定义
├── dao/                      # 数据访问层
├── model/                    # 数据模型
├── listener/                 # 监听器
├── pkg/                      # 公共包
├── proto/                    # Protobuf 定义
├── sql/                      # SQL 脚本
├── scripts/                  # 脚本
├── tycore/                   # 核心组件
├── tykafka/                  # Kafka 封装
└── tysql/                    # 数据库驱动
```

**说明**:

- 这是一个独立的 Git 子模块
- 专门处理内容审核相关的业务逻辑
- 支持 Kafka 消息队列和数据库分片

## 3. 文件命名约定

### 3.1 Go 文件命名

- **dao 文件**: `xxx_dao.go` (数据访问层)
- **model 文件**: `xxx.go` (模型定义)
- **service 文件**: `xxx.go` (服务实现)
- **测试文件**: `xxx_test.go`
- **工具文件**: `xxx_util.go` 或 `xxx.go`

### 3.2 目录命名

- 使用小写字母和下划线
- 单词用下划线分隔（如 `web_user_manage`）
- 避免使用驼峰命名

### 3.3 配置文件

- 主配置文件: `cfg.yaml`
- 环境特定配置: `cfg.{env}.yaml`

## 4. 依赖关系图

```yaml
main.go
  └── cmd/
       └── internal/
            ├── api/            # HTTP 路由
            │     └── service/   # 业务逻辑
            │           ├── dao/ # 数据访问
            │           │     └── model/ # 数据模型
            │           ├── model/ # 直接使用
            │           └── pkg/   # 外部服务
            └── conf/           # 配置
```

## 5. 关键文件说明

### 5.1 main.go

- 程序入口
- 引入 Swagger 文档
- 启动命令行工具

### 5.2 internal/run.go

- 服务启动和关闭逻辑
- 信号处理（SIGUSR2, SIGHUP, SIGQUIT 等）
- Worker 管理器生命周期管理

### 5.3 Makefile

- `make gen`: 生成代码（Protobuf、Swagger）
- `make mac`: 编译 macOS 版本
- `make linux`: 编译 Linux 版本
- `make windows`: 编译 Windows 版本

## 6. 最佳实践

1. **代码组织**: 按业务域划分 service，每个 service 独立
2. **分层清晰**: API → Service → DAO → Model，职责分明
3. **可复用性**: 通用功能放在 pkg/，项目内工具放在 util/
4. **配置管理**: 使用 internal/conf/ 统一管理配置
5. **文档生成**: 使用 Swagger 注解自动生成 API 文档
6. **代码生成**: Protobuf 定义放在 proto/，通过 `make gen` 生成代码

## 7. 相关文档

- [系统架构文档](./ARCHITECTURE.md)
- [核心模块说明](./MODULES.md)
- [数据模型文档](./MODELS.md)
- [API路由文档](./ROUTES.md)
- [配置和环境文档](./CONFIG.md)
- [开发指南](./DEVELOPMENT.md)
