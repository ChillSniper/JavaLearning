package com.itheima.StaticInner;

public class Outer {
    // 静态内部类：属于外部类本身持有
    public static String schoolName = "Jilin University";
    public int age;
    public static class StaticInner {
        public void show() {
            System.out.println(schoolName);

            // 2. 静态内部类中，不可以直接访问外部类的实例成员！
            //            System.out.println(age);
        }
    }
}
