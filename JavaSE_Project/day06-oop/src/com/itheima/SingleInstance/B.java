package com.itheima.SingleInstance;

public class B {
    private static B b = null;
    private B() {}
    public static B getInstance() {
        if (b == null) {
            System.out.println("this is B");
            b = new B();
        }
        return b;
    }
}

