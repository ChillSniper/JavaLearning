package com.itheima.demo3Stream;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class StreamDemo1 {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        list.add("张无忌");
        list.add("李天");
        List<String> new_list = new ArrayList<>();
        for (String name :list) {
            if(name.startsWith("张") && name.length() == 3){
                new_list.add(name);
            }
        }
        System.out.println(new_list);

        List<String> New_list = list.stream().filter(s -> s.startsWith("张")).filter(s -> s.length() == 3).toList();
        System.out.println(New_list);
    }
}
