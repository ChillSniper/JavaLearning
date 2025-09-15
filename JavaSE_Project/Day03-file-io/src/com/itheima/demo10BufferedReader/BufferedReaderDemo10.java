package com.itheima.demo10BufferedReader;

import java.io.*;

public class BufferedReaderDemo10 {
    public static void main(String[] args) {
        try (
                Reader fr = new FileReader("Day03-file-io\\src\\com\\itheima\\test.txt");
                BufferedReader br = new BufferedReader(fr);
                ) {
            String s;
            while ((s = br.readLine()) != null) {
                System.out.println(s);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
