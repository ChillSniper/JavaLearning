package com.itheima.DemoTcp3;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;

public class ServerReader extends Thread {
    private Socket socket;
    public ServerReader(Socket socket) {
        this.socket = socket;
    }
    @Override
    public void run() {
        try {
            InputStream inputStream = socket.getInputStream();
            DataInputStream dataInputStream = new DataInputStream(inputStream);

            // 读取数据

            while (true) {
                String data = dataInputStream.readUTF();
                System.out.println("msg = " + data);
                System.out.println("Server ip = " + socket.getInetAddress() + "Server port = " + socket.getPort());
                System.out.println("-------------------------------------------------------------");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
