package com.itheima.code;

import java.util.Arrays;

public class code_demo1 {
    public static String[] cards = new String[5];
    static {
        System.out.println("code_demo1 was tested.");
        cards[0] = "1";
        cards[1] = "2";
        cards[2] = "3";
        cards[3] = "4";
        cards[4] = "5";
    }
    public static void main(String[] args) {
        System.out.println(Arrays.toString(cards));
    }
}
