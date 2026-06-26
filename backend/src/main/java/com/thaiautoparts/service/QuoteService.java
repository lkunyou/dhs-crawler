package com.thaiautoparts.service;

import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.entity.Quotation;

import java.util.Map;

public interface QuoteService {
    PageResult<Map<String, Object>> listQuotes(int page, int size, String companyName, String status);
    Map<String, Object> getQuoteById(Long id);
    Quotation createQuote(Quotation quotation);
    Quotation updateQuote(Long id, Quotation quotation);
    void deleteQuote(Long id);
    java.util.List<Map<String, Object>> listAll();
}