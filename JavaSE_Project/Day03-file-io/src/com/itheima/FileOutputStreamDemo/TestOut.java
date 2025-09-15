package com.itheima.FileOutputStreamDemo;

import java.io.FileWriter;
import java.io.Writer;

public class TestOut {
    public static void main(String[] args) {
        try (
                Writer wt = new FileWriter("Day03-file-io/src/com/itheima/output.txt");
                ){
            wt.write("This is a test\n");
            wt.write("This is another test");
            wt.write("\n测试");
            char[] cs = "java".toCharArray();
            wt.write(cs);
            wt.write("\r\n");
            wt.write(cs, 1, 2);
            wt.flush();
//            wt.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
