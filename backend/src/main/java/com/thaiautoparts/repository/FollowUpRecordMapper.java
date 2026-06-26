package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.FollowUpRecord;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface FollowUpRecordMapper extends BaseMapper<FollowUpRecord> {
    
    @Select("SELECT * FROM p_follow_up_record WHERE company_id = #{companyId} ORDER BY created_at DESC")
    List<FollowUpRecord> findByCompanyId(@Param("companyId") Long companyId);
    
    @Select("SELECT COUNT(*) FROM p_follow_up_record WHERE outcome = #{outcome}")
    Long countByOutcome(@Param("outcome") String outcome);
    
    @Select("SELECT COUNT(*) FROM p_follow_up_record WHERE follow_up_type = #{type}")
    Long countByType(@Param("type") String type);
}
