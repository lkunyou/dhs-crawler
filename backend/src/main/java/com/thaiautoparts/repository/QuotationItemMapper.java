package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.QuotationItem;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface QuotationItemMapper extends BaseMapper<QuotationItem> {

    @Select("SELECT * FROM p_quotation_item WHERE quotation_id = #{quotationId}")
    List<QuotationItem> selectByQuotationId(@Param("quotationId") Long quotationId);
}
