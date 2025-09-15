package com.itheima.demo4_synchronized_code;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Account {
    private double money;
    private String cardId;

    private final Lock lk = new ReentrantLock();

    public void drawMoney(double amount) {
        String name = Thread.currentThread().getName();
        lk.lock();
        try {
            if(this.money >= amount) {
                System.out.println(name + "get" + this.money);
                this.money -= amount;
                System.out.println(name + "successfully get the money" + ", and the account left" + this.money);
            }
            else {
                System.out.println(name + "failed to get the money");
            }
        } finally {
            lk.unlock();
        }
    }
}
