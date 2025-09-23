# 整体架构

![alt text](image.png)

## Spring Framework系统架构

![alt text](image-1.png)

## Spring核心概念

IoC（Inversion of Control）控制反转

使用对象时，由主动new产生对象转换为**由外部提供对象**。此过程中，对象创建控制权由程序转移到外部，此思想被称为**控制反转**

核心思想：**充分解耦**

利用IoC容器管理Bean（IoC）
在IoC容器中，将所有有依赖关系的bean进行关系绑定（**DI**）

这个DI，就是**依赖注入**

### IoC入门案例

IoC是用来管理Bean的，这个Bean，也就是对象

这个入门案例写了个寂寞

### DI入门案例

注意这个细节

![alt text](image-2.png)

ref指的是当前容器中bean的名字
而name指的是实现类中bean属性的名字（就是对象的名字）

### bean配置

关于bean的基础配置

**为什么bean默认为单例？**

如果说不设置为单例，会造成bean数量很大，而这并不是Spring负责管理的

### bean实例化

bean怎么整出来**单例**的？

bean实际上就是**对象**，创建bean使用**构造方法**完成

还有一种办法，**静态工厂**（这个了解即可）

第三种办法：**实例工厂**

这仨玩意听了和没听一样

### bean生命周期

bean生命周期：从创建到销毁的过程

先提供生命周期控制方法

然后配置生命周期控制方法

>讲真这部分内容我还是没听懂，这玩意有什么用么，一直在改配置文件

### 依赖注入方式

此处涉及到向类中传递数据的方式

**依赖注入**描述的是在容器中建立bean之间**依赖关系**的过程

而bean运行需要的数据分为两种：

1. 引用类型
2. 简单类型（基本数据类型和String）

而依赖注入方式有两种

1. setter注入
2. 构造器注入

由此，使用依赖注入传递数据的方式有四种

#### setter注入-简单类型

要在bean中定义引用类型属性，然后给到set方法（当然是可以访问到的）
案例：

```java
// 例子
public void setNumber(int number) {
    this.Number = number;
}
```

然后从配置中用property标签value属性注入简单类型数据

#### 构造器注入

**耦合度**很高的一种方案

```xml
<bean id = "" class = "">
    <constructor-arg name="" ref = "">
</bean>
```

注意**name**字段对应的是形参，ref对应的bean的名字

这就带来了一个问题，形参和bean配置中的name字段发生了**耦合**！

自己开发的模块大多使用setter注入

#### 依赖自动装配

很便捷的一个办法！！！
给定setter注入，然后在XML配置文件中，加入"autowire = "byType"

#### 集合注入

>这部分内容不知道在搞什么鬼

没啥用，在项目中很少使用

> 听的还是稀里糊涂的，我仍然没搞懂这个框架究竟在做什么，发挥着什么用途

### 加载properties文件

![alt text](image-3.png)

这个不知道什么鬼，根本听不懂

#### 容器

不care那些闹心的事，不care！

BeanFactory创建完毕之后，所有的bean都是延迟加载

### 核心容器总结

![alt text](image-5.png)

关于**依赖注入**相关

![alt text](image-6.png)

### 注解开发

Spring2.5 注解开发定义bean
Spring3.0 纯注解开发

但是这个注解开发定义还是要写配置文件，非常的麻烦

由此，我们引入**纯注解开发**！！！

### 纯注解开发

Spring3.0引入
用Java类代替配置文件

```java
@Configuration
@ComponentScan("com.itheima")
public class SpringConfig {

}
```

上面这段代码直接代替了Spring的核心配置文件

@Configuration注解用于设定当前类为配置类
@ComponentScan注解用于设定扫描路径，这个注解只能添加一次，多个数据的话，得用数组形式

### bean管理

关于bean作用范围和bean生命周期

### 依赖注入

使用**注解**的形式作**依赖注入**

```java

```
