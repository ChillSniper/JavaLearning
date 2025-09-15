package com.itheima.DemoTcp4;

import java.io.*;
import java.net.Socket;

public class ServerReaderRunnable implements Runnable {
    private Socket socket;
    public ServerReaderRunnable(Socket socket) {
        this.socket = socket;
    }
    @Override
    public void run() {
        try {
            // 给当前对应的浏览器管道响应一个网页数据
            OutputStream outputStream = socket.getOutputStream();

            // 字节输出流包装写出数据给浏览器
            // 把字节输出流 -> 打印流
            PrintStream ps = new PrintStream(outputStream);
            ps.println("HTTP/1.1 200 OK");
            ps.println("Content-Type: text/html; charset=utf-8");
            ps.println();
            ps.println("<html>");
            ps.println("<head>");
            ps.println("<meta charset=\"utf-8\">");
            ps.println("</head>");
            ps.println("<body>");
            ps.println("Test the text information for tcp server");
            ps.println("New !");
            ps.println("</body>");
            ps.println("</html>");
            socket.close();

        } catch (IOException e) {
            System.out.println("Server is offline" + socket.getInetAddress().getHostAddress());
            e.printStackTrace();
        }
    }
}
