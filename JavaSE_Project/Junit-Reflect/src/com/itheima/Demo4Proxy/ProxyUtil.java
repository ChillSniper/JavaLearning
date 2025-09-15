package com.itheima.Demo4Proxy;

import javax.swing.*;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class ProxyUtil {
    public static StarService createProxy(Star s) {
        StarService proxy = (StarService) Proxy.newProxyInstance(Proxy.class.getClassLoader(),
                s.getClass().getInterfaces(),
                new InvocationHandler() {
            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
//                return null;
                // 复用逻辑
                Object result = method.invoke(s, args);

                // 复用逻辑

                return result;
            }
        });
        return proxy;
    }
}
