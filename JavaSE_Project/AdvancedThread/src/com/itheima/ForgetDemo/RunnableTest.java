package com.itheima.ForgetDemo;

public class RunnableTest {
    public static void main(String[] args) {

    }
}

class MyRunnable implements Runnable {

    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println(Thread.currentThread().getName() + ":" + i);
        }
    }
}