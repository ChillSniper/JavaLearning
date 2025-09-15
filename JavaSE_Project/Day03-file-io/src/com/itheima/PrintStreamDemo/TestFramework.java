package com.itheima.PrintStreamDemo;

import org.apache.commons.io.FileUtils;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class TestFramework {
    public static void main(String[] args) throws IOException {
//        FileUtils.copyFile(new File("Day03-file-io\\src\\com\\itheima\\test.txt"),
//                new File("D:\\Java后端开发学习\\Java基础\\Day03-file-io\\src\\com\\itheima\\test_out.txt"));
        Files.copy(Path.of("D:\\Java后端开发学习\\Java基础\\Day03-file-io\\src\\com\\itheima\\test.txt"), Path.of("D:\\Java后端开发学习\\Java基础\\Day03-file-io\\src\\com\\itheima\\test.txt"));
    }
}
