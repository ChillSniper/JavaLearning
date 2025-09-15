package com.itheima.demo1hashset;

import java.util.LinkedHashSet;
import java.util.Set;
import java.util.HashSet;
import java.util.TreeSet;

public class setDemo1 {
    public static void main(String[] args) {
        Set<String> st = new TreeSet<>();
        st.add("B");
        st.add("A");
        System.out.println(st);
    }
}
