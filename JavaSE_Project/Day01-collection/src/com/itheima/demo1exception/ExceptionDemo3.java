package com.itheima.demo1exception;

public class ExceptionDemo3 {
    public static void main(String[] args) throws ItheimaAgeLegal {
        saveAge(100);
    }
    // 需求 year < 1 || year > 200 认定为非法异常
    public static void saveAge(int age) throws ItheimaAgeLegal {
        if(age < 1 || age > 200) {
            throw new ItheimaAgeLegal("The year num is invalid");
        } else {
            System.out.println("The age is valid.");

        }
    }
}
