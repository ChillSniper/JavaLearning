package com.itheima.service;

import com.itheima.pojo.Dept;

import java.util.List;

public interface DeptService {
    /**
     * 查询全部部门
     */
    public List<Dept> findAll();

    /**
     * 根据ID删除部门
     */
    void delete(Integer id);

    /**
     * 新增部门
     */
    void save(Dept dept);

    /**
     * 根据ID查询部门
     */
    Dept getInfo(Integer id);

    /**
     * 更新部门
     */
    void update(Dept dept);
}
