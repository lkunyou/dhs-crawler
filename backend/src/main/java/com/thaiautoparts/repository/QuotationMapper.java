package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.Quotation;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface QuotationMapper extends BaseMapper<Quotation> {

    @Select("<script>" +
            "SELECT company_id AS companyId, COUNT(*) AS cnt FROM p_quotation " +
            "WHERE company_id IN " +
            "<foreach collection='companyIds' item='id' open='(' separator=',' close=')'>#{id}</foreach> " +
            "GROUP BY company_id" +
            "</script>")
    List<Map<String, Object>> countByCompanyIds(@Param("companyIds") List<Long> companyIds);
}
