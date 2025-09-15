package com.itheima.FileInputStreamDemo1;

import java.io.*;
import java.util.Arrays;

public class Test {
    public static void main(String[] args) throws IOException {
        InputStream in = new FileInputStream("D:\\Java后端开发学习\\Java基础\\Day03-file-io\\src\\com\\itheima\\test.txt");
        byte[] buffer = new byte[1024];

        // 定义一个变量
        int len = 0;
        while((len = in.read(buffer)) != -1) {
            String str = new String(buffer, 0, len);
            System.out.print(str);
        }
    }
}
