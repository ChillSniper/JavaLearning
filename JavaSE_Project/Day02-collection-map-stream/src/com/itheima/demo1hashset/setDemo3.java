package com.itheima.demo1hashset;

import java.util.Comparator;
import java.util.Set;
import java.util.TreeSet;

public class setDemo3 {
    public static void main(String[] args) {
        Set<Teacher> teachers = new TreeSet<>(Comparator.comparingDouble(Teacher::getSalary));
        teachers.add(new Teacher("老陈", 20, 0.5));
        teachers.add(new Teacher("dlei", 18, 0.1));
        teachers.add(new Teacher("Li", 12, 155151.61));
        System.out.println(teachers);
    }

}
