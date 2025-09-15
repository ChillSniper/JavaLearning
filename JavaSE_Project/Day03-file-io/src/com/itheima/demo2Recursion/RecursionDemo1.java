package com.itheima.demo2Recursion;
import java.io.File;

public class RecursionDemo1 {
    static int cnt;
    public static void main(String[] args) {
        File dir = new File("D:/");
        dfs(dir, "QQ.exe");
    }
    /*
    *
    * */
    public static void dfs(File dir, String fileName) {
        if(dir == null || !dir.exists() || dir.isFile()) {
            System.out.println("fuck");
            return ;
        }
        // build the objs
        File[] files = dir.listFiles();

        if(files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    if(file.getName().equals(fileName)) {
                        System.out.println("已找到目标文件：" + file.getAbsolutePath());
                    }
                }
                else {
                    dfs(file, fileName);
                }
            }
        }
    }
}
