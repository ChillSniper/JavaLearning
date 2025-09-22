package com.itheima.factory;

import com.itheima.dao.UserDao;
import com.itheima.dao.impl.UserDaoImpl;
import org.springframework.beans.factory.FactoryBean;
//FactoryBean创建对象
public class UserDaoFactoryBean implements FactoryBean<UserDao> {
    //返回要创建的对象
    public UserDao getObject() throws Exception {
        return new UserDaoImpl();
    }
    //返回要创建的对象类型
    public Class<?> getObjectType() {
        return UserDao.class;
    }
    public boolean isSingleton() {
//        return false;
        return true; //默认是true
    }
}