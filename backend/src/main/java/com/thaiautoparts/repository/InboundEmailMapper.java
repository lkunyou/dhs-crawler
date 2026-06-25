package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.InboundEmail;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface InboundEmailMapper extends BaseMapper<InboundEmail> {
}