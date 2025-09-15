package com.itheima;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

// @RestController注解：表示当前类是一个控制器类
// 控制器类：专门用来处理请求的类
// @Controller + @ResponseBody = @RestController
@RestController
public class HelloController {
    @RequestMapping("/hello")//请求路径
    public String hello(String name) {
        System.out.println("name:" + name);
        return "Hello " + name + "~";
    }
}
