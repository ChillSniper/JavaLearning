package com.itheima.DemoTcp4;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.*;

public class ServerDemo2 {
    public static void main(String[] args) throws IOException {
        // 多发多收
        System.out.println("The server is running...");

        // 1. 创建服务端ServerSocket对象，绑定端口号，监听客户端连接
        ServerSocket serverSocket = new ServerSocket(8080);

        ExecutorService pool = new ThreadPoolExecutor(3, 10, 10,
                TimeUnit.MILLISECONDS, new ArrayBlockingQueue<>(100),
                Executors.defaultThreadFactory(), new ThreadPoolExecutor.AbortPolicy());

        while (true) {
            Socket socket = serverSocket.accept();
            System.out.println("A new client has been accepted!" + socket.getInetAddress().getHostAddress());
            pool.execute(new ServerReaderRunnable(socket));
        }
    }
}
