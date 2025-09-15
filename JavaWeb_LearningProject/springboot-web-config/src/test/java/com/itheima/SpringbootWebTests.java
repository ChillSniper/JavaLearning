package com.itheima;

import com.example.HeaderParser;
import com.example.TokenParser;
import com.google.gson.Gson;
import com.itheima.controller.DeptController;
import com.itheima.pojo.Result;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;

@SpringBootTest
class SpringbootWebTests {

    // 这边涉及到IOC容器
    @Autowired
    private ApplicationContext applicationContext;

    @Autowired
    private Gson gson;

    @Test
    public void testJson() {
        System.out.println(gson.toJson(Result.success("Hello gson")));
    }

    @Test
    public void testScope() {
        for (int i = 0;i < 1000;i ++) {
            Object deptController = applicationContext.getBean("deptController");
            System.out.println(deptController);
        }
    }

    @Autowired
    private HeaderParser headerParser;

    @Test
    public void testHeaderParser() {
        headerParser.parse();
    }
}
