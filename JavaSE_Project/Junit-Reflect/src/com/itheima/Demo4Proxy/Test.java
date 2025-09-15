package com.itheima.Demo4Proxy;

import java.lang.reflect.Proxy;

public class Test {
    public static void main(String[] args) {
        Star s = new Star("LI");

        // 创建代理
        StarService proxy = (StarService) ProxyUtil.createProxy(s);
        proxy.Sing("Hello");
        System.out.println(proxy.dance());
    }
}
