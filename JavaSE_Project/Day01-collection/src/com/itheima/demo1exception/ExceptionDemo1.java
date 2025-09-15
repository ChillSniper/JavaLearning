package com.itheima.demo1exception;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ExceptionDemo1 {
    public static void main(String[] args) throws Exception {
//        test1();
//        String s = null;
//        System.out.println(s.length());
//        try {
//            new_show();
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
        System.out.println("start");
        try {
            System.out.println(div(10, 1));
            System.out.println("Successfully.");

        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("fucking zero error.");
        }
        System.out.println("end");
    }

    public static int div(int a, int b) throws Exception {
        if(b == 0) {
            System.out.println("fuck");
            throw new Exception("fuck 0");
        }
        return a / b;
    }

    public static void test1() {
        int[] arr = {1,2,3,4,5};
        System.out.println(arr[0]);
    }
    public static void new_show() throws Exception {
        String s = "2024-07-09 11:12:33";

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
//        Date d = sdf.parse(s);
        Date d = sdf.parse(s);
        System.out.println(d);

        InputStream is = new FileInputStream("D:/meinv.png");

    }
}
