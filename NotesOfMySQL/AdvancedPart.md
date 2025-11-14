# Advanced Part

进阶篇总线
![alt text](..\pictures\image-5_3.png)

## 存储引擎

### MySQL体系结构

连接层、服务层、引擎层、存储层

![alt text](..\pictures\image-6_2.png)

### 存储引擎简介

存储引擎是存储数据、建立索引、更新/查询数据等技术的实现方式。存储引擎是基于表的，而不是基于库的。存储引擎可以被称为**表类型**

比方说：MEMORY，MyISAM，InnoDB

### 存储引擎特点

#### InnoDB

InnoDB是一种兼顾高可靠性和高性能的通用存储引擎
![alt text](..\pictures\image-7_3.png)

#### MyISAM

MyISAM是MySQL早期的默认存储引擎

关于InnoDB、MyISAM、Memory这三个存储引擎的特点区别
（这种东西感觉根本记不住）

![alt text](..\pictures\image-8_3.png)

#### 存储引擎的选择

主要还是选择InnoDB
![alt text](..\pictures\image-9_3.png)

## 索引
