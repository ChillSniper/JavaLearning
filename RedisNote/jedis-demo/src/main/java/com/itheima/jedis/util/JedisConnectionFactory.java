package com.itheima.jedis.util;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

public class JedisConnectionFactory {
    private static final JedisPool jedisPool;

    static {
        // 先配置连接池
        JedisPoolConfig jedisPoolConfig = new JedisPoolConfig();
        jedisPoolConfig.setMaxTotal(10);
        jedisPoolConfig.setMaxIdle(10); // 最大空闲连接（即使没人用）
        jedisPoolConfig.setMinIdle(1); // 如果一直没人访问，空闲连接会被释放直到这个值
        jedisPoolConfig.setMaxWaitMillis(10000); // -1指的是无限等待

        // 然后创建连接池对象
        jedisPool = new JedisPool(jedisPoolConfig, "192.168.100.133",
                6379, 1000, "563543");
    }

    public static Jedis getJedisPool() {
        return jedisPool.getResource();
    }
}
