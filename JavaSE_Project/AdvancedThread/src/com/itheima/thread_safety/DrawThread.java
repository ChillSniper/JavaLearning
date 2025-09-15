package com.itheima.thread_safety;

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
