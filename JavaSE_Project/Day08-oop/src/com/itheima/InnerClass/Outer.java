package com.itheima.InnerClass;

public class Outer {
    // 成员内部类, 没有static修饰，属于外部类的对象持有。
    public class InnerClass {
        public void show() {
            System.out.println("InnerClass.show");
        }
    }
}
