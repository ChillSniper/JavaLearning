package com.itheima.Lambda;

public class LambdaDemo1 {
    public static void main(String[] args) {
        Swim s1 = () -> {
            System.out.println("tesst");
        };
        s1.swimming();
    }

}

abstract class Animal {
    public abstract void cry();

}

@FunctionalInterface // 声明函数式接口的注解！
interface Swim {
    void swimming();
//    void S();
}