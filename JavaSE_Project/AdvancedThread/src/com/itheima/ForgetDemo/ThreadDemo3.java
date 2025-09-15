package com.itheima.ForgetDemo;

import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.FutureTask;

public class ThreadDemo3 {
    public static void main(String[] args) throws ExecutionException, InterruptedException {
        Callable<String> mc = new MyCallable(100);

        FutureTask<String> ft = new FutureTask<String>(mc);
        Thread t1 = new Thread(ft);

        t1.start();

        Callable<String> mc2 = new MyCallable(50);

        FutureTask<String> ft2 = new FutureTask<String>(mc2);
        Thread t2 = new Thread(ft);

        t2.start();
        // we should get the final val.

    }
}

class MyCallable implements Callable<String> {
        private int n;
        public MyCallable(int n) {
            this.n = n;
        }
    public String call() throws Exception {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += i;
        }
        return "thread" + n + "the value is " + sum;
    }
}