# Start Steps

## 生产者发送的原理

Kafka Producer 生产者

main线程 -> Interceptors拦截器 -> Serializer序列化器 -> Partitioner分区器

发送原理非常抽象，后面的课里面会慢慢讲

在消息发送的过程中，涉及到两个线程：**main线程和Sender线程**。在mian线程中创建一个双端队列**RecordAccumulator**，main线程将信息发送给**RecordAccumulator**，Sender线程不断从RecordAccumulator中拉取消息，发送给Kafka Broker

### 异步发送流程
