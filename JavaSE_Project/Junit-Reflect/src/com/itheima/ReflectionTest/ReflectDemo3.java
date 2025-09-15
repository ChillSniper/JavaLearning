package com.itheima.ReflectionTest;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;

public class ReflectDemo3 {
    public static void main(String[] args) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        ArrayList<String> list = new ArrayList<>();
        list.add("张无忌");
        list.add("令狐冲");
        Class c = list.getClass();
        Method add = c.getDeclaredMethod("add", Object.class );
        add.invoke(list, "t");
        add.invoke(list, "test");
        for (String s : list) {
            System.out.println(s);
        }

    }
}
