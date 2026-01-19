package com.heima.test;

import com.itheima.jedis.util.JedisConnectionFactory;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import redis.clients.jedis.Jedis;

import java.util.Map;

public class JedisTest {
    private Jedis jedis;

    @BeforeEach
    void setUp() {
//        jedis = new Jedis("192.168.100.133", 6379);

        jedis = JedisConnectionFactory.getJedisPool();
        // set the password
        jedis.auth("563543");

        // choose the db
        jedis.select(0);

    }

    @Test
    void testString() {
        String result = jedis.set("name", "HerbertLu");

        System.out.println("result = " + result);

        String name = jedis.get("name");

        System.out.println("name = " + name);

    }

    @Test
    void testHash() {
        jedis.hset("user:1", "name", "HerbertLu");
        jedis.hset("user:1", "age", "20");

        Map<String, String> map = jedis.hgetAll("user:1");
        System.out.println(map);
    }

    @AfterEach
    void tearDown() {
        if (jedis != null) {
            jedis.close();
        }
    }
}
