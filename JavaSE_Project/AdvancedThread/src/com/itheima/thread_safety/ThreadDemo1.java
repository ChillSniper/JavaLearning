package com.itheima.thread_safety;

public class ThreadDemo1 {
    public static void main(String[] args) {
        // 线程安全问题模拟
        // 1. 设计一个账户类
        Account account = new Account(100000, "ICBC-110");

        Thread t1 = new DrawThread("John", account);
        t1.start();
        Thread t2 = new DrawThread("Ace", account);
        t2.start();


    }
}
