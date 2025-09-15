package com.itheima.aop;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.*;
import org.springframework.stereotype.Component;

@Slf4j
@Aspect
@Component
public class MyAspect1 {

    @Pointcut("execution(* com.itheima.service.impl.*.*(..))")
    public void pt() {}

    // 前置通知
    @Before("execution(* com.itheima.service.impl.*.*(..))")
    public void before() {
        log.info("before...");
        // before the method execution

    }

    @Around("execution(* com.itheima.service.impl.*.*(..))")
    public Object around(ProceedingJoinPoint joinPoint) throws Throwable {
        log.info("around... before...");
        Object result = joinPoint.proceed();
        log.info("around... after...");
        return result;
    }

    // 后置通知
    // 无论是否出现异常都会执行！
    @After("execution(* com.itheima.service.impl.*.*(..))")
    public void after() {
        log.info("after...");
    }

    // 返回后通知，目标方法运行之后运行，如果出现异常则不会运行
    @AfterReturning("execution(* com.itheima.service.impl.*.*(..))")
    public void afterReturning() {
        log.info("afterReturning...");
    }

    // 异常后通知，目标方法运行后运行，只有出现异常才会运行！
    @AfterThrowing("execution(* com.itheima.service.impl.*.*(..))")
    public void afterThrowing() {
        log.info("afterThrowing...");
    }
}