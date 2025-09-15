package com.itheima.aop;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.springframework.stereotype.Component;

import java.util.Arrays;

@Slf4j
@Aspect
@Component
public class MyAspect6 {
    @Before("execution(* com.itheima.service.*.*(..))")
    public void before(JoinPoint joinPoint) {
        log.info("before...");
        // 获取目标对象
        Object target = joinPoint.getTarget();
        log.info("get object target: {}", target);
        // 获取目标类
        String name = joinPoint.getTarget().getClass().getName();
        log.info("get object target class name: {}", name);
        // 获取目标方法
        String methodName = joinPoint.getSignature().getName();
        log.info("get object method name: {}", methodName);
        // 获取方法参数
        Object[] args = joinPoint.getArgs();
        log.info("get object args: {}", Arrays.toString(args));
    }

    @Around("execution(* com.itheima.service.*.*(..))")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        log.info("around...before...");
        Object result = pjp.proceed();
        log.info("around...after...");
        return result;
    }

}
