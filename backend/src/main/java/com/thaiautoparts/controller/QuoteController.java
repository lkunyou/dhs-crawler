package com.thaiautoparts.controller;

import com.alibaba.excel.EasyExcel;
import com.alibaba.excel.context.AnalysisContext;
import com.alibaba.excel.read.listener.ReadListener;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.Quotation;
import com.thaiautoparts.service.QuoteService;
import jakarta.servlet.http.HttpServletResponse;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.math.BigDecimal;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequestMapping("/quotes")
@RequiredArgsConstructor
public class QuoteController {

    private final QuoteService quoteService;

    private final ConcurrentHashMap<String, List<Quotation>> tempQuoteStore = new ConcurrentHashMap<>();

    @GetMapping
    public Result<PageResult<Map<String, Object>>> listQuotes(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String companyName,
            @RequestParam(required = false) String status) {
        PageResult<Map<String, Object>> result = quoteService.listQuotes(page, size, companyName, status);
        return Result.success(result);
    }

    @GetMapping("/{id}")
    public Result<Map<String, Object>> getQuote(@PathVariable Long id) {
        Map<String, Object> quote = quoteService.getQuoteById(id);
        return Result.success(quote);
    }

    @PostMapping
    public Result<Quotation> createQuote(@RequestBody Quotation quotation) {
        Quotation created = quoteService.createQuote(quotation);
        return Result.success(created);
    }

    @PutMapping("/{id}")
    public Result<Quotation> updateQuote(@PathVariable Long id, @RequestBody Quotation quotation) {
        Quotation updated = quoteService.updateQuote(id, quotation);
        return Result.success(updated);
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteQuote(@PathVariable Long id) {
        quoteService.deleteQuote(id);
        return Result.success();
    }

    @GetMapping("/export")
    public void exportQuotes(HttpServletResponse response) throws IOException {
        response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        response.setCharacterEncoding("utf-8");
        String fileName = URLEncoder.encode("报价单列表", StandardCharsets.UTF_8).replaceAll("\\+", "%20");
        response.setHeader("Content-disposition", "attachment;filename*=utf-8''" + fileName + ".xlsx");

        List<Map<String, Object>> list = quoteService.listAll();
        List<QuoteExcel> excelList = new ArrayList<>();
        for (Map<String, Object> q : list) {
            QuoteExcel e = new QuoteExcel();
            e.setQuoteNo((String) q.get("quoteNo"));
            e.setCompanyName((String) q.get("companyName"));
            e.setValidDate(q.get("validDate") != null ? q.get("validDate").toString() : "");
            e.setTotalAmount(q.get("totalAmount") != null ? new BigDecimal(q.get("totalAmount").toString()) : null);
            e.setStatus((String) q.get("status"));
            e.setRemark((String) q.get("remark"));
            excelList.add(e);
        }
        EasyExcel.write(response.getOutputStream(), QuoteExcel.class).sheet("报价单").doWrite(excelList);
    }

    @PostMapping("/import-preview")
    public Result<Map<String, Object>> importQuotesPreview(@RequestParam("file") MultipartFile file) throws IOException {
        List<Quotation> list = new ArrayList<>();
        EasyExcel.read(file.getInputStream(), QuoteExcel.class, new ReadListener<QuoteExcel>() {
            @Override
            public void invoke(QuoteExcel data, AnalysisContext context) {
                Quotation q = new Quotation();
                q.setQuotationNo(data.getQuoteNo());
                q.setStatus(data.getStatus());
                q.setNotes(data.getRemark());
                list.add(q);
            }
            @Override
            public void doAfterAllAnalysed(AnalysisContext context) {}
        }).sheet().doRead();

        String tempId = UUID.randomUUID().toString();
        tempQuoteStore.put(tempId, list);

        Map<String, Object> result = new HashMap<>();
        result.put("tempId", tempId);
        result.put("total", list.size());
        result.put("list", list);
        return Result.success(result);
    }

    @PostMapping("/import-confirm")
    public Result<Void> importQuotesConfirm(@RequestParam("tempId") String tempId) {
        List<Quotation> list = tempQuoteStore.remove(tempId);
        if (list == null || list.isEmpty()) {
            return Result.error("预览数据已过期或不存在，请重新上传");
        }
        for (Quotation q : list) {
            quoteService.createQuote(q);
        }
        return Result.success();
    }

    @PostMapping("/import-cancel")
    public Result<Void> importQuotesCancel(@RequestParam("tempId") String tempId) {
        tempQuoteStore.remove(tempId);
        return Result.success();
    }

    @Data
    public static class QuoteExcel {
        @com.alibaba.excel.annotation.ExcelProperty("报价编号")
        private String quoteNo;
        @com.alibaba.excel.annotation.ExcelProperty("客户名称")
        private String companyName;
        @com.alibaba.excel.annotation.ExcelProperty("有效期")
        private String validDate;
        @com.alibaba.excel.annotation.ExcelProperty("总金额")
        private BigDecimal totalAmount;
        @com.alibaba.excel.annotation.ExcelProperty("状态")
        private String status;
        @com.alibaba.excel.annotation.ExcelProperty("备注")
        private String remark;
    }
}