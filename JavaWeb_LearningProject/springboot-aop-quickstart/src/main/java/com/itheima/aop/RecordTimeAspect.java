package com.itheima.aop;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;
@Slf4j
@Aspect
@Component
public class RecordTimeAspect {
    @Around("execution(* com.itheima.service.impl.*.*(..))")
    public Object recordTime(ProceedingJoinPoint joinPoint) throws Throwable {
        // record the start time
        long begin = System.currentTimeMillis();
        // execute the original method

        Object result = joinPoint.proceed();

        // record the end time, then calculate the time difference
        long end = System.currentTimeMillis();
        log.info("method execute time: {} ms", (end - begin));

        return result;
    }
}
