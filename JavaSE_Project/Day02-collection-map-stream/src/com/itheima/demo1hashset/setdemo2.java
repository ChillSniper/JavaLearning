package com.itheima.demo1hashset;

import java.util.HashSet;
import java.util.Set;

public class setdemo2 {
    public static void main(String[] args) {
        Student s1 = new Student("张三", 18, "男");
        Student s2 = new Student("张三", 18, "男");
        Set<Student> st = new HashSet<Student>();
        st.add(s1);
        st.add(s2);
        System.out.println(st);
    }

}
