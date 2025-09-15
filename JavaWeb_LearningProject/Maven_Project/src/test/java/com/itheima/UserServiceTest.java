package com.itheima;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;

public class UserServiceTest {
    @Test
    public void testGetAge() {
        UserService userService = new UserService();
        Integer age = userService.getAge("320684200505170277");
        System.out.println(age);
    }
    @Test
    public void testGenderWithAssert() {
        UserService u = new UserService();
        String gender = u.getGender("320684200505170277");
        Assertions.assertEquals("男", gender);
    }
    @Test
    public void testGenderWithAssertThrow() {
        UserService u = new UserService();
        Assertions.assertThrows(IllegalArgumentException.class, () -> {
            u.getGender(null);
        });
    }

    @ParameterizedTest
    @ValueSource(strings = {"320684200505170277", "320684200505170278", "320684200505170279", "320684200505170280"})
    public void testGetGenderNew(String idCard) {
        UserService u = new UserService();
        String gender = u.getGender(idCard);
        Assertions.assertEquals("男", gender);
    }
}
