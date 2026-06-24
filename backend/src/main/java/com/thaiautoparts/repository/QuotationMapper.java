package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.Quotation;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface QuotationMapper extends BaseMapper<Quotation> {
}
