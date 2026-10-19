# 接口响应 Diff 报告

报告格式版本：1

旧版输入 SHA-256：736c01d5c26bb4a6aa2e641a3397676823760211c7eebbbba519bfb3bfe008f3

新版输入 SHA-256：3ab810cab06b76fcdf18dd3c3401c2b04804b6d88284f5ba730bf2af10dea3de

有效配置 SHA-256：b3d9767469d92d1d0cc5c8231123836eff8f465e8a6d3cbb619ddd14f7a9d163

## 记录统计

| 总记录数 | 有差异数 | 无差异数 | 共同记录数 | 记录新增数 | 记录删除数 |
| --- | --- | --- | --- | --- | --- |
| 7 | 4 | 3 | 7 | 0 | 0 |

## 差异分类

| Diff 类型 | 条数 |
| --- | --- |
| 状态码变更 | 1 |
| 字段删除 | 4 |
| 字段新增 | 3 |
| 字段类型变更 | 2 |
| 字段值变更 | 0 |
| 记录删除 | 0 |
| 记录新增 | 0 |

差异明细总条数：10

## 忽略处理统计

| 旧版命中数 | 新版命中数 |
| --- | --- |
| 23 | 23 |

## 差异明细

### req&#95;001 - 获取文章详情（GET /api/articles/1）

| 比较对象 | 字段路径 | Diff 类型 | 旧值 | 新值 |
| --- | --- | --- | --- | --- |
| body | data.author&#95;email | 字段删除 | string "creator@kuaishou.com" | 字段不存在 |
| body | data.like&#95;count | 字段类型变更 | string "128" | number 128 |
| body | data.updated&#95;at | 字段新增 | 字段不存在 | string "2024-06-01T00:00:00Z" |

### req&#95;002 - 获取文章详情 - 文章 ID 2（GET /api/articles/2）

| 比较对象 | 字段路径 | Diff 类型 | 旧值 | 新值 |
| --- | --- | --- | --- | --- |
| body | data.author&#95;email | 字段删除 | string "videocreator@kuaishou.com" | 字段不存在 |
| body | data.like&#95;count | 字段类型变更 | string "356" | number 356 |
| body | data.updated&#95;at | 字段新增 | 字段不存在 | string "2024-06-02T00:00:00Z" |

### req&#95;003 - 获取文章列表（GET /api/articles）

| 比较对象 | 字段路径 | Diff 类型 | 旧值 | 新值 |
| --- | --- | --- | --- | --- |
| body | data.data | 字段新增 | 字段不存在 | object {"list":&#91;{"category":"video","id":1,"like&#95;count":128,"title":"快手创作者成长指南"},{"category":"video","id":2,"like&#95;count":356,"title":"如何拍出爆款短视频"},{"category":"live","id":3,"like&#95;count":89,"title":"直播带货运营技巧"}&#93;,"total":3} |
| body | data.items | 字段删除 | array &#91;{"category":"video","id":1,"like&#95;count":"128","title":"快手创作者成长指南"},{"category":"video","id":2,"like&#95;count":"356","title":"如何拍出爆款短视频"},{"category":"live","id":3,"like&#95;count":"89","title":"直播带货运营技巧"}&#93; | 字段不存在 |
| body | data.total | 字段删除 | number 3 | 字段不存在 |

### req&#95;004 - 创建新文章（POST /api/articles）

| 比较对象 | 字段路径 | Diff 类型 | 旧值 | 新值 |
| --- | --- | --- | --- | --- |
| HTTP | response.status | 状态码变更 | number 200 | number 201 |

## 无差异记录

| id | 请求描述 | method | path |
| --- | --- | --- | --- |
| req&#95;005 | 获取不存在的文章 | GET | /api/articles/999 |
| req&#95;006 | 更新文章 | PUT | /api/articles/1 |
| req&#95;007 | 创建文章 - 缺少必填参数 | POST | /api/articles |

## 疑似动态字段

提示数量：0
