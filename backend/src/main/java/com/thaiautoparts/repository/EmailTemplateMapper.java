package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.EmailTemplate;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface EmailTemplateMapper extends BaseMapper<EmailTemplate> {
}
