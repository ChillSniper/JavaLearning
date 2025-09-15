package com.itheima.demo6Collection;

import java.util.*;
import java.util.function.Consumer;

public class Test {
    public static void main(String[] args) {
        ArrayList<String> names = new ArrayList<>();
        names.add("A");
        names.add("B");
        names.add("C");
        names.add("D");

        names.forEach(System.out::println);

    }

}
