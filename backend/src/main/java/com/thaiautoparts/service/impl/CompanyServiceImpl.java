package com.thaiautoparts.service.impl;

import cn.hutool.core.bean.BeanUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.dto.CompanyDTO;
import com.thaiautoparts.dto.ContactPersonDTO;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.ContactPerson;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.ContactPersonMapper;
import com.thaiautoparts.repository.EmailRecordMapper;
import com.thaiautoparts.repository.WhatsappRecordMapper;
import com.thaiautoparts.repository.QuotationMapper;
import com.thaiautoparts.service.CompanyService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class CompanyServiceImpl implements CompanyService {

    private final CompanyMapper companyMapper;
    private final ContactPersonMapper contactPersonMapper;
    private final EmailRecordMapper emailRecordMapper;
    private final WhatsappRecordMapper whatsappRecordMapper;
    private final QuotationMapper quotationMapper;

    @Override
    public PageResult<CompanyDTO> listCompanies(int page, int size, String keyword, String leadGrade, String status) {
        LambdaQueryWrapper<Company> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Company::getIsDuplicate, false);
        
        if (StrUtil.isNotBlank(keyword)) {
            wrapper.like(Company::getCompanyName, keyword)
                   .or()
                   .like(Company::getWebsite, keyword);
        }
        if (StrUtil.isNotBlank(leadGrade)) {
            wrapper.eq(Company::getLeadGrade, leadGrade);
        }
        if (StrUtil.isNotBlank(status)) {
            wrapper.eq(Company::getStatus, status);
        }
        wrapper.orderByDesc(Company::getCreatedAt);

        Page<Company> pageParam = new Page<>(page, size);
        Page<Company> result = companyMapper.selectPage(pageParam, wrapper);

        List<CompanyDTO> dtoList = result.getRecords().stream()
                .map(this::convertToDTO)
                .collect(Collectors.toList());

        List<Long> companyIds = dtoList.stream().map(CompanyDTO::getId).collect(Collectors.toList());
        if (!companyIds.isEmpty()) {
            Map<Long, Integer> emailCountMap = emailRecordMapper.countByCompanyIds(companyIds).stream()
                    .collect(Collectors.toMap(m -> (Long) m.get("companyId"), m -> ((Number) m.get("cnt")).intValue()));
            Map<Long, Integer> whatsappCountMap = whatsappRecordMapper.countByCompanyIds(companyIds).stream()
                    .collect(Collectors.toMap(m -> (Long) m.get("companyId"), m -> ((Number) m.get("cnt")).intValue()));
            Map<Long, Integer> quoteCountMap = quotationMapper.countByCompanyIds(companyIds).stream()
                    .collect(Collectors.toMap(m -> (Long) m.get("companyId"), m -> ((Number) m.get("cnt")).intValue()));

            for (CompanyDTO dto : dtoList) {
                Long companyId = dto.getId();
                dto.setEmailCount(emailCountMap.getOrDefault(companyId, 0));
                dto.setWhatsappCount(whatsappCountMap.getOrDefault(companyId, 0));
                dto.setQuoteCount(quoteCountMap.getOrDefault(companyId, 0));
            }
        }

        return new PageResult<>(result.getTotal(), page, size, dtoList);
    }

    @Override
    public CompanyDTO getCompanyById(Long id) {
        Company company = companyMapper.selectById(id);
        if (company == null) {
            throw new RuntimeException("Company not found: " + id);
        }
        return convertToDTO(company);
    }

    @Override
    @Transactional
    public CompanyDTO createCompany(CompanyDTO dto) {
        Company company = new Company();
        BeanUtil.copyProperties(dto, company);
        
        if (company.getLeadScore() == null) {
            company.setLeadScore(0);
        }
        if (company.getLeadGrade() == null) {
            company.setLeadGrade("C");
        }
        if (company.getStatus() == null) {
            company.setStatus("New");
        }
        if (company.getCountry() == null) {
            company.setCountry("Thailand");
        }
        
        companyMapper.insert(company);
        return getCompanyById(company.getId());
    }

    @Override
    @Transactional
    public CompanyDTO updateCompany(Long id, CompanyDTO dto) {
        Company company = companyMapper.selectById(id);
        if (company == null) {
            throw new RuntimeException("Company not found: " + id);
        }
        
        BeanUtil.copyProperties(dto, company, "id", "createdAt");
        company.setId(id);
        companyMapper.updateById(company);
        
        return getCompanyById(id);
    }

    @Override
    @Transactional
    public void deleteCompany(Long id) {
        companyMapper.deleteById(id);
    }

    @Override
    @Transactional
    public void updateLeadScore(Long companyId) {
        Company company = companyMapper.selectById(companyId);
        if (company == null) return;

        int score = 0;
        
        if (Boolean.TRUE.equals(company.getIsAutoPartsCore())) score += 20;
        if (Boolean.TRUE.equals(company.getIsImporterDistributor())) score += 20;
        if (company.getEmployeeCount() != null) score += 15;
        if (Boolean.TRUE.equals(company.getHasOemCooperation())) score += 15;
        if (company.getWebsiteCompleteness() != null) score += (company.getWebsiteCompleteness() / 10);
        
        String grade;
        if (score >= 80) grade = "S";
        else if (score >= 60) grade = "A";
        else if (score >= 40) grade = "B";
        else grade = "C";

        company.setLeadScore(score);
        company.setLeadGrade(grade);
        companyMapper.updateById(company);
    }

    @Override
    public List<Map<String, Object>> getLeadGradeStats() {
        return companyMapper.countByLeadGrade();
    }

    @Override
    public List<Map<String, Object>> getStatusStats() {
        return companyMapper.countByStatus();
    }

    @Override
    public List<Map<String, Object>> getSourceStats() {
        return companyMapper.countBySource();
    }

    @Override
    public List<CompanyDTO> listAllCompanies() {
        List<Company> list = companyMapper.selectList(new LambdaQueryWrapper<Company>().orderByDesc(Company::getCreatedAt));
        return list.stream().map(this::convertToDTO).collect(Collectors.toList());
    }

    private CompanyDTO convertToDTO(Company company) {
        CompanyDTO dto = BeanUtil.copyProperties(company, CompanyDTO.class);
        
        List<ContactPerson> contacts = contactPersonMapper.findByCompanyId(company.getId());
        List<ContactPersonDTO> contactDTOs = contacts.stream()
                .map(c -> BeanUtil.copyProperties(c, ContactPersonDTO.class))
                .collect(Collectors.toList());
        dto.setContacts(contactDTOs);
        
        return dto;
    }
}
