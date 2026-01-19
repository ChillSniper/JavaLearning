package com.heima;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.heima.redis.pojo.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;

import java.util.Map;

@SpringBootTest
class RedisStringTests {

    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @Test
    void contextLoads() {
    }

    @Test
    void testString() {
        stringRedisTemplate.opsForValue().set("name", "Herbert");

        Object name = stringRedisTemplate.opsForValue().get("name");
        System.out.println(name);
    }

    private static final ObjectMapper objectMapper = new ObjectMapper();

    @Test
    void testSaveUser() throws JsonProcessingException {
        // 现在得手动序列化
        User user = new User("虎哥", 21);
        String json = objectMapper.writeValueAsString(user);
        stringRedisTemplate.opsForValue().set("user:200", json);

        String jsonUser = stringRedisTemplate.opsForValue().get("user:200");

        // 手动反序列化

        User newUser = objectMapper.readValue(jsonUser, User.class);

        System.out.println("o = " + newUser);
    }

    @Test
    void testHash() {
        stringRedisTemplate.opsForHash().put("user:400", "name", "虎哥");
        stringRedisTemplate.opsForHash().put("user:400", "age", "21");
        Map<Object, Object> entries = stringRedisTemplate.opsForHash().entries("user:400");
        System.out.println("entries = " + entries);
    }
}
