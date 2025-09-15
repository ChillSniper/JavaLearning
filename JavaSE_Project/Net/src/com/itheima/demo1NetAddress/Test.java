package com.itheima.demo1NetAddress;

import java.net.InetAddress;

public class Test {
    public static void main(String[] args) {
        // 获得本机IP对象
        try {
            InetAddress inetAddress = InetAddress.getLocalHost();
            System.out.println(inetAddress.getHostAddress());
            System.out.println(inetAddress.getHostName());

            InetAddress inetAddress2 = InetAddress.getByName("ByteDance.com");
            System.out.println(inetAddress2.getHostAddress());
            System.out.println(inetAddress2.getHostName());

            // ping
            System.out.println(inetAddress2.isReachable(1000));


        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
