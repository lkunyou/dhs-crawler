package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.Company;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface CompanyMapper extends BaseMapper<Company> {
    
    @Select("SELECT COUNT(*) FROM p_company WHERE is_duplicate = 0")
    Long countTotal();
    
    @Select("SELECT lead_grade, COUNT(*) as count FROM p_company WHERE is_duplicate = 0 GROUP BY lead_grade")
    List<Map<String, Object>> countByLeadGrade();
    
    @Select("SELECT status, COUNT(*) as count FROM p_company WHERE is_duplicate = 0 GROUP BY status")
    List<Map<String, Object>> countByStatus();
    
    @Select("SELECT source, COUNT(*) as count FROM p_company WHERE is_duplicate = 0 GROUP BY source")
    List<Map<String, Object>> countBySource();
    
    @Select("SELECT * FROM p_company WHERE company_name = #{companyName} AND country = #{country} LIMIT 1")
    Company findByCompanyNameAndCountry(@Param("companyName") String companyName, @Param("country") String country);
}
