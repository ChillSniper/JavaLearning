package com.itheima.demo1NetAddress;

import java.io.IOException;
import java.net.*;

public class UDP_Demo_Client {
    public static void main(String[] args) throws IOException {
        System.out.println("The Client is running...");
        // target: 完成UDP通信的一发一收：客户端开发
        // 1. 创建发送端对象
        DatagramSocket datagramSocket = new DatagramSocket();
        // 2. 创建数据包对象，封装要发送的数据
        byte[] buffer = "Test the UDP DEMO".getBytes();
        DatagramPacket datagramPacket = new DatagramPacket(buffer, buffer.length, InetAddress.getByName("192.168.56.1"), 8080);

        datagramSocket.send(datagramPacket);

    }
}
