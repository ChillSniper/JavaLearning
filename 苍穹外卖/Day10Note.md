# Day10

## 概览

>拖拖拉拉的终于来到Day10了，还有三天的工作量，本项目即可收尾搞定

本节开发内容和技术点：Spring Task、订单状态定时处理、WebSocket、来单提醒、客户催单

## Spring Task

留意一下**cron表达式**

Spring Task是Spring框架提供的任务调度工具，可以**按照约定的时间自动执行**某个逻辑

只要是需要定时处理的场景都可以使用**Spring** **Task**

**cron**表达式实际上是一个字符串，通过cron表达式可以**定义任务触发的时间**

cron表达式在线生成器：<https://cron.qqe2.com>

## 订单状态定时处理

![alt text](..\pictures\image-17_4.png)

这个地方没有**接口**这个概念，因为是自动执行的

## WebSocket

**WebScocket**是基于**TCP**的一种新的网络协议
实现**浏览器**和**服务器**之间的全双工通信
**浏览器**和**服务器**只需要完成一次握手，两者就可以建立**持久性**的连接，并且进行双向数据传输

对于**HTTP**协议和**WebSocket**协议的对比：

- HTTP是短连接
- WebSocket是长连接
- HTTP通信是单向的，基于请求响应模式
- WebSocket支持双向通信
- HTTP和WebSocket底层都是TCP连接
![alt text](..\pictures\image-18_5.png) ![alt text](..\pictures\image-19_4.png)

## 来单提醒

太好玩了这个哈哈哈哈哈哈哈

## 客户催单

![alt text](..\pictures\image-20_4.png)
