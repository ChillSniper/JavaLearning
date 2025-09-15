package com.itheima.thread_safety;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Account {
    private double money;
    private String cardId;
    public void drawMoney(double amount) {
        String name = Thread.currentThread().getName();
        if(this.money >= amount) {
            System.out.println(name + "get" + this.money);
            this.money -= amount;
            System.out.println(name + "successfully get the money" + ", and the account left" + this.money);
        }
        else {
            System.out.println(name + "failed to get the money");
        }
    }
}
