package com.itheima;

import com.example.EnableHeaderConfig;
import com.example.HeaderConfig;
import com.example.MyImportSelector;
import org.apache.http.message.TokenParser;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Import;
import org.springframework.stereotype.Component;

//@Import(HeaderConfig.class) // 配置类导入
//@ComponentScan(basePackages = {"com.example", "com.itheima"})
//@Import(MyImportSelector.class)
//@EnableHeaderConfig
@Import(HeaderConfig.class)
@SpringBootApplication
public class SpringbootWebConfigApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringbootWebConfigApplication.class, args);
    }

}
