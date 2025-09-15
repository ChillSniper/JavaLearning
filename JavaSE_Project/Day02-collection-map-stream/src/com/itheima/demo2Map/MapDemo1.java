package com.itheima.demo2Map;

import java.util.HashMap;
import java.util.Map;

public class MapDemo1 {
    public static void main(String[] args) {
        Map<String, Integer> mp = new HashMap<>();
        mp.put("jack", 100);
        mp.put("tom", 200);
        mp.put("jill", 300);
        mp.put("tom", 400);
        mp.put(null, null);
        System.out.println(mp);
    }
}
