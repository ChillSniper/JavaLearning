package com.itheima.Demo4Tcp1;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

public class Client1 {
    public static void main(String[] args) throws IOException {
        System.out.println("The client is running...");

        // 1. 常见Socket管道对象
        Socket socket = new Socket("127.0.0.1", 9999);

        // 2. 从Socket管道中得到一个字节输出流
        OutputStream os = socket.getOutputStream();
        // 3. 特殊数据流
        DataOutputStream dos = new DataOutputStream(os);
        dos.writeInt(1);
        dos.writeUTF("我想你了，你在哪里？");

        // 4. 关闭资源
        socket.close();


    }
}
