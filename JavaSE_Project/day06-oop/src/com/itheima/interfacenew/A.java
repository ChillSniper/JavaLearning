package com.itheima.interfacenew;

public interface A {
    // 1. 默认方法(普通实例方法)，但是务必加上 default
    // 默认public
    default void go(){

    }

    // 2. 私有方法
    // 即私有的示例方法
    private void run() {

    }

    // 3. 静态方法
    // 特别注意：其只能使用当前接口名来调用！
    static void show() {

    }
}
