package com.itheima.demo3Stream;

import java.util.*;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class StreamDemo2 {
    public static void main(String[] args) {
//        Collection<String> list = new ArrayList<>();
//        list.add("test");
//        Stream<String> s1 = list.stream();
//
//        Map<String, Integer> mp = new HashMap<>();
//        mp.put("test", 1);
//        Stream<String> ss = mp.keySet().stream();
//        Stream<Integer> si = mp.values().stream();
//        Stream<Map.Entry<String, Integer>> sd = mp.entrySet().stream();
//
//        String[] names = {"Herbert", "Li", "Ack"};
//        Stream<String> ss1 = Arrays.stream(names);
//        System.out.println(ss1.count());
//
//        list.stream().filter(s -> s.startsWith("张") && s.length() == 3).forEach(System.out::println);

//        List<Double> scores = new ArrayList<>();
//        scores.add(1.0);
//        scores.add(2.0);
//        scores.add(3.0);
//        scores.add(4.0);
//        scores.add(5.0);
//        scores.stream().forEach(System.out::println);
//        scores.stream().sorted((o1, o2) -> Double.compare(o2, o1)).forEach(System.out::println);
        List<Teacher> tcs = new ArrayList<>();
        tcs.add(new Teacher("Jack", 23, 3000));
        tcs.add(new Teacher("Lee", 33, 4500));
        tcs.add(new Teacher("Wang", 40, 9000));
        tcs.add(new Teacher("Zhao", 53, 7000));

        tcs.stream().filter(t ->t.getSalary() > 3000).forEach(System.out::println);
        System.out.println("-----------------------------");
        long cnt = tcs.stream().filter(t -> t.getSalary() > 3000).count();
        System.out.println(cnt);
        System.out.println("----------------------------");

        Optional<Teacher> max = tcs.stream().max(Comparator.comparing(Teacher::getSalary));
        Teacher maxTeacher = max.get();
        System.out.println(maxTeacher);

        Map<String, Double> mp = tcs.stream().collect(Collectors.toMap(new Function<Teacher, String>() {
            @Override
            public String apply(Teacher t) {
                return t.getName();
            }
        }, new Function<Teacher, Double>() {
            @Override
            public Double apply(Teacher t) {
                return t.getSalary();
            }
        }));
        System.out.println(mp);
    }
}
