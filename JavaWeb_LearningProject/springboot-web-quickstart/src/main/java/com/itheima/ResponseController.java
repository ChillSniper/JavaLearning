package com.itheima;

import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.IOException;

@RestController
public class ResponseController {
    @RequestMapping("/response")
    public void response(HttpServletResponse response) throws IOException {
        // 1. 设置响应状态码
        response.setStatus(HttpServletResponse.SC_OK);

        // 2. 设置响应头
        response.setHeader("name", "itheima");

        // 3. 设置响应体
        response.getWriter().write("<h1>hello response</h1>");

    }

    /*
    *   方式二：使用ResponseEntity对象设置响应数据
    *      ResponseEntity：表示响应数据
    *     ResponseEntity<T>：表示响应数据，T表示响应体数据类型
    * */
    @RequestMapping("/response2")
    public ResponseEntity<String> responseEntity() {
        // 1. 创建响应头对象
        return ResponseEntity.status(401).header("name", "javaweb-ai").body("<h1>hello responseEntity</h1>");
    }
}
