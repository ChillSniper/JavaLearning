package com.itheima.Demo4Tcp1;

import java.io.DataInput;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class ServerDemo2 {
    public static void main(String[] args) throws IOException {
        System.out.println("The server is running...");

        // 1. 创建服务端ServerSocket对象，绑定端口号，监听客户端连接
        ServerSocket serverSocket = new ServerSocket(9999);
        Socket socket = serverSocket.accept();
        InputStream inputStream = socket.getInputStream();

        DataInputStream dataInputStream = new DataInputStream(inputStream);

        // 读取数据
        int id = dataInputStream.readInt();
        String data = dataInputStream.readUTF();
        System.out.println("id = " + id + ", msg = " + data);
        System.out.println("Server ip = " + socket.getInetAddress());
    }
}
