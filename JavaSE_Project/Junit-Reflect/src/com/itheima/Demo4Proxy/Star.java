package com.itheima.Demo4Proxy;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Star implements StarService{
    private String name;

    @Override
    public void Sing(String name) {
        System.out.println(name + "is sing.");
    }

    @Override
    public String dance() {
        System.out.println(name + "is dance.");
        return null;
    }
}
