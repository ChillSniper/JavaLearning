package com.itheima.controller;

import cn.hutool.core.io.IoUtil;
import com.itheima.pojo.User;
import com.itheima.service.UserService;
import com.itheima.service.impl.UserServiceImpl;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.FileNotFoundException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

@RestController
public class UserController {
//    @Autowired
//    private UserService userService;

//    private final UserService userService;
//
//    @Autowired
//    public UserController(UserService userService) {
//        this.userService = userService;
//    }

//    @Qualifier("userServiceImpl2")
//    @Autowired
    @Resource(name = "userServiceImpl")
    private UserService u;

    @RequestMapping("/list")
    public List<User> list() throws FileNotFoundException {

        List<User> userList = u.findAll();

        // 还得转化为json格式的内容
        return userList;
    }
}
