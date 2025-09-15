package com.itheima.demo1NetAddress;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class UDP_Demo_Server {
    public static void main(String[] args) throws IOException {
        System.out.println("The Server is running...");
        // 创建UDP服务器
        // 1. 创建接收端对象
        DatagramSocket datagramSocket = new DatagramSocket(8080);
        // 2. 创建数据包对象负责接收数据
        byte[] buffer = new byte[1024 * 64];
        // 创建数据包
        DatagramPacket datagramPacket = new DatagramPacket(buffer, buffer.length);

        // 3. 接收数据
        datagramSocket.receive(datagramPacket);

        // 4. 查看数据是否接受到
        // 获取当前收到的数据长度
        int len = datagramPacket.getLength();
        String data = new String(buffer, 0, len);
        System.out.println("Server get the data: " + data);

        String ip = datagramPacket.getAddress().getHostAddress();
        int port = datagramPacket.getPort();
        System.out.println("Server IP: " + ip + " Port: " + port);

    }
}
