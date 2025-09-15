package com.itheima.demo1_file;

import java.io.File;

public class FileDemo1 {
    public static void main(String[] args) {
        File f1 = new File("D:/resource/test.txt");
        File f2 = new File("D:\\ComputerScienceLearning\\计算机网络-中科大\\cn");
        System.out.println(f2.exists());
        System.out.println(f2.length());
        System.out.println(f2.canRead());
        // how to read the f2 ?
        System.out.println(f2.canWrite());
        System.out.println(f2.hashCode());

        File[] files = f2.listFiles();

    }
}
