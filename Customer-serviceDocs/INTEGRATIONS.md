# Customer-Service 外部依赖文档

## 1. 概述

Customer-Service 系统集成了多个外部服务，所有外部服务 SDK 封装在 `pkg/` 目录下。本文档详细说明各个外部服务的功能、配置和使用方法。

## 2. 外部服务分类

### 2.1 游戏相关服务

- **game_server**: 游戏服务器 SDK
- **item_server**: 物品服务 SDK
- **anti_addition**: 防沉迷系统
- **sdk**: 游戏 SDK 集成

### 2.2 通信服务

- **email_server**: 邮件服务
- **smtp_util**: SMTP 工具
- **sms**: 短信服务
- **msg_server**: 消息服务

### 2.3 内容和数据服务

- **content**: 内容库集成
- **es**: Elasticsearch
- **obs**: 对象存储

### 2.4 运营和 CRM 服务

- **vip_admin**: VIP 管理服务
- **invoice_server**: 发票服务
- **gift_code_server**: 礼包码服务
- **dingtalk**: 钉钉集成
- **wechat**: 微信集成

### 2.5 AI 和智能服务

- **ai_help_server**: AI 帮助服务
- **ai_td_server**: AI TD 服务

### 2.6 工具和服务

- **db**: 数据库初始化
- **permission**: 权限管理
- **short_link**: 短链接生成
- **crawler**: 爬虫工具
- **cticloud**: 呼叫中心
- **user_punish**: 用户处罚
- **tmp**: 临时系统

---

## 3. 游戏相关服务

### 3.1 game_server - 游戏服务器 SDK

**路径**: `pkg/game_server/`

**功能**:

- 与游戏服务器通信
- 获取游戏内数据
- 执行游戏内操作
- 发送游戏内通知

**主要方法**:

```go
// GetPlayerInfo 获取玩家信息
func GetPlayerInfo(projectID, userID string) (*PlayerInfo, error)

// SendMail 发送游戏内邮件
func SendMail(projectID, userID, title, content string) error

// BanPlayer 封禁玩家
func BanPlayer(projectID, userID string, duration int64) error

// UnbanPlayer 解禁玩家
func UnbanPlayer(projectID, userID string) error
```

**配置**:

```yaml
sdk_access:
  - cloud_id: "1"
    access_id: "wa15a79da9101b3ac6"
    secret_key: "9kQLYmnEaTYjhubOo2IelCvNtwBXX0ST"
```

**使用示例**:

```go
import "customer-service/pkg/game_server"

playerInfo, err := game_server.GetPlayerInfo("project123", "user456")
if err != nil {
    return err
}
fmt.Printf("Player: %s, Level: %d", playerInfo.Name, playerInfo.Level)
```

---

### 3.2 item_server - 物品服务 SDK

**路径**: `pkg/item_server/`

**功能**:

- 物品查询
- 物品发放
- 物品扣除
- 物品记录查询

**主要方法**:

```go
// GetItemInfo 获取物品信息
func GetItemInfo(projectID, itemID string) (*ItemInfo, error)

// GiveItem 发放物品
func GiveItem(projectID, userID, itemID string, count int) error

// DeductItem 扣除物品
func DeductItem(projectID, userID, itemID string, count int) error

// GetItemRecords 获取物品记录
func GetItemRecords(projectID, userID string, page, pageSize int) ([]ItemRecord, error)
```

**使用示例**:

```go
import "customer-service/pkg/item_server"

err := item_server.GiveItem("project123", "user456", "item789", 100)
if err != nil {
    return err
}
```

---

### 3.3 anti_addition - 防沉迷系统

**路径**: `pkg/anti_addition/`

**功能**:

- 用户实名认证
- 防沉迷时长限制
- 充值限制
- 游戏时长查询

**主要方法**:

```go
// VerifyRealName 验证实名
func VerifyRealName(projectID, userID, name, idCard string) (*RealNameInfo, error)

// GetPlayTime 获取游戏时长
func GetPlayTime(projectID, userID string) (*PlayTimeInfo, error)

// CheckPayLimit 检查充值限制
func CheckPayLimit(projectID, userID string) (*PayLimitInfo, error)

// LimitGameTime 限制游戏时长
func LimitGameTime(projectID, userID string, duration int) error
```

**配置**:

```yaml
anti_addiction:
  access:
    - cloud_id: "3"
      access_id: "15e0d56b999a2394"
      secret_key: "tZP01TGVtyNNSj4yLKmhQjFwjcsqlNzR"
```

---

### 3.4 sdk - 游戏 SDK 集成

**路径**: `pkg/sdk/`

**功能**:

- 统一的游戏 SDK 接口
- 多游戏项目支持
- SDK 认证和授权

---

## 4. 通信服务

### 4.1 email_server - 邮件服务

**路径**: `pkg/email_server/`

**功能**:

- 发送 HTML 邮件
- 邮件模板管理
- 邮件队列
- 发送状态跟踪

**主要方法**:

```go
// SendEmail 发送邮件
func SendEmail(to, subject, content string) (*SendResult, error)

// SendEmailWithCC 发送邮件（带抄送）
func SendEmailWithCC(to, cc, subject, content string) (*SendResult, error)

// SendTemplateEmail 发送模板邮件
func SendTemplateEmail(to, templateID string, params map[string]interface{}) (*SendResult, error)

// GetSendStatus 获取发送状态
func GetSendStatus(emailID string) (*SendStatus, error)
```

**使用示例**:

```go
import "customer-service/pkg/email_server"

result, err := email_server.SendEmail(
    "user@example.com",
    "Welcome",
    "<h1>Welcome to our service!</h1>",
)
if err != nil {
    return err
}
fmt.Printf("Email sent: %s", result.EmailID)
```

---

### 4.2 smtp_util - SMTP 工具

**路径**: `pkg/smtp_util/`

**功能**:

- SMTP 邮件发送
- SMTP 连接池
- TLS/SSL 支持

**主要方法**:

```go
// SendSMTP 通过 SMTP 发送邮件
func SendSMTP(from, to, subject, body string) error

// SendSMTPWithAuth 通过 SMTP 发送邮件（带认证）
func SendSMTPWithAuth(from, to, subject, body, username, password string) error
```

---

### 4.3 sms - 短信服务

**路径**: `pkg/sms/`

**功能**:

- 发送短信
- 验证码短信
- 模板短信
- 短信记录查询

**主要方法**:

```go
// SendSMS 发送短信
func SendSMS(phone, content string) (*SendResult, error)

// SendCode 发送验证码短信
func SendCode(phone, code string) (*SendResult, error)

// SendTemplateSMS 发送模板短信
func SendTemplateSMS(phone, templateID string, params map[string]string) (*SendResult, error)

// GetSendStatus 获取发送状态
func GetSendStatus(smsID string) (*SendStatus, error)
```

**使用示例**:

```go
import "customer-service/pkg/sms"

result, err := sms.SendCode("13800138000", "123456")
if err != nil {
    return err
}
fmt.Printf("SMS sent: %s", result.SMSID)
```

---

### 4.4 msg_server - 消息服务

**路径**: `pkg/msg_server/`

**功能**:

- 站内消息发送
- 消息推送
- 消息模板
- 消息记录

**主要方法**:

```go
// SendMessage 发送站内消息
func SendMessage(projectID, userID, title, content string) (*SendResult, error)

// SendBatchMessage 批量发送消息
func SendBatchMessage(projectID string, userIDs []string, title, content string) (*SendResult, error)

// GetMessageList 获取消息列表
func GetMessageList(projectID, userID string, page, pageSize int) ([]Message, error)
```

---

## 5. 内容和数据服务

### 5.1 content - 内容库集成

**路径**: `pkg/content/`

**功能**:

- 内容审核
- 内容管理
- 内容分类
- 内容标签

**主要方法**:

```go
// SubmitContent 提交内容审核
func SubmitContent(content *Content) (*AuditTask, error)

// GetAuditStatus 获取审核状态
func GetAuditStatus(taskID string) (*AuditStatus, error)

// GetContent 获取内容
func GetContent(contentID string) (*Content, error)
```

**相关模块**: `content-lib/` (Git 子模块）

---

### 5.2 es - Elasticsearch

**路径**: `pkg/es/`

**功能**:

- 索引管理
- 文档搜索
- 聚合查询
- 批量操作

**主要方法**:

```go
// IndexDocument 索引文档
func IndexDocument(index string, doc interface{}) error

// SearchDocument 搜索文档
func SearchDocument(index string, query elastic.Query, from, size int) (*SearchResult, error)

// DeleteDocument 删除文档
func DeleteDocument(index, docID string) error

// AggregateDocument 聚合查询
func AggregateDocument(index string, agg elastic.Aggregation) (*AggregationResult, error)
```

**使用示例**:

```go
import "customer-service/pkg/es"

// 搜索用户
query := elastic.NewTermQuery("name", "John")
result, err := es.SearchDocument("users", query, 0, 10)
if err != nil {
    return err
}
fmt.Printf("Found %d users", result.TotalHits)
```

---

### 5.3 obs - 对象存储

**路径**: `pkg/obs/`

**功能**:

- 文件上传
- 文件下载
- 文件删除
- 文件列表

**主要方法**:

```go
// UploadFile 上传文件
func UploadFile(bucket, key string, data []byte) (*UploadResult, error)

// DownloadFile 下载文件
func DownloadFile(bucket, key string) ([]byte, error)

// DeleteFile 删除文件
func DeleteFile(bucket, key string) error

// GetFileURL 获取文件 URL
func GetFileURL(bucket, key string, expire time.Duration) (string, error)
```

---

## 6. 运营和 CRM 服务

### 6.1 vip_admin - VIP 管理服务

**路径**: `pkg/vip_admin/`

**功能**:

- VIP 用户管理
- VIP 等级管理
- VIP 权益配置
- VIP 数据查询

**主要方法**:

```go
// GetVIPInfo 获取 VIP 信息
func GetVIPInfo(projectID, userID string) (*VIPInfo, error)

// SetVIPLevel 设置 VIP 等级
func SetVIPLevel(projectID, userID string, level int) error

// GetVIPBenefits 获取 VIP 权益
func GetVIPBenefits(level int) ([]VIPBenefit, error)

// AddVIPPoints 添加 VIP 积分
func AddVIPPoints(projectID, userID string, points int) error
```

---

### 6.2 invoice_server - 发票服务

**路径**: `pkg/invoice_server/`

**功能**:

- 发票申请
- 发票开具
- 发票查询
- 发票下载

**主要方法**:

```go
// ApplyInvoice 申请发票
func ApplyInvoice(req *InvoiceRequest) (*Invoice, error)

// GetInvoice 获取发票
func GetInvoice(invoiceID string) (*Invoice, error)

// DownloadInvoice 下载发票 PDF
func DownloadInvoice(invoiceID string) ([]byte, error)

// GetInvoiceList 获取发票列表
func GetInvoiceList(projectID, userID string, page, pageSize int) ([]Invoice, error)
```

---

### 6.3 gift_code_server - 礼包码服务

**路径**: `pkg/gift_code_server/`

**功能**:

- 生成礼包码
- 验证礼包码
- 兑换礼包码
- 礼包码管理

**主要方法**:

```go
// GenerateGiftCode 生成礼包码
func GenerateGiftCode(projectID, codeType string, count int) ([]string, error)

// ValidateGiftCode 验证礼包码
func ValidateGiftCode(projectID, userID, code string) (*GiftCode, error)

// RedeemGiftCode 兑换礼包码
func RedeemGiftCode(projectID, userID, code string) (*RedeemResult, error)

// GetGiftCodeInfo 获取礼包码信息
func GetGiftCodeInfo(projectID, code string) (*GiftCode, error)
```

---

### 6.4 dingtalk - 钉钉集成

**路径**: `pkg/dingtalk/`

**功能**:

- 发送钉钉消息
- 钉钉机器人
- 钉钉审批
- 钉钉通知

**主要方法**:

```go
// SendTextMessage 发送文本消息
func SendTextMessage(webhook, secret, content string) error

// SendMarkdownMessage 发送 Markdown 消息
func SendMarkdownMessage(webhook, secret, title, content string) error

// SendLinkMessage 发送链接消息
func SendLinkMessage(webhook, secret, title, text, messageURL, picURL string) error
```

**配置**:

```yaml
app:
  ding_web_hook: "https://oapi.dingtalk.com/robot/send?access_token=xxx"
  ding_secret: "SECxxx"
```

---

### 6.5 wechat - 微信集成

**路径**: `pkg/wechat/`

**功能**:

- 微信公众号
- 微信登录
- 微信支付
- 微信消息

**主要方法**:

```go
// GetAccessToken 获取访问令牌
func GetAccessToken(appID, appSecret string) (*AccessToken, error)

// SendTemplateMessage 发送模板消息
func SendTemplateMessage(openID, templateID string, data map[string]interface{}) error

// GetUserInfo 获取用户信息
func GetUserInfo(openID, lang string) (*UserInfo, error)

// CreateQrCode 创建二维码
func CreateQrCode(scene, expire int64) (*QrCode, error)
```

---

## 7. AI 和智能服务

### 7.1 ai_help_server - AI 帮助服务

**路径**: `pkg/ai_help_server/`

**功能**:

- AI 对话
- 问题回答
- 知识库管理
- 聊天记录

**主要方法**:

```go
// AskQuestion 提问
func AskQuestion(projectID, userID, question string) (*Answer, error)

// GetChatHistory 获取聊天历史
func GetChatHistory(projectID, userID, sessionID string) ([]ChatRecord, error)

// AddQuestion 添加问题到知识库
func AddQuestion(projectID, question, answer, category string) error

// SubmitChatLog 提交聊天日志
func SubmitChatLog(log *ChatLog) error
```

---

### 7.2 ai_td_server - AI TD 服务

**路径**: `pkg/ai_td_server/`

**功能**:

- AI 意图识别
- AI 语义分析
- AI 推荐系统

**主要方法**:

```go
// RecognizeIntent 识别意图
func RecognizeIntent(text string) (*Intent, error)

// AnalyzeSentiment 分析情感
func AnalyzeSentiment(text string) (*Sentiment, error)

// GetRecommendation 获取推荐
func GetRecommendation(userID, itemType string) ([]Recommendation, error)
```

---

## 8. 工具和服务

### 8.1 db - 数据库初始化

**路径**: `pkg/db/`

**功能**:

- 数据库连接初始化
- 连接池管理
- 数据库迁移
- 读写分离

**主要方法**:

```go
// InitDB 初始化数据库连接
func InitDB(config *Config) (*gorm.DB, error)

// GetDB 获取数据库连接
func GetDB() *gorm.DB

// CloseDB 关闭数据库连接
func CloseDB() error
```

---

### 8.2 permission - 权限管理

**路径**: `pkg/permission/`

**功能**:

- 权限验证
- 角色管理
- 权限配置
- Casbin 集成

**主要方法**:

```go
// CheckPermission 检查权限
func CheckPermission(userID, resource, action string) (bool, error)

// GetPermissions 获取用户权限
func GetPermissions(userID string) ([]Permission, error)

// AddPermission 添加权限
func AddPermission(userID, resource, action string) error

// RemovePermission 移除权限
func RemovePermission(userID, resource, action string) error
```

---

### 8.3 short_link - 短链接生成

**路径**: `pkg/short_link/`

**功能**:

- 生成短链接
- 短链接跳转
- 短链接统计

**主要方法**:

```go
// GenerateShortLink 生成短链接
func GenerateShortLink(longURL string) (string, error)

// GetLongURL 获取长链接
func GetLongURL(shortLink string) (string, error)

// GetClickStats 获取点击统计
func GetClickStats(shortLink string) (*ClickStats, error)
```

---

### 8.4 crawler - 爬虫工具

**路径**: `pkg/crawler/`

**功能**:

- 网页抓取
- 数据提取
- 反爬虫处理

**主要方法**:

```go
// CrawlURL 抓取网页
func CrawlURL(url string) (*Page, error)

// ExtractData 提取数据
func ExtractData(page *Page, selector string) ([]string, error)

// CrawlWithProxy 使用代理抓取
func CrawlWithProxy(url, proxyURL string) (*Page, error)
```

---

### 8.5 cticloud - 呼叫中心

**路径**: `pkg/cticloud/`

**功能**:

- 外呼管理
- 坐席管理
- 通话记录
- 实时监控

**主要方法**:

```go
// MakeCall 发起外呼
func MakeCall(phone, agentID string) (*Call, error)

// GetAgents 获取坐席列表
func GetAgents() ([]Agent, error)

// GetCallRecords 获取通话记录
func GetCallRecords(page, pageSize int) ([]CallRecord, error)

// MonitorAgent 监控坐席
func MonitorAgent(agentID string) (*MonitorData, error)
```

---

### 8.6 user_punish - 用户处罚

**路径**: `pkg/user_punish/`

**功能**:

- 用户封禁
- 用户禁言
- 处罚记录
- 处罚申诉

**主要方法**:

```go
// BanUser 封禁用户
func BanUser(projectID, userID string, reason string, duration int64) error

// UnbanUser 解封用户
func UnbanUser(projectID, userID string) error

// GetPunishRecords 获取处罚记录
func GetPunishRecords(projectID, userID string) ([]PunishRecord, error)

// SubmitAppeal 提交申诉
func SubmitAppeal(projectID, userID, reason string) (*Appeal, error)
```

---

### 8.7 tmp - 临时系统

**路径**: `pkg/tmp/`

**功能**:

- 临时数据存储
- 临时令牌生成
- 临时会话管理

**主要方法**:

```go
// GenerateTmpToken 生成临时令牌
func GenerateTmpToken(userID string, expire time.Duration) (string, error)

// ValidateTmpToken 验证临时令牌
func ValidateTmpToken(token string) (*TmpToken, error)

// SetTmpData 设置临时数据
func SetTmpData(key string, value interface{}, expire time.Duration) error

// GetTmpData 获取临时数据
func GetTmpData(key string) (interface{}, error)
```

---

## 9. 代码生成

### 9.1 gen - 生成代码

**路径**: `pkg/gen/`

**功能**:

- Protobuf 生成的代码
- Swagger 文档
- API 接口定义

**内容**:

- `api/`: Protobuf 生成的 API 代码
- `pb/`: Protobuf 生成的 PB 代码

---

## 10. 使用示例

### 10.1 发送邮件和短信

```go
import (
    "customer-service/pkg/email_server"
    "customer-service/pkg/sms"
)

// 发送邮件
_, err := email_server.SendEmail(
    "user@example.com",
    "Verification Code",
    "Your code is: 123456",
)

// 发送短信
_, err = sms.SendCode("13800138000", "123456")
```

### 10.2 调用游戏服务器

```go
import "customer-service/pkg/game_server"

// 获取玩家信息
playerInfo, err := game_server.GetPlayerInfo("project123", "user456")
if err != nil {
    return err
}

// 发放物品
err = game_server.GiveItem("project123", "user456", "item789", 100)
```

### 10.3 内容审核

```go
import "customer-service/pkg/content"

// 提交内容审核
task, err := content.SubmitContent(&Content{
    Type:    "chat",
    Content:  "Hello world",
    UserID:   "user456",
})

// 查询审核状态
status, err := content.GetAuditStatus(task.TaskID)
```

### 10.4 发送钉钉通知

```go
import "customer-service/pkg/dingtalk"

// 发送文本消息
err := dingtalk.SendTextMessage(
    config.App.DingWebHook,
    config.App.DingSecret,
    "New work order created",
)
```

---

## 11. 错误处理

### 11.1 统一错误处理

```go
import "customer-service/pkg/errors"

// 使用统一错误
if err != nil {
    return errors.Wrap(err, "failed to send email")
}
```

### 11.2 重试机制

```go
import "github.com/sethvargo/go-retry"

// 使用重试机制
backoff := retry.WithMaxRetries(5, retry.NewExponential(100*time.Millisecond))
for r := retry.Start(ctx, backoff, nil); r.Next(); {
    err := sendEmail(...)
    if err == nil {
        break
    }
    if r.Err() != nil {
        return r.Err()
    }
}
```

---

## 12. 最佳实践

### 12.1 配置管理

- ✅ 使用配置文件管理外部服务凭证
- ✅ 敏感信息使用环境变量
- ✅ 定期轮换密钥

### 12.2 错误处理

- ✅ 统一错误处理
- ✅ 记录错误日志
- ✅ 提供友好的错误信息

### 12.3 性能优化

- ✅ 使用连接池
- ✅ 批量操作
- ✅ 缓存结果

### 12.4 监控和日志

- ✅ 记录调用日志
- ✅ 监控调用成功率
- ✅ 告警机制

---

## 13. 相关文档

- [系统架构文档](./ARCHITECTURE.md)
- [目录结构详解](./STRUCTURE.md)
