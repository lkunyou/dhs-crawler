package com.thaiautoparts.controller;

import com.alibaba.excel.EasyExcel;
import com.alibaba.excel.context.AnalysisContext;
import com.alibaba.excel.read.listener.ReadListener;
import com.thaiautoparts.dto.CompanyDTO;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.CompanyService;
import jakarta.servlet.http.HttpServletResponse;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequestMapping("/companies")
@RequiredArgsConstructor
public class CompanyController {

    private final CompanyService companyService;

    private final ConcurrentHashMap<String, List<CompanyDTO>> tempCompanyStore = new ConcurrentHashMap<>();

    @GetMapping
    public Result<PageResult<CompanyDTO>> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String companyName,
            @RequestParam(required = false) String website,
            @RequestParam(required = false) String email,
            @RequestParam(required = false) String whatsapp,
            @RequestParam(required = false) String leadGrade,
            @RequestParam(required = false) String status) {
        return Result.success(companyService.listCompanies(page, size, companyName, website, email, whatsapp, leadGrade, status));
    }

    @GetMapping("/{id}")
    public Result<CompanyDTO> getById(@PathVariable Long id) {
        return Result.success(companyService.getCompanyById(id));
    }

    @GetMapping("/find-by-email")
    public Result<CompanyDTO> findByEmail(@RequestParam String email) {
        return Result.success(companyService.findCompanyByEmail(email));
    }

    @PostMapping
    public Result<CompanyDTO> create(@RequestBody CompanyDTO dto) {
        return Result.success(companyService.createCompany(dto));
    }

    @PutMapping("/{id}")
    public Result<CompanyDTO> update(@PathVariable Long id, @RequestBody CompanyDTO dto) {
        return Result.success(companyService.updateCompany(id, dto));
    }

    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) {
        companyService.deleteCompany(id);
        return Result.success();
    }

    @PostMapping("/{id}/score")
    public Result<Void> updateScore(@PathVariable Long id) {
        companyService.updateLeadScore(id);
        return Result.success();
    }

    @GetMapping("/stats/grade")
    public Result<List<Map<String, Object>>> getGradeStats() {
        return Result.success(companyService.getLeadGradeStats());
    }

    @GetMapping("/stats/status")
    public Result<List<Map<String, Object>>> getStatusStats() {
        return Result.success(companyService.getStatusStats());
    }

    @GetMapping("/stats/source")
    public Result<List<Map<String, Object>>> getSourceStats() {
        return Result.success(companyService.getSourceStats());
    }

    @GetMapping("/export")
    public void exportCompanies(HttpServletResponse response) throws IOException {
        response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        response.setCharacterEncoding("utf-8");
        String fileName = URLEncoder.encode("客户列表", StandardCharsets.UTF_8).replaceAll("\\+", "%20");
        response.setHeader("Content-disposition", "attachment;filename*=utf-8''" + fileName + ".xlsx");

        List<CompanyDTO> list = companyService.listAllCompanies();
        List<CompanyExcel> excelList = new ArrayList<>();
        for (CompanyDTO c : list) {
            CompanyExcel e = new CompanyExcel();
            e.setCompanyName(c.getCompanyName());
            e.setCompanyNameEn(c.getCompanyNameEn());
            e.setCountry(c.getCountry());
            e.setCity(c.getCity());
            e.setWebsite(c.getWebsite());
            e.setEmail(c.getEmail());
            e.setPhone(c.getPhone());
            e.setWhatsapp(c.getWhatsapp());
            e.setAddress(c.getAddress());
            e.setCompanyType(c.getCompanyType());
            e.setLeadGrade(c.getLeadGrade());
            e.setStatus(c.getStatus());
            excelList.add(e);
        }
        EasyExcel.write(response.getOutputStream(), CompanyExcel.class).sheet("客户").doWrite(excelList);
    }

    @PostMapping("/import-preview")
    public Result<Map<String, Object>> importCompaniesPreview(@RequestParam("file") MultipartFile file) throws IOException {
        List<CompanyDTO> list = new ArrayList<>();
        EasyExcel.read(file.getInputStream(), CompanyExcel.class, new ReadListener<CompanyExcel>() {
            @Override
            public void invoke(CompanyExcel data, AnalysisContext context) {
                CompanyDTO c = new CompanyDTO();
                c.setCompanyName(data.getCompanyName());
                c.setCompanyNameEn(data.getCompanyNameEn());
                c.setCountry(data.getCountry());
                c.setCity(data.getCity());
                c.setWebsite(data.getWebsite());
                c.setEmail(data.getEmail());
                c.setPhone(data.getPhone());
                c.setWhatsapp(data.getWhatsapp());
                c.setAddress(data.getAddress());
                c.setCompanyType(data.getCompanyType());
                c.setLeadGrade(data.getLeadGrade());
                c.setStatus(data.getStatus());
                list.add(c);
            }
            @Override
            public void doAfterAllAnalysed(AnalysisContext context) {}
        }).sheet().doRead();

        String tempId = UUID.randomUUID().toString();
        tempCompanyStore.put(tempId, list);

        Map<String, Object> result = new HashMap<>();
        result.put("tempId", tempId);
        result.put("total", list.size());
        result.put("list", list);
        return Result.success(result);
    }

    @PostMapping("/import-confirm")
    public Result<Void> importCompaniesConfirm(@RequestParam("tempId") String tempId) {
        List<CompanyDTO> list = tempCompanyStore.remove(tempId);
        if (list == null || list.isEmpty()) {
            return Result.error("预览数据已过期或不存在，请重新上传");
        }
        for (CompanyDTO c : list) {
            companyService.createCompany(c);
        }
        return Result.success();
    }

    @PostMapping("/import-cancel")
    public Result<Void> importCompaniesCancel(@RequestParam("tempId") String tempId) {
        tempCompanyStore.remove(tempId);
        return Result.success();
    }

    @Data
    public static class CompanyExcel {
        @com.alibaba.excel.annotation.ExcelProperty("公司名称")
        private String companyName;
        @com.alibaba.excel.annotation.ExcelProperty("英文名称")
        private String companyNameEn;
        @com.alibaba.excel.annotation.ExcelProperty("国家")
        private String country;
        @com.alibaba.excel.annotation.ExcelProperty("城市")
        private String city;
        @com.alibaba.excel.annotation.ExcelProperty("网站")
        private String website;
        @com.alibaba.excel.annotation.ExcelProperty("邮箱")
        private String email;
        @com.alibaba.excel.annotation.ExcelProperty("电话")
        private String phone;
        @com.alibaba.excel.annotation.ExcelProperty("WhatsApp")
        private String whatsapp;
        @com.alibaba.excel.annotation.ExcelProperty("地址")
        private String address;
        @com.alibaba.excel.annotation.ExcelProperty("类型")
        private String companyType;
        @com.alibaba.excel.annotation.ExcelProperty("等级")
        private String leadGrade;
        @com.alibaba.excel.annotation.ExcelProperty("状态")
        private String status;
    }
}
