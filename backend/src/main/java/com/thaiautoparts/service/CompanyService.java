package com.thaiautoparts.service;

import com.thaiautoparts.dto.CompanyDTO;
import com.thaiautoparts.dto.PageResult;

import java.util.List;
import java.util.Map;

public interface CompanyService {
    PageResult<CompanyDTO> listCompanies(int page, int size, String keyword, String leadGrade, String status);
    CompanyDTO getCompanyById(Long id);
    CompanyDTO createCompany(CompanyDTO dto);
    CompanyDTO updateCompany(Long id, CompanyDTO dto);
    void deleteCompany(Long id);
    void updateLeadScore(Long companyId);
    List<Map<String, Object>> getLeadGradeStats();
    List<Map<String, Object>> getStatusStats();
    List<Map<String, Object>> getSourceStats();
    List<CompanyDTO> listAllCompanies();
    CompanyDTO findCompanyByEmail(String email);
}
