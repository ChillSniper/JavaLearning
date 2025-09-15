package com.itheima.PrintStreamDemo;

import java.io.*;

public class DataStreamTest {
    public static void main(String[] args) throws IOException {
        try(
                DataInputStream dos = new DataInputStream(new FileInputStream("D:\\Java后端开发学习\\Java基础\\Day03-file-io\\src\\com\\itheima\\test.txt"));

        ) {
            System.out.println(dos.readInt());
            System.out.println(dos.readUTF());
            System.out.println(dos.readByte());
        } catch(Exception e) {
            e.printStackTrace();
        }
    }
}
