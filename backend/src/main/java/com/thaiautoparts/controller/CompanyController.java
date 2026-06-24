package com.thaiautoparts.controller;

import com.thaiautoparts.dto.CompanyDTO;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.CompanyService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/companies")
@RequiredArgsConstructor
public class CompanyController {

    private final CompanyService companyService;

    @GetMapping
    public Result<PageResult<CompanyDTO>> list(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String keyword,
            @RequestParam(required = false) String leadGrade,
            @RequestParam(required = false) String status) {
        return Result.success(companyService.listCompanies(page, size, keyword, leadGrade, status));
    }

    @GetMapping("/{id}")
    public Result<CompanyDTO> getById(@PathVariable Long id) {
        return Result.success(companyService.getCompanyById(id));
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
}
