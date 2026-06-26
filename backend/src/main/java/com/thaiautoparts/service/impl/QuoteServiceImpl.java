package com.thaiautoparts.service.impl;

import cn.hutool.core.bean.BeanUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.Quotation;
import com.thaiautoparts.entity.QuotationItem;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.QuotationItemMapper;
import com.thaiautoparts.repository.QuotationMapper;
import com.thaiautoparts.service.QuoteService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class QuoteServiceImpl implements QuoteService {

    private final QuotationMapper quotationMapper;
    private final QuotationItemMapper quotationItemMapper;
    private final CompanyMapper companyMapper;

    @Override
    public PageResult<Map<String, Object>> listQuotes(int page, int size, String companyName, String status) {
        LambdaQueryWrapper<Quotation> wrapper = new LambdaQueryWrapper<>();

        if (StrUtil.isNotBlank(status)) {
            wrapper.eq(Quotation::getStatus, status);
        }

        if (StrUtil.isNotBlank(companyName)) {
            List<Company> companies = companyMapper.selectList(new LambdaQueryWrapper<Company>()
                    .like(Company::getCompanyName, companyName));
            if (!companies.isEmpty()) {
                List<Long> companyIds = companies.stream().map(Company::getId).collect(Collectors.toList());
                wrapper.in(Quotation::getCompanyId, companyIds);
            } else {
                wrapper.in(Quotation::getCompanyId, List.of(-1L));
            }
        }

        wrapper.orderByDesc(Quotation::getCreatedAt);

        Page<Quotation> pageParam = new Page<>(page, size);
        Page<Quotation> result = quotationMapper.selectPage(pageParam, wrapper);

        List<Map<String, Object>> dtoList = result.getRecords().stream()
                .map(this::convertToMap)
                .collect(Collectors.toList());

        return new PageResult<>(result.getTotal(), page, size, dtoList);
    }

    @Override
    public Map<String, Object> getQuoteById(Long id) {
        Quotation quotation = quotationMapper.selectById(id);
        if (quotation == null) {
            throw new RuntimeException("Quote not found: " + id);
        }
        Map<String, Object> map = convertToMap(quotation);
        List<QuotationItem> items = quotationItemMapper.selectByQuotationId(id);
        map.put("items", items);
        return map;
    }

    @Override
    @Transactional
    public Quotation createQuote(Quotation quotation) {
        if (StrUtil.isBlank(quotation.getQuotationNo())) {
            quotation.setQuotationNo(generateQuoteNo());
        }

        if (quotation.getStatus() == null) {
            quotation.setStatus("draft");
        }

        if (quotation.getCurrency() == null) {
            quotation.setCurrency("USD");
        }

        // 计算总金额并保存报价
        BigDecimal totalAmount = calculateTotalAmount(quotation.getItems());
        quotation.setTotalAmount(totalAmount);
        quotationMapper.insert(quotation);

        // 保存报价明细
        saveQuotationItems(quotation.getId(), quotation.getItems());

        return quotation;
    }

    @Override
    @Transactional
    public Quotation updateQuote(Long id, Quotation quotation) {
        Quotation existing = quotationMapper.selectById(id);
        if (existing == null) {
            throw new RuntimeException("Quote not found: " + id);
        }

        BeanUtil.copyProperties(quotation, existing, "id", "createdAt", "quotationNo", "totalAmount", "items");

        // 重新计算总金额
        BigDecimal totalAmount = calculateTotalAmount(quotation.getItems());
        existing.setTotalAmount(totalAmount);

        quotationMapper.updateById(existing);

        // 删除旧明细，保存新明细
        if (quotation.getItems() != null) {
            quotationItemMapper.delete(new LambdaQueryWrapper<QuotationItem>()
                    .eq(QuotationItem::getQuotationId, id));
            saveQuotationItems(id, quotation.getItems());
        }

        return existing;
    }

    @Override
    @Transactional
    public void deleteQuote(Long id) {
        quotationItemMapper.delete(new LambdaQueryWrapper<QuotationItem>()
                .eq(QuotationItem::getQuotationId, id));
        quotationMapper.deleteById(id);
    }

    private BigDecimal calculateTotalAmount(List<QuotationItem> items) {
        if (items == null || items.isEmpty()) {
            return BigDecimal.ZERO;
        }
        return items.stream()
                .map(item -> item.getUnitPrice().multiply(BigDecimal.valueOf(item.getQuantity())))
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }

    private void saveQuotationItems(Long quotationId, List<QuotationItem> items) {
        if (items == null || items.isEmpty()) {
            return;
        }
        for (QuotationItem item : items) {
            item.setQuotationId(quotationId);
            item.setLineTotal(item.getUnitPrice().multiply(BigDecimal.valueOf(item.getQuantity())));
            quotationItemMapper.insert(item);
        }
    }

    @Override
    public List<Map<String, Object>> listAll() {
        List<Quotation> list = quotationMapper.selectList(new LambdaQueryWrapper<Quotation>().orderByDesc(Quotation::getCreatedAt));
        return list.stream().map(this::convertToMap).collect(Collectors.toList());
    }

    private String generateQuoteNo() {
        String prefix = "QT";
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss"));
        return prefix + timestamp;
    }

    private Map<String, Object> convertToMap(Quotation quotation) {
        Map<String, Object> map = new HashMap<>();
        map.put("id", quotation.getId());
        map.put("quoteNo", quotation.getQuotationNo());
        map.put("companyId", quotation.getCompanyId());
        map.put("totalAmount", quotation.getTotalAmount());
        map.put("validDate", quotation.getValidUntil());
        map.put("remark", quotation.getNotes());
        map.put("status", quotation.getStatus());
        map.put("createdAt", quotation.getCreatedAt());
        map.put("updatedAt", quotation.getUpdatedAt());

        // 兼容旧数据：如果没有明细，使用主表字段
        map.put("productName", quotation.getProductName());
        map.put("productModel", quotation.getProductDescription());
        map.put("quantity", quotation.getQuantity());
        map.put("unitPrice", quotation.getUnitPrice());

        if (quotation.getCompanyId() != null) {
            Company company = companyMapper.selectById(quotation.getCompanyId());
            if (company != null) {
                map.put("companyName", company.getCompanyName());
                map.put("companyEmail", company.getEmail());
            }
        }

        return map;
    }
}
