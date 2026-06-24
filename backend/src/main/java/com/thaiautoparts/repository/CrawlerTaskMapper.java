package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.CrawlerTask;
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface CrawlerTaskMapper extends BaseMapper<CrawlerTask> {
}
