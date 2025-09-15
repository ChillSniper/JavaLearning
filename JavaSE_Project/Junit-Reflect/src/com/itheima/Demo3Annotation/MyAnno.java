package com.itheima.Demo3Annotation;

public @interface MyAnno {
    String value();
    int age() default 18;
    String[] address();
}
