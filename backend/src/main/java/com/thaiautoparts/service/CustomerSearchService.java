package com.thaiautoparts.service;

import java.util.List;
import java.util.Map;

public interface CustomerSearchService {
    /**
     * 使用搜索引擎API搜索客户信息
     * @param keyword 搜索关键词
     * @param source 数据源 (serpapi, brave, bing, linkedin, yellowpages)
     * @param country 国家代码 (默认TH)
     * @return 搜索结果列表
     */
    List<Map<String, Object>> searchCompanies(String keyword, String source, String country);
    
    /**
     * 批量搜索客户信息
     * @param keywords 关键词列表
     * @param source 数据源
     * @param country 国家代码
     * @return 搜索结果列表
     */
    List<Map<String, Object>> batchSearchCompanies(List<String> keywords, String source, String country);

    /**
     * 从URL获取并解析公司信息
     * @param url 网站URL
     * @param keyword 搜索关键字
     * @return 解析出的公司信息
     */
    Map<String, Object> fetchCompanyFromUrl(String url, String keyword);
}