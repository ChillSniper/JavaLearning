package com.itheima.demo7executorService;

import java.util.concurrent.*;

public class ExecutorServiceDemo1 {
    public static void main(String[] args) {
        ExecutorService pool = new ThreadPoolExecutor(3, 5, 10,
                TimeUnit.MILLISECONDS, new ArrayBlockingQueue<>(3),
                Executors.defaultThreadFactory(), new ThreadPoolExecutor.CallerRunsPolicy());
        Runnable target = new MyRunnable();
        pool.execute(target); // 此时会创建线程，并且自动启动线程处理这个任务
        pool.execute(target);
        pool.execute(target);

        pool.execute(target);
        pool.execute(target);
        pool.execute(target);

        pool.execute(target);
        pool.execute(target);
        pool.execute(target);

        pool.shutdown();
    }
}
