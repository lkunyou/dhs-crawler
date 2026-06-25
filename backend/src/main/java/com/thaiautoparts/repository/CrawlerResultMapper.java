package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.CrawlerResult;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface CrawlerResultMapper extends BaseMapper<CrawlerResult> {

    @Select("SELECT status, COUNT(*) as count FROM p_crawler_result WHERE task_id = #{taskId} GROUP BY status")
    List<Map<String, Object>> countByStatus(@Param("taskId") Long taskId);

    @Select("SELECT source_type, COUNT(*) as count FROM p_crawler_result WHERE task_id = #{taskId} GROUP BY source_type")
    List<Map<String, Object>> countBySource(@Param("taskId") Long taskId);
}
