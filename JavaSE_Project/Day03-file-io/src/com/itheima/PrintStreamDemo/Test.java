package com.itheima.PrintStreamDemo;

import java.io.FileOutputStream;
import java.io.PrintStream;

public class Test {
    public static void main(String[] args) {
        try (
                PrintStream ps = new PrintStream(new FileOutputStream("D:\\Java后端开发学习\\Java基础\\Day03-file-io\\src\\com\\itheima\\test.txt", true));
                ){
            ps.print(95);
            ps.print("\r\ntest\r\n");
            ps.println("用于测试");
        }catch(Exception e) {
            e.printStackTrace();
        }
    }
}
