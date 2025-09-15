package com.itheima.SingleInstance;

public class A {
    // 1. 私有化构造器
    private A() {

    }

    public static final A a = new A();
    public static A getInstance() {
        return a;
    }
}
