package com.itheima.demo2Recursion;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;

public class Demo3Charset {

    public static void main(String[] args) throws UnsupportedEncodingException {
        String name = "测试数据abs";
        byte[] bytes = name.getBytes("GBK");
        System.out.println(bytes.length);
        System.out.println(Arrays.toString(bytes));
        String new_name = new String(bytes, "GBK");
        System.out.println(new_name);
    }

}
