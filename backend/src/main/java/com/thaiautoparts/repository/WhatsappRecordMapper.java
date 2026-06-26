package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.WhatsappRecord;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

@Mapper
public interface WhatsappRecordMapper extends BaseMapper<WhatsappRecord> {

    @Select("<script>" +
            "SELECT company_id AS companyId, COUNT(*) AS cnt FROM p_whatsapp_record " +
            "WHERE company_id IN " +
            "<foreach collection='companyIds' item='id' open='(' separator=',' close=')'>#{id}</foreach> " +
            "GROUP BY company_id" +
            "</script>")
    List<Map<String, Object>> countByCompanyIds(@Param("companyIds") List<Long> companyIds);
    
    @Select("SELECT COUNT(*) FROM p_whatsapp_record WHERE status = #{status}")
    Long countByStatus(@Param("status") String status);
}
