package com.itheima.demo7FileReader;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.Reader;
import java.io.FileReader;

public class Test {
    public static void main(String[] args) throws FileNotFoundException {
        try (
                Reader fr = new FileReader("Day03-file-io\\src\\com\\itheima\\test.txt");
        ) {
            char[] buf = new char[1024];
            int len;
            while ((len = fr.read(buf)) != -1) {
                String str = new String(buf, 0, len);
                System.out.println(str);
            }
        }catch (Exception e) {
            e.printStackTrace();
        }
    }
}
