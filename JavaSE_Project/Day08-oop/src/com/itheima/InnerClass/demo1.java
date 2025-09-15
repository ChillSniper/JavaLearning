package com.itheima.InnerClass;

public class demo1 {
    public static void main(String[] args) {
        Outer.InnerClass oi = new Outer().new InnerClass();
        oi.show();
    }

}
