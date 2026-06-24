package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.Task;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface TaskMapper extends BaseMapper<Task> {
    
    @Select("SELECT * FROM p_task WHERE assigned_to = #{assignedTo} AND status = 'Pending' ORDER BY due_date ASC")
    List<Task> findPendingByAssignedTo(@Param("assignedTo") Long assignedTo);
    
    @Select("SELECT * FROM p_task WHERE company_id = #{companyId} ORDER BY created_at DESC")
    List<Task> findByCompanyId(@Param("companyId") Long companyId);
}
