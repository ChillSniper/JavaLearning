package com.itheima.SingleInstance;

public class Test {
    public static void main(String[] args) {
        // 设计单例类
//        A a1 = A.a;
//        A a2 = A.a;
//        System.out.println(a1 == a2);
//        A a3 = A.getInstance();
//        System.out.println(a3);
        B b = B.getInstance();
        B b2 = B.getInstance();
    }
}
