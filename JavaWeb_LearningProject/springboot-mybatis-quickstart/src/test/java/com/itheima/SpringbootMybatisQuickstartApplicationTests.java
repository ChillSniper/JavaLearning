package com.itheima;

import com.itheima.mapper.UserMapper;
import com.itheima.pojo.User;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
class SpringbootMybatisQuickstartApplicationTests {
    @Autowired
    private UserMapper userMapper;

    @Test
    public void testFindAll(){
        List<User> userList = userMapper.findAll();
        userList.forEach(System.out::println);
    }

    @Test
    public void testDeleteById(){
        userMapper.deleteById(1);
    }

    @Test
    public void testInsertUser(){
        User user = new User(null, "lisi", "123456", "李四", 30);

        userMapper.insertUser(user);
    }

    @Test
    public void testFindByUserNameAndPassword() {
        User user = userMapper.findByUserNameAndPassword("lisi", "123456");
        System.out.println(user);
    }
}
