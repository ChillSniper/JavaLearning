package com.itheima.GenericDemo4;

import java.lang.reflect.Array;

public class Test {
    public static void main(String[] args) {
        // 学会定义泛型方法
        int [] arr = {1,2,3,4,5};
        PrintArray(arr);
    }
    public static <T> void PrintArray(T t) {
        int length = Array.getLength(t);
        for (int i = 0; i < length; i++) {
            System.out.println(Array.get(t, i));
        }
    }
}
