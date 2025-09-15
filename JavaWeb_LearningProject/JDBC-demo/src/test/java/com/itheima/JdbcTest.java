package com.itheima;

import com.itheima.pojo.User;
import org.junit.jupiter.api.Test;

import javax.swing.plaf.nimbus.State;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class JdbcTest {
    @Test
    public void testUpdate() throws ClassNotFoundException, SQLException {
        Class.forName("com.mysql.cj.jdbc.Driver");

        String url = "jdbc:mysql://localhost:3306/web01";
        String username = "root";
        String password = "LxcFightForLove0517";
        Connection connection = DriverManager.getConnection(url, username, password);

        Statement statement =  connection.createStatement();

        int i = statement.executeUpdate("update user set age = 25 where id = 1");
        System.out.println("SQL语句执行完毕影响的记录数：" + i);
        statement.close();
        connection.close();
    }

    @Test
    public void testSelect() {
        // 数据库连接信息
        String url = "jdbc:mysql://localhost:3306/web01";
        String user = "root";
        String password = "LxcFightForLove0517";

        // 查询SQL语句
        String sql = "SELECT id, username, password, name, age FROM user WHERE username = ? AND password = ?";

        List<User> userList = new ArrayList<>();

        // JDBC代码
        try (
                // 1.加载驱动
                // Class.forName("com.mysql.cj.jdbc.Driver"); // 可省略，JDBC4.0+会自动加载

                // 2.建立连接
                Connection conn = DriverManager.getConnection(url, user, password);

                // 3.预编译SQL
                PreparedStatement pstmt = conn.prepareStatement(sql)
        ) {
            // 设置SQL参数
            pstmt.setString(1, "daqiao");
            pstmt.setString(2, "123456");

            // 4.执行查询
            ResultSet rs = pstmt.executeQuery();

            // 5.处理结果集
            while (rs.next()) {
                User u = new User();
                u.setId(rs.getInt("id"));
                u.setUsername(rs.getString("username"));
                u.setPassword(rs.getString("password"));
                u.setName(rs.getString("name"));
                u.setAge(rs.getInt("age"));
                userList.add(u);
            }

            // 6.关闭ResultSet
            rs.close();

        } catch (SQLException e) {
            e.printStackTrace();
        }

        // 输出结果
        if (userList.isEmpty()) {
            System.out.println("没有查询到用户数据！");
        } else {
            for (User u : userList) {
                System.out.println(u);
            }
        }
    }
}
