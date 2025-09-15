package com.itheima.service.impl;

import com.itheima.dao.UserDao;
import com.itheima.pojo.User;
import com.itheima.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Primary;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Component
public class UserServiceImpl2 implements UserService {


    @Autowired
    private UserDao userDao;

    @Override
    public List<User> findAll() {
        // 调用dao获取数据

        List<String> lines = userDao.findAll();

        List<User> userList = lines.stream().map(line ->{
            String[] parts = line.split(",");
            Integer id = Integer.parseInt(parts[0]);
            String username = parts[1];
            String password = parts[2];
            String name = parts[3];
            Integer age = Integer.parseInt(parts[4]);
            LocalDateTime updateTime = LocalDateTime.parse(parts[5], DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss") );
            return new User(id + 200, username, password, name, age, updateTime);
        }).toList();
        return userList;
    }
}
