package com.itheima.mapper;

import com.itheima.pojo.User;
import org.apache.ibatis.annotations.*;


import java.util.List;

@Mapper //
public interface UserMapper {
//    @Select("select * from user")
    public List<User> findAll();

    @Delete("delete from user where id = #{id}")
    public void deleteById(Integer id);

    @Insert("insert into user (id, username, password, name, age) values (#{id}, #{username}, #{password}, #{name}, #{age})")
    public void insertUser(User user);

    @Select("select * from user where username = #{username} and password = #{password}")
    public User findByUserNameAndPassword(@Param("username")String username, @Param("password")String password);
}
