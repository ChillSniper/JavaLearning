package com.itheima.DemoTcp2;

import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;
import java.util.Scanner;

public class Client1 {
    public static void main(String[] args) throws IOException {
        System.out.println("The client is running...");

        // 1. 常见Socket管道对象
        Socket socket = new Socket("127.0.0.1", 9999);

        // 2. 从Socket管道中得到一个字节输出流
        OutputStream os = socket.getOutputStream();
        // 3. 特殊数据流

        DataOutputStream dos = new DataOutputStream(os);

        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("Please enter: ");
            String input = sc.nextLine();
            if("exit".equals(input)) {
                System.out.println("The client is exiting...");
                socket.close();
                break;
            }
            dos.writeUTF(input);
            dos.flush();
        }

    }
}
