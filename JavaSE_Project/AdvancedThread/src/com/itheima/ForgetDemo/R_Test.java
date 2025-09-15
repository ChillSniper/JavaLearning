package com.itheima.ForgetDemo;

public class R_Test {
    public static void main(String[] args) {
        Runnable fk = ()->{
                for (int i = 0; i < 10; i++) {
                    System.out.println(Thread.currentThread().getName() + ":" + i);
            }
        };
        Thread t1 = new Thread(fk);
        t1.start();
        for (int i = 0; i < 10; i++) {
            System.out.println(Thread.currentThread().getName() + ":" + i);
        }
    }
}
