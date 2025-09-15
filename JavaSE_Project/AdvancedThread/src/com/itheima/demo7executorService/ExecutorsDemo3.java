package com.itheima.demo7executorService;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ExecutorsDemo3 {
    public static void main(String[] args) {
        // target: build the thread pool
        ExecutorService pool = Executors.newFixedThreadPool(3);

    }
}
