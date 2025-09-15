package com.itheima.ReflectionTest;

public class ReflectDemo1 {
    public static void main(String[] args) throws Exception {
        Class c1 = Student.class;
        // to print the name of class
        System.out.println(c1);
        Class c2 = Class.forName("com.itheima.ReflectionTest.Student");
        System.out.println(c2);
        System.out.println(c1.equals(c2));

        Student s = new Student();
        Class s3 = s.getClass();
        System.out.println(s3.equals(c2));

    }

}
