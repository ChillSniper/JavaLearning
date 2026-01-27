# Customer-Service 数据模型文档

## 1. 概述

Customer-Service 系统使用 GORM 作为 ORM 框架，数据模型定义在 `internal/model/` 目录下。每个模型对应数据库中的一张表，使用结构体标签定义字段属性和约束。

## 2. 核心模型

### 2.1 用户和权限相关

#### user.go - 用户模型

```go
type User struct {
    ID        uint      `gorm:"primarykey"`
    Username  string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    Password  string    `gorm:"type:varchar(255);not null"`
    Email     string    `gorm:"type:varchar(100)"`
    Phone     string    `gorm:"type:varchar(20)"`
    Status    int       `gorm:"default:1;comment:状态 1:正常 0:禁用"`
    RoleID    uint      `gorm:"index"`
    CreatedAt time.Time
    UpdatedAt time.Time
    DeletedAt gorm.DeletedAt `gorm:"index"`
}
```

**说明**:

- 管理员和客服人员信息
- 支持软删除
- 关联角色表

---

#### role.go - 角色模型

```go
type Role struct {
    ID          uint      `gorm:"primarykey"`
    Name        string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    Description string    `gorm:"type:varchar(200)"`
    Permissions string    `gorm:"type:text;comment:权限ID列表，逗号分隔"`
    CreatedAt   time.Time
    UpdatedAt   time.Time
    DeletedAt   gorm.DeletedAt `gorm:"index"`
}
```

**说明**:

- 角色权限管理
- 权限字段存储权限 ID 列表

---

#### project.go - 项目模型

```go
type Project struct {
    ID          uint      `gorm:"primarykey"`
    ProjectID   string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectName string    `gorm:"type:varchar(100);not null"`
    GameID      string    `gorm:"type:varchar(50)"`
    Status      int       `gorm:"default:1;comment:状态 1:正常 0:禁用"`
    Config      string    `gorm:"type:text;comment:项目配置JSON"`
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

**说明**:

- 多项目管理
- 每个项目对应一个游戏
- Config 字段存储 JSON 格式的配置

---

### 2.2 工单相关

#### work_order.go - 工单模型

```go
type WorkOrder struct {
    ID          uint      `gorm:"primarykey"`
    OrderNo     string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    UserID      string    `gorm:"type:varchar(50);not null;index"`
    Title       string    `gorm:"type:varchar(200);not null"`
    Content     string    `gorm:"type:text;not null"`
    Type        int       `gorm:"comment:工单类型"`
    Priority    int       `gorm:"default:1;comment:优先级 1:低 2:中 3:高"`
    Status      int       `gorm:"default:1;comment:状态 1:待处理 2:处理中 3:已关闭"`
    HandlerID   uint      `gorm:"index"`
    Remark      string    `gorm:"type:text;comment:处理备注"`
    Rating      int       `gorm:"default:0;comment:评价 0:未评价 1-5:评分"`
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

**说明**:

- 客服工单系统核心表
- 支持工单评分
- 记录处理人和处理状态

---

### 2.3 投诉相关

#### complaint.go - 投诉模型

```go
type Complaint struct {
    ID          uint      `gorm:"primarykey"`
    ComplaintNo string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    UserID      string    `gorm:"type:varchar(50);not null;index"`
    Type        int       `gorm:"comment:投诉类型"`
    Content     string    `gorm:"type:text;not null"`
    Evidence    string    `gorm:"type:text;comment:证据URL"`
    Status      int       `gorm:"default:1;comment:状态 1:待处理 2:处理中 3:已关闭"`
    HandlerID   uint      `gorm:"index"`
    Result      string    `gorm:"type:text;comment:处理结果"`
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

**说明**:

- 用户投诉记录
- 支持证据附件
- 记录处理人和处理结果

---

#### refund_underage_record.go - 未成年人退款记录

```go
type RefundUnderageRecord struct {
    ID            uint      `gorm:"primarykey"`
    RefundNo      string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID     string    `gorm:"type:varchar(50);not null"`
    UserID        string    `gorm:"type:varchar(50);not null"`
    GuardianName  string    `gorm:"type:varchar(50);not null;comment:监护人姓名"`
    GuardianID    string    `gorm:"type:varchar(20);not null;comment:监护人身份证"`
    GuardianPhone string    `gorm:"type:varchar(20);not null;comment:监护人手机"`
    RefundAmount decimal.Decimal `gorm:"type:decimal(10,2);not null"`
    BankAccount   string    `gorm:"type:varchar(50);not null;comment:银行卡号"`
    BankName      string    `gorm:"type:varchar(100);not null;comment:银行名称"`
    Status        int       `gorm:"default:1;comment:状态 1:待审核 2:审核通过 3:审核拒绝"`
    Remark        string    `gorm:"type:text"`
    CreatedAt     time.Time
    UpdatedAt     time.Time
}
```

**说明**:

- 未成年人退款申请
- 需要监护人信息
- 退款金额精确到分

---

### 2.4 订单和支付相关

#### item_record.go - 物品记录

```go
type ItemRecord struct {
    ID          uint      `gorm:"primarykey"`
    RecordNo    string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    UserID      string    `gorm:"type:varchar(50);not null;index"`
    ItemID      string    `gorm:"type:varchar(50);not null"`
    ItemName    string    `gorm:"type:varchar(100);not null"`
    ItemCount   int       `gorm:"not null;comment:物品数量"`
    OrderNo     string    `gorm:"type:varchar(50);index;comment:订单号"`
    OperatorID  uint      `gorm:"comment:操作人ID"`
    Reason      string    `gorm:"type:varchar(200);comment:操作原因"`
    CreatedAt   time.Time
}
```

**说明**:

- GM 工具物品操作记录
- 记录物品的发送、扣除等操作
- 关联订单号

---

#### pay_risk_strategy_records.go - 支付风控策略记录

```go
type PayRiskStrategyRecord struct {
    ID          uint      `gorm:"primarykey"`
    OrderNo     string    `gorm:"type:varchar(50);not null;index"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    UserID      string    `gorm:"type:varchar(50);not null"`
    StrategyID  string    `gorm:"type:varchar(50);not null"`
    StrategyName string    `gorm:"type:varchar(100);not null"`
    Result      int       `gorm:"comment:风控结果 1:通过 2:拦截"`
    Reason      string    `gorm:"type:text;comment:拦截原因"`
    CreatedAt   time.Time
}
```

**说明**:

- 支付风控策略执行记录
- 记录风控拦截原因

---

### 2.5 通知和消息相关

#### notify.go - 通知模型

```go
type Notify struct {
    ID          uint      `gorm:"primarykey"`
    NotifyID    string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    UserID      string    `gorm:"type:varchar(50);not null;index"`
    Type        int       `gorm:"comment:通知类型 1:站内信 2:邮件 3:短信"`
    Title       string    `gorm:"type:varchar(200);not null"`
    Content     string    `gorm:"type:text;not null"`
    Status      int       `gorm:"default:0;comment:状态 0:待发送 1:已发送 2:发送失败"`
    SendTime    *time.Time
    ErrorMsg    string    `gorm:"type:text"`
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

**说明**:

- 统一通知记录表
- 支持站内信、邮件、短信三种方式
- 记录发送状态和错误信息

---

#### email_record.go - 邮件记录

```go
type EmailRecord struct {
    ID          uint      `gorm:"primarykey"`
    EmailID     string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    To          string    `gorm:"type:varchar(200);not null"`
    Cc          string    `gorm:"type:varchar(500)"`
    Subject     string    `gorm:"type:varchar(200);not null"`
    Content     string    `gorm:"type:text;not null"`
    Status      int       `gorm:"default:0;comment:状态 0:待发送 1:已发送 2:发送失败"`
    SendTime    *time.Time
    ErrorMsg    string    `gorm:"type:text"`
    CreatedAt   time.Time
}
```

**说明**:

- 邮件发送记录
- 支持抄送
- 记录发送状态

---

#### sms.go - 短信模型

```go
type SMS struct {
    ID          uint      `gorm:"primarykey"`
    SMSID       string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    Phone       string    `gorm:"type:varchar(20);not null;index"`
    TemplateID  string    `gorm:"type:varchar(50);not null"`
    Params      string    `gorm:"type:text;comment:模板参数JSON"`
    Content     string    `gorm:"type:text;not null;comment:实际发送内容"`
    Status      int       `gorm:"default:0;comment:状态 0:待发送 1:已发送 2:发送失败"`
    SendTime    *time.Time
    ErrorMsg    string    `gorm:"type:text"`
    CreatedAt   time.Time
}
```

**说明**:

- 短信发送记录
- 支持模板短信
- 参数以 JSON 格式存储

---

#### sms_code_temp.go - 短信验证码模板

```go
type SMSCodeTemp struct {
    ID         uint      `gorm:"primarykey"`
    Phone      string    `gorm:"type:varchar(20);not null;index"`
    Code       string    `gorm:"type:varchar(10);not null"`
    Type       int       `gorm:"comment:验证码类型"`
    ExpireTime time.Time `gorm:"not null"`
    Used       bool      `gorm:"default:false;comment:是否已使用"`
    CreatedAt  time.Time
}
```

**说明**:

- 短信验证码临时存储
- 设置过期时间
- 标记是否已使用

---

### 2.6 VIP 相关

#### vip_white_record.go - VIP 白名单记录

```go
type VIPWhiteRecord struct {
    ID         uint      `gorm:"primarykey"`
    RecordID   string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID  string    `gorm:"type:varchar(50);not null;index"`
    UserID     string    `gorm:"type:varchar(50);not null"`
    VIPLevel   int       `gorm:"comment:VIP等级"`
    Reason     string    `gorm:"type:varchar(200);comment:加入原因"`
    Status     int       `gorm:"default:1;comment:状态 1:生效 0:失效"`
    OperatorID uint      `gorm:"index"`
    CreatedAt  time.Time
}
```

**说明**:

- VIP 白名单管理
- 记录操作人

---

### 2.7 礼品和奖励相关

#### gift_code_record.go - 礼包码记录

```go
type GiftCodeRecord struct {
    ID         uint      `gorm:"primarykey"`
    CodeID     string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID  string    `gorm:"type:varchar(50);not null;index"`
    Code       string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    Type       int       `gorm:"comment:礼包码类型"`
    Reward     string    `gorm:"type:text;comment:奖励内容JSON"`
    MaxUse     int       `gorm:"comment:最大使用次数"`
    UsedCount  int       `gorm:"default:0;comment:已使用次数"`
    ExpireTime *time.Time
    Status     int       `gorm:"default:1;comment:状态 1:可用 0:不可用"`
    CreatedAt  time.Time
}
```

**说明**:

- 礼包码管理
- 奖励内容以 JSON 存储
- 控制使用次数和有效期

---

#### vouch_history.go - 兑换历史

```go
type VouchHistory struct {
    ID        uint      `gorm:"primarykey"`
    HistoryID string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID string    `gorm:"type:varchar(50);not null;index"`
    UserID    string    `gorm:"type:varchar(50);not null;index"`
    Code      string    `gorm:"type:varchar(50);not null;index"`
    Reward    string    `gorm:"type:text;comment:奖励内容"`
    CreatedAt time.Time
}
```

**说明**:

- 兑换码使用记录
- 记录用户兑换历史

---

### 2.8 内容审核相关

#### model_content_audit/ 目录

包含内容审核相关的模型：

- 审核任务模型
- 审核结果模型
- 处罚记录模型
- 标签模型
- 队列配置模型

---

### 2.9 注销相关

#### account_cancel_record.go - 账号注销记录

```go
type AccountCancelRecord struct {
    ID          uint      `gorm:"primarykey"`
    RecordID    string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    UserID      string    `gorm:"type:varchar(50);not null"`
    Phone       string    `gorm:"type:varchar(20);not null"`
    Reason      string    `gorm:"type:varchar(200);comment:注销原因"`
    Status      int       `gorm:"default:1;comment:状态 1:申请中 2:审核通过 3:审核拒绝"`
    ReviewerID  uint      `gorm:"index"`
    ReviewTime  *time.Time
    CancelTime  *time.Time
    CreatedAt   time.Time
}
```

**说明**:

- 账号注销申请记录
- 包含审核流程

---

#### change_password_record_dao.go - 修改密码记录

```go
type ChangePasswordRecord struct {
    ID        uint      `gorm:"primarykey"`
    UserID    string    `gorm:"type:varchar(50);not null;index"`
    ProjectID string    `gorm:"type:varchar(50);not null;index"`
    OldHash   string    `gorm:"type:varchar(255)"`
    NewHash   string    `gorm:"type:varchar(255);not null"`
    IP        string    `gorm:"type:varchar(50)"`
    UserAgent string    `gorm:"type:varchar(500)"`
    CreatedAt time.Time
}
```

**说明**:

- 密码修改历史记录
- 记录 IP 和 User-Agent 用于审计

---

### 2.10 封禁申诉相关

#### forbidden_appeal_record.go - 封禁申诉记录

```go
type ForbiddenAppealRecord struct {
    ID          uint      `gorm:"primarykey"`
    AppealID    string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    UserID      string    `gorm:"type:varchar(50);not null"`
    ForbiddenID string    `gorm:"type:varchar(50);not null"`
    Reason      string    `gorm:"type:text;not null;comment:申诉理由"`
    Evidence    string    `gorm:"type:text;comment:证据URL"`
    Status      int       `gorm:"default:1;comment:状态 1:待审核 2:审核通过 3:审核拒绝"`
    ReviewerID  uint      `gorm:"index"`
    ReviewTime  *time.Time
    Remark      string    `gorm:"type:text;comment:审核备注"`
    CreatedAt   time.Time
}
```

**说明**:

- 封禁申诉记录
- 支持证据附件
- 包含审核流程

---

### 2.11 AI 相关

#### ai_chat_log.go - AI 聊天日志

```go
type AIChatLog struct {
    ID        uint      `gorm:"primarykey"`
    LogID     string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID string    `gorm:"type:varchar(50);not null;index"`
    UserID    string    `gorm:"type:varchar(50);not null;index"`
    SessionID string    `gorm:"type:varchar(50);not null;index"`
    Question  string    `gorm:"type:text;not null"`
    Answer    string    `gorm:"type:text;not null"`
    Status    int       `gorm:"default:0;comment:状态 0:待审核 1:已审核"`
    ReviewerID uint     `gorm:"index"`
    CreatedAt time.Time
}
```

**说明**:

- AI 客服聊天记录
- 支持人工审核

---

#### ai_question.go - AI 问题库

```go
type AIQuestion struct {
    ID        uint      `gorm:"primarykey"`
    QuestionID string   `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID string    `gorm:"type:varchar(50);not null;index"`
    Question  string    `gorm:"type:text;not null"`
    Answer    string    `gorm:"type:text;not null"`
    Category  string    `gorm:"type:varchar(50);comment:问题分类"`
    Keywords  string    `gorm:"type:text;comment:关键词JSON"`
    Status    int       `gorm:"default:1;comment:状态 1:启用 0:禁用"`
    CreatedAt time.Time
    UpdatedAt time.Time
}
```

**说明**:

- AI 问题知识库
- 支持分类和关键词匹配

---

### 2.12 字典管理

#### dict.go - 字典模型

```go
type Dict struct {
    ID        uint      `gorm:"primarykey"`
    DictID    string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    DictType  string    `gorm:"type:varchar(50);not null;index"`
    DictKey   string    `gorm:"type:varchar(50);not null"`
    DictValue string    `gorm:"type:varchar(200);not null"`
    Sort      int       `gorm:"default:0;comment:排序"`
    Status    int       `gorm:"default:1;comment:状态 1:启用 0:禁用"`
    Remark    string    `gorm:"type:varchar(200)"`
    CreatedAt time.Time
    UpdatedAt time.Time
}
```

**说明**:

- 系统字典表
- 支持多类型字典
- 支持排序

---

### 2.13 其他模型

#### outbound_call_record.go - 外呼记录

```go
type OutboundCallRecord struct {
    ID        uint      `gorm:"primarykey"`
    RecordID  string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID string    `gorm:"type:varchar(50);not null;index"`
    UserID    string    `gorm:"type:varchar(50);not null"`
    Phone     string    `gorm:"type:varchar(20);not null"`
    AgentID   string    `gorm:"type:varchar(50);comment:坐席ID"`
    Status    int       `gorm:"default:1;comment:状态 1:待呼叫 2:呼叫中 3:已接通 4:未接通"`
    Duration  int       `gorm:"comment:通话时长(秒)"`
    Remark    string    `gorm:"type:text;comment:通话备注"`
    CallTime  *time.Time
    CreatedAt time.Time
}
```

**说明**:

- 呼叫中心外呼记录
- 记录通话时长和状态

---

#### mobile_bind_record.go - 手机绑定记录

```go
type MobileBindRecord struct {
    ID        uint      `gorm:"primarykey"`
    UserID    string    `gorm:"type:varchar(50);not null;index"`
    ProjectID string    `gorm:"type:varchar(50);not null;index"`
    Phone     string    `gorm:"type:varchar(20);not null"`
    BindType  int       `gorm:"comment:绑定类型"`
    IP        string    `gorm:"type:varchar(50)"`
    CreatedAt time.Time
}
```

**说明**:

- 手机号绑定记录
- 记录绑定 IP 用于审计

---

#### channel_bind.go - 渠道绑定

```go
type ChannelBind struct {
    ID        uint      `gorm:"primarykey"`
    UserID    string    `gorm:"type:varchar(50);not null;index"`
    ProjectID string    `gorm:"type:varchar(50);not null;index"`
    ChannelID string    `gorm:"type:varchar(50);not null;comment:渠道ID"`
    ChannelName string   `gorm:"type:varchar(100);comment:渠道名称"`
    BindTime  time.Time `gorm:"not null"`
    CreatedAt time.Time
}
```

**说明**:

- 用户渠道绑定记录
- 追踪用户来源渠道

---

#### wechat_official.go - 微信公众号

```go
type WechatOfficial struct {
    ID          uint      `gorm:"primarykey"`
    UserID      string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    ProjectID   string    `gorm:"type:varchar(50);not null;index"`
    OpenID      string    `gorm:"type:varchar(50);not null;uniqueIndex"`
    UnionID     string    `gorm:"type:varchar(50);index"`
    Nickname    string    `gorm:"type:varchar(100)"`
    HeadImgURL  string    `gorm:"type:varchar(500)"`
    Subscribe   bool      `gorm:"default:true;comment:是否关注"`
    SubscribeTime *time.Time
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

**说明**:

- 微信公众号用户绑定
- 存储 OpenID 和 UnionID

---

## 3. 模型子目录

### 3.1 model_vip/ - VIP 相关模型

包含 VIP 等级、VIP 权益、VIP 记录等模型

### 3.2 model_gift_code/ - 礼包码相关模型

包含礼包码类型、礼包码奖励配置等模型

### 3.3 model_invoice/ - 发票相关模型

包含发票申请、发票详情等模型

### 3.4 model_content_audit/ - 内容审核相关模型

包含审核任务、审核结果、处罚记录等模型

### 3.5 model_web/ - Web 相关模型

包含 Web 端特有的数据模型

### 3.6 model_vip_scrm/ - VIP CRM 相关模型

包含 VIP 客户画像、行为分析等模型

### 3.7 model_bi/ - BI 数据模型

包含数据仓库相关的模型

## 4. 数据库索引

### 4.1 常用索引类型

- **主键索引**: `gorm:"primarykey"`
- **唯一索引**: `gorm:"uniqueIndex"`
- **普通索引**: `gorm:"index"`
- **复合索引**: 多个字段组合索引

### 4.2 索引设计原则

1. 查询频繁的字段添加索引
2. 外键字段添加索引
3. 软删除字段添加索引: `DeletedAt`
4. 唯一性约束字段使用唯一索引

## 5. 数据库关联关系

### 5.1 一对一关系

```go
type User struct {
    ID       uint
    Profile  Profile  // 一对一
}

type Profile struct {
    ID     uint
    UserID uint
    User   User `gorm:"foreignKey:UserID"`
}
```

### 5.2 一对多关系

```go
type Project struct {
    ID       uint
    Orders   []Order  // 一对多
}

type Order struct {
    ID        uint
    ProjectID uint
    Project   Project `gorm:"foreignKey:ProjectID"`
}
```

### 5.3 多对多关系

```go
type User struct {
    ID     uint
    Roles  []Role `gorm:"many2many:user_roles;"`
}

type Role struct {
    ID    uint
    Users []User `gorm:"many2many:user_roles;"`
}
```

## 6. 数据库迁移

### 6.1 自动迁移

```go
db.AutoMigrate(&User{}, &Role{}, &Project{})
```

### 6.2 SQL 脚本

重要数据库变更通过 SQL 脚本管理，位于 `sql/` 目录

## 7. 数据验证

### 7.1 GORM 验证标签

```go
type User struct {
    Username string `gorm:"not null;size:50"`
    Email    string `gorm:"not null;uniqueIndex"`
    Age      int    `gorm:"min:0;max:150"`
}
```

### 7.2 自定义验证

在 Service 层进行业务逻辑验证

## 8. 软删除

GORM 支持软删除，模型需包含 `DeletedAt` 字段：

```go
type User struct {
    ID        uint
    DeletedAt gorm.DeletedAt `gorm:"index"`
}
```

## 9. 时间戳

模型自动包含时间戳字段：

```go
CreatedAt time.Time  // 创建时间
UpdatedAt time.Time  // 更新时间
```

## 10. 最佳实践

1. **命名规范**: 表名使用复数，字段名使用蛇形命名
2. **字段类型**: 根据业务需求选择合适的字段类型
3. **索引优化**: 合理使用索引，避免过度索引
4. **关联关系**: 明确定义表之间的关联关系
5. **注释**: 为表和字段添加清晰的注释
6. **版本管理**: 数据库变更通过 SQL 脚本和迁移文件管理

## 11. 相关文档

- [系统架构文档](./ARCHITECTURE.md)
- [目录结构详解](./STRUCTURE.md)
- [核心模块说明](./MODULES.md)
- [API路由文档](./ROUTES.md)
- [配置和环境文档](./CONFIG.md)
- [开发指南](./DEVELOPMENT.md)
