package com.itheima.Noname;

public class Test {
    public static void main(String[] args) {
        Animal a = new Animal() {
            @Override
            public void cry() {
                System.out.println("a is cry.");
            }
        };

        a.cry();
    }
}