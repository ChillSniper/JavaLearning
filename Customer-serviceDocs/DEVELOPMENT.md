# Customer-Service 开发指南

## 1. 概述

本文档提供 Customer-Service 项目的开发指南，包括开发环境搭建、编码规范、测试指南、部署流程等。

## 2. 开发环境搭建

### 2.1 系统要求

- **Go 版本**: 1.21 或更高
- **MySQL**: 5.7 或更高
- **Redis**: 5.0 或更高
- **Protobuf**: 3.0 或更高
- **Make**: 用于构建和代码生成

### 2.2 安装依赖

```bash
# 克隆项目
git clone http://tygit.tuyoo.com/dev5/customer-service.git
cd customer-service

# 下载 Go 依赖
go mod download

# 初始化子模块
git submodule update --init --recursive
```

---

### 2.3 配置文件

复制配置模板并修改:

```bash
cp internal/conf/cfg.yaml.example internal/conf/cfg.yaml
```

编辑 `internal/conf/cfg.yaml`:

- 配置数据库连接信息
- 设置 JWT Secret
- 配置防沉迷和 SDK 访问凭证

---

### 2.4 启动服务

```bash
# 开发模式启动
go run main.go

# 或使用 Makefile
make run
```

服务启动后访问:

- **API 服务**: <http://localhost:8010>
- **Swagger 文档**: <http://localhost:8010/swagger/index.html>
- **健康检查**: <http://localhost:8010/health>

---

## 3. 项目结构

### 3.1 核心目录

```yaml
customer-service/
├── internal/           # 内部业务逻辑
│   ├── api/           # API 路由
│   ├── service/       # 业务服务层
│   ├── dao/           # 数据访问层
│   ├── model/         # 数据模型
│   └── conf/          # 配置管理
├── pkg/              # 可重用包
├── proto/            # Protobuf 定义
├── middleware/       # 中间件
└── util/            # 工具函数
```

**详细说明**: 参见 [目录结构详解](./STRUCTURE.md)

---

## 4. 编码规范

### 4.1 命名规范

#### 4.1.1 包命名

- 使用小写单词
- 不使用下划线或驼峰
- 包名应该简洁、描述性强

**示例**:

```go
// ✅ 好的包名
package user
package work_order
package email

// ❌ 不好的包名
package userService
package work_order
package EmailService
```

#### 4.1.2 文件命名

- 使用小写字母和下划线
- DAO 文件: `xxx_dao.go`
- 测试文件: `xxx_test.go`

**示例**:

```yaml
user_dao.go
work_order_test.go
email_service.go
```

#### 4.1.3 函数命名

- 导出函数: 驼峰命名（首字母大写）
- 私有函数: 驼峰命名（首字母小写）

**示例**:

```go
// 导出函数
func CreateUser() error {}
func GetUserByID(id uint) (*User, error) {}

// 私有函数
func validateUser(u *User) error {}
func hashPassword(pwd string) string {}
```

#### 4.1.4 变量命名

- 使用驼峰命名
- 常量使用大写字母和下划线

**示例**:

```go
var userName string
var userAge int

const MAX_RETRY_COUNT = 3
const DEFAULT_PAGE_SIZE = 10
```

---

### 4.2 代码格式化

#### 4.2.1 使用 go fmt

```bash
# 格式化所有代码
go fmt ./...

# 检查格式
gofmt -l .
```

#### 4.2.2 使用 goimports

```bash
# 自动整理导入
goimports -w .
```

**配置 IDE**:

- GoLand: Settings → Go → Imports → Format with goimports
- VS Code: settings.json 中配置 `"go.useLanguageServerForCodeLens": true`

---

### 4.3 注释规范

#### 4.3.1 包注释

```go
// Package user 提供用户管理功能
// 包括用户创建、查询、更新、删除等操作
package user
```

#### 4.3.2 函数注释

```go
// CreateUser 创建新用户
// 参数:
//   - username: 用户名
//   - password: 密码（明文）
// 返回:
//   - *User: 创建的用户对象
//   - error: 错误信息
func CreateUser(username, password string) (*User, error) {
    // 实现
}
```

#### 4.3.3 Swagger 注解

```go
// @Summary 创建用户
// @Description 创建新用户账号
// @Tags 用户管理
// @Accept json
// @Produce json
// @Param request body CreateUserRequest true "用户信息"
// @Success 200 {object} UserResponse
// @Failure 400 {object} ErrorResponse
// @Router /user [post]
func CreateUser(c *gin.Context) {
    // 实现
}
```

---

### 4.4 错误处理

#### 4.4.1 错误定义

```go
package errors

var (
    ErrUserNotFound = errors.New("user not found")
    ErrInvalidPassword = errors.New("invalid password")
    ErrDuplicateUsername = errors.New("duplicate username")
)
```

#### 4.4.2 错误包装

```go
func GetUserByID(id uint) (*User, error) {
    var user User
    if err := db.First(&user, id).Error; err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, errors.Wrap(errors.ErrUserNotFound, "get user by id")
        }
        return nil, errors.Wrap(err, "database error")
    }
    return &user, nil
}
```

#### 4.4.3 错误返回

```go
func CreateUser(req *CreateUserRequest) (*User, error) {
    // 验证参数
    if err := validateRequest(req); err != nil {
        return nil, errors.Wrap(err, "invalid request")
    }
    
    // 业务逻辑
    // ...
    
    return user, nil
}
```

---

## 5. 开发流程

### 5.1 新增业务模块

#### 步骤 1: 定义数据模型

创建 `internal/model/xxx.go`:

```go
package model

import (
    "time"
    "gorm.io/gorm"
)

type XXX struct {
    ID        uint      `gorm:"primarykey"`
    Name      string    `gorm:"type:varchar(100);not null"`
    Status    int       `gorm:"default:1"`
    CreatedAt time.Time
    UpdatedAt time.Time
    DeletedAt gorm.DeletedAt `gorm:"index"`
}
```

#### 步骤 2: 创建 DAO 层

创建 `internal/dao/xxx_dao.go`:

```go
package dao

import "customer-service/internal/model"

type XXXDAO struct{}

func NewXXXDAO() *XXXDAO {
    return &XXXDAO{}
}

// Create 创建记录
func (d *XXXDAO) Create(xxx *model.XXX) error {
    return db.Create(xxx).Error
}

// GetByID 根据 ID 查询
func (d *XXXDAO) GetByID(id uint) (*model.XXX, error) {
    var xxx model.XXX
    err := db.First(&xxx, id).Error
    if err != nil {
        return nil, err
    }
    return &xxx, nil
}

// Update 更新记录
func (d *XXXDAO) Update(xxx *model.XXX) error {
    return db.Save(xxx).Error
}

// Delete 删除记录（软删除）
func (d *XXXDAO) Delete(id uint) error {
    return db.Delete(&model.XXX{}, id).Error
}
```

#### 步骤 3: 实现服务层

创建 `internal/service/xxx/xxx.go`:

```go
package xxx

import (
    "customer-service/internal/dao"
    "customer-service/internal/model"
)

type Service struct {
    dao *dao.XXXDAO
}

func NewService() *Service {
    return &Service{
        dao: dao.NewXXXDAO(),
    }
}

// Create 创建记录
func (s *Service) Create(req *CreateRequest) (*model.XXX, error) {
    // 参数验证
    if err := validateCreateRequest(req); err != nil {
        return nil, err
    }
    
    // 创建对象
    xxx := &model.XXX{
        Name:   req.Name,
        Status: req.Status,
    }
    
    // 保存到数据库
    if err := s.dao.Create(xxx); err != nil {
        return nil, err
    }
    
    return xxx, nil
}
```

#### 步骤 4: 定义 Protobuf

创建 `proto/http/xxx.proto`:

```protobuf
syntax = "proto3";

package xxx;

option go_package = "customer-service/pkg/gen/api";

service XXXService {
    rpc CreateXXX(CreateXXXRequest) returns (CreateXXXResponse);
    rpc GetXXX(GetXXXRequest) returns (GetXXXResponse);
}

message CreateXXXRequest {
    string name = 1;
    int32 status = 2;
}

message CreateXXXResponse {
    int32 code = 1;
    string message = 2;
    XXX data = 3;
}

message XXX {
    uint32 id = 1;
    string name = 2;
    int32 status = 3;
}
```

#### 步骤 5: 生成代码

```bash
# 生成 Protobuf 代码和 Swagger 文档
make gen
```

#### 步骤 6: 注册路由

在 `internal/api/server.go` 中注册:

```go
import (
    "customer-service/internal/service/xxx"
    "customer-service/pkg/gen/api"
)

// 在 projectJwt 路由组中注册
api.RegisterXXXServiceHttpHandler(projectJwt, xxx.NewService())
```

#### 步骤 7: 编写测试

创建 `internal/service/xxx/xxx_test.go`:

```go
package xxx

import (
    "testing"
)

func TestService_Create(t *testing.T) {
    tests := []struct {
        name    string
        req     *CreateRequest
        wantErr bool
    }{
        {
            name: "success",
            req: &CreateRequest{
                Name:   "test",
                Status: 1,
            },
            wantErr: false,
        },
        {
            name: "invalid name",
            req: &CreateRequest{
                Name:   "",
                Status: 1,
            },
            wantErr: true,
        },
    }
    
    s := NewService()
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            _, err := s.Create(tt.req)
            if (err != nil) != tt.wantErr {
                t.Errorf("Create() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

#### 步骤 8: 运行测试

```bash
# 运行所有测试
go test ./...

# 运行特定模块测试
go test ./internal/service/xxx

# 查看测试覆盖率
go test -cover ./...
```

---

### 5.2 修改数据库

#### 5.2.1 创建迁移脚本

在 `sql/` 目录下创建迁移脚本:

```sql
-- sql/migrations/001_add_xxx_table.sql
CREATE TABLE `xxx` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL COMMENT '名称',
    `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态',
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `deleted_at` datetime DEFAULT NULL,
    PRIMARY KEY (`id`),
    KEY `idx_deleted_at` (`deleted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='XXX表';
```

#### 5.2.2 执行迁移

```bash
# 手动执行
mysql -u root -p customer_service < sql/migrations/001_add_xxx_table.sql

# 或使用迁移工具
go run scripts/migrate.go
```

---

### 5.3 修改 Protobuf

修改 `proto/http/` 下的 `.proto` 文件后，运行:

```bash
# 生成代码
make gen
```

生成的代码位于:

- Go 代码: `pkg/gen/api/`
- Swagger 文档: `docs/swagger.yaml`

---

## 6. 测试指南

### 6.1 单元测试

#### 6.1.1 Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -2, -3, -5},
        {"zero", 0, 0, 0},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d, want %d", 
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

#### 6.1.2 Mock 外部依赖

```go
package xxx_test

import (
    "testing"
    "github.com/stretchr/testify/mock"
)

type MockXXXDAO struct {
    mock.Mock
}

func (m *MockXXXDAO) Create(xxx *model.XXX) error {
    args := m.Called(xxx)
    return args.Error(0)
}

func TestService_Create(t *testing.T) {
    mockDAO := new(MockXXXDAO)
    mockDAO.On("Create", mock.Anything).Return(nil)
    
    s := &Service{dao: mockDAO}
    err := s.Create(&CreateRequest{Name: "test"})
    
    if err != nil {
        t.Errorf("unexpected error: %v", err)
    }
    
    mockDAO.AssertExpectations(t)
}
```

---

### 6.2 集成测试

创建 `scripts/integration_tests/` 目录:

```go
// scripts/integration_tests/integration_test.go
package integration_tests

import (
    "testing"
    "customer-service/internal/service"
)

func TestIntegration(t *testing.T) {
    // 初始化测试环境
    // ...
    
    // 测试完整流程
    s := xxx.NewService()
    user, err := s.Create(&CreateRequest{Name: "test"})
    if err != nil {
        t.Fatalf("failed to create: %v", err)
    }
    
    // 验证结果
    if user.Name != "test" {
        t.Errorf("expected name 'test', got '%s'", user.Name)
    }
}
```

---

### 6.3 测试覆盖率

```bash
# 生成覆盖率报告
go test -coverprofile=coverage.out ./...

# 查看覆盖率
go tool cover -html=coverage.out

# 命令行查看
go tool cover -func=coverage.out
```

---

## 7. Git 工作流

### 7.1 分支策略

```yaml
main (主分支，生产代码)
  └── develop (开发分支)
      ├── feature/xxx (功能分支)
      ├── bugfix/xxx (修复分支)
      └── hotfix/xxx (紧急修复分支)
```

### 7.2 提交规范

使用 Conventional Commits:

```yaml
feat: 新增用户管理功能
fix: 修复登录 Token 过期问题
docs: 更新 API 文档
style: 代码格式调整
refactor: 重构 DAO 层
test: 添加单元测试
chore: 更新依赖包
```

**提交消息格式**:

```yaml
<type>(<scope>): <subject>

<body>

<footer>
```

**示例**:

```yaml
feat(user): add user creation API

Add new endpoint for creating users with validation.

- Add user model
- Implement create user service
- Add unit tests

Closes #123
```

### 7.3 Pull Request

PR 模板:

```markdown
## 变更说明
<!-- 描述本次变更的内容 -->

## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化
- [ ] 其他

## 测试
- [ ] 单元测试
- [ ] 集成测试
- [ ] 手动测试

## 相关 Issue
Closes #xxx

## 截图或示例
<!-- 如果涉及 UI 变更，请提供截图 -->
<!-- 如果涉及 API 变更，请提供请求/响应示例 -->

## 配置变更
<!-- 如果涉及配置变更，请说明 -->
```

---

## 8. 构建和部署

### 8.1 本地构建

```bash
# 构建当前平台
go build -o customer-service main.go

# 使用 Makefile
make build

# 交叉编译
make mac    # macOS
make linux  # Linux
make windows # Windows
```

### 8.2 Docker 构建

```bash
# 构建镜像
docker build -f build/Dockerfile.customer-service -t customer-service:latest .

# 运行容器
docker run -p 8010:8010 \
  -e DB_HOST= \
  -e DB_PASSWORD= \
  customer-service:latest
```

### 8.3 部署到 Kubernetes

```bash
# 应用配置
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

---

## 9. 调试技巧

### 9.1 使用 Delve

```bash
# 安装 Delve
go install github.com/go-delve/delve/cmd/dlv@latest

# 调试运行
dlv debug main.go

# 调试测试
dlv test ./internal/service/xxx
```

### 9.2 日志调试

```go
import "tygit.tuyoo.com/gocomponents/glog"

glog.XInfo("Debug info: %+v", data)
glog.XWarn("Warning: %s", message)
glog.XError("Error: %v", err)
```

### 9.3 pprof 性能分析

```bash
# 启动服务后，发送 SIGUSR2 信号开启 pprof
kill -USR2 <pid>

# 访问 pprof
go tool pprof http://localhost:8010/debug/pprof/profile

# 生成火焰图
go tool pprof -http=:8080 http://localhost:8010/debug/pprof/profile
```

---

## 10. 常见问题

### 10.1 依赖问题

```bash
# 清理依赖缓存
go clean -modcache

# 更新依赖
go get -u ./...

# 整理依赖
go mod tidy
```

### 10.2 编译错误

```bash
# 检查 Go 版本
go version

# 清理编译缓存
go clean -cache

# 重新构建
go build -a
```

### 10.3 测试失败

```bash
# 运行详细测试输出
go test -v ./...

# 运行特定测试
go test -v -run TestCreateUser ./internal/service/user

# 跳过缓存
go test -count=1 ./...
```

---

## 11. 最佳实践

### 11.1 代码组织

- ✅ 按业务域划分模块
- ✅ 保持单一职责原则
- ✅ 避免循环依赖
- ✅ 使用接口抽象

### 11.2 性能优化

- ✅ 使用连接池
- ✅ 合理使用缓存
- ✅ 避免 N+1 查询
- ✅ 使用索引优化查询

### 11.3 安全

- ✅ 参数验证
- ✅ SQL 注入防护（使用参数化查询）
- ✅ 敏感数据加密
- ✅ 权限控制

### 11.4 可维护性

- ✅ 添加注释和文档
- ✅ 编写单元测试
- ✅ 遵循代码规范
- ✅ 定期重构

---

## 12. 相关文档

- [系统架构文档](./ARCHITECTURE.md)
- [目录结构详解](./STRUCTURE.md)
- [核心模块说明](./MODULES.md)
- [数据模型文档](./MODELS.md)
- [API路由文档](./ROUTES.md)
- [配置和环境文档](./CONFIG.md)
- [外部依赖文档](./INTEGRATIONS.md)
