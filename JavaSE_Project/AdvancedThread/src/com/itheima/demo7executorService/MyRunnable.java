package com.itheima.demo7executorService;

public class MyRunnable implements Runnable {
    public static void main(String[] args) {

    }

    @Override
    public void run() {
        for (int i = 0; i < 10; i++) {
            System.out.println(Thread.currentThread().getName() + " printout: " + i);
            try {
                Thread.sleep(Integer.MAX_VALUE);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }
}
