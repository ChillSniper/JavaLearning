package com.itheima.ForgetDemo;

public class Test {
    public static void main(String[] args) {
        // 1. the way of building the thread
        // main方法本身是由一条主线程负责推荐执行的

        Thread t1 = new MyThread();
        Thread t2 = new MyThread();
        t1.start();
        t2.start();

    }
}

class MyThread extends Thread {
    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            // So wonderful of the IDEA
            System.out.println(Thread.currentThread().getName() + ":" + i);
        }
    }
}