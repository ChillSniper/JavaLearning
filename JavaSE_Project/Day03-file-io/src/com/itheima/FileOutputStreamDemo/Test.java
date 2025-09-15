package com.itheima.FileOutputStreamDemo;

import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;

public class Test {
    public static void main(String[] args) throws IOException {
        OutputStream out = new FileOutputStream("Day03-file-io/src/test.out");
        out.write(97);
        out.write('b');
        out.write('t');
        out.write('测');
        out.close();
    }

    public static void copyFile(String src, String dest) throws IOException {

    }
}
