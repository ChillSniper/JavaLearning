package com.itheima.ReflectionTest;

import org.junit.Test;

import java.lang.reflect.Constructor;

public class ReflectDemo2 {
    @Test
    public void GetClassInfo() {
        // get the class
        Class<Student> c1 = Student.class;
        System.out.println(c1.getSimpleName());
    }

    @Test
    public void GetConstructorInfo() {
        Class<Student> c1 = Student.class;
        Constructor[] cons = c1.getConstructors();
        for (Constructor c : cons) {
            System.out.println(c.getName() + "(" + c.getParameterTypes().length + ")");
        }
    }
}
