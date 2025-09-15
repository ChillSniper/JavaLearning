package com.itheima.demo4_synchronized_code;

import com.itheima.demo4_synchronized_code.Account;

public class DrawThread extends Thread {
    private Account account;
    public DrawThread(String name, Account account) {
        super(name);
        this.account = account;
    }

    @Override
    public void run() {
        // get money
        account.drawMoney(100000);
    }
}
