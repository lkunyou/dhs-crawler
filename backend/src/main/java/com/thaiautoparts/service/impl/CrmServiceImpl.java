package com.thaiautoparts.service.impl;

import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.FollowUpRecord;
import com.thaiautoparts.entity.Quotation;
import com.thaiautoparts.entity.Task;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.FollowUpRecordMapper;
import com.thaiautoparts.repository.QuotationMapper;
import com.thaiautoparts.repository.TaskMapper;
import com.thaiautoparts.service.CrmService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class CrmServiceImpl implements CrmService {

    private final FollowUpRecordMapper followUpRecordMapper;
    private final TaskMapper taskMapper;
    private final QuotationMapper quotationMapper;
    private final CompanyMapper companyMapper;

    @Override
    @Transactional
    public FollowUpRecord addFollowUp(FollowUpRecord record) {
        followUpRecordMapper.insert(record);
        
        // 更新公司最后联系时间
        Company company = companyMapper.selectById(record.getCompanyId());
        if (company != null) {
            company.setLastContactedAt(LocalDateTime.now());
            companyMapper.updateById(company);
        }
        
        return record;
    }

    @Override
    public List<FollowUpRecord> getFollowUpRecords(Long companyId) {
        return followUpRecordMapper.findByCompanyId(companyId);
    }

    @Override
    @Transactional
    public Task createTask(Task task) {
        if (task.getStatus() == null) {
            task.setStatus("Pending");
        }
        if (task.getPriority() == null) {
            task.setPriority("Medium");
        }
        taskMapper.insert(task);
        return task;
    }

    @Override
    @Transactional
    public Task updateTaskStatus(Long taskId, String status) {
        Task task = taskMapper.selectById(taskId);
        if (task == null) {
            throw new RuntimeException("Task not found: " + taskId);
        }
        task.setStatus(status);
        if ("Completed".equals(status)) {
            task.setCompletedAt(LocalDateTime.now());
        }
        taskMapper.updateById(task);
        return task;
    }

    @Override
    public List<Task> getPendingTasks(Long assignedTo) {
        return taskMapper.findPendingByAssignedTo(assignedTo);
    }

    @Override
    public List<Task> getCompanyTasks(Long companyId) {
        return taskMapper.findByCompanyId(companyId);
    }

    @Override
    @Transactional
    public Quotation createQuotation(Quotation quotation) {
        if (quotation.getStatus() == null) {
            quotation.setStatus("Draft");
        }
        if (quotation.getCurrency() == null) {
            quotation.setCurrency("USD");
        }
        
        // 生成报价单号
        String quotationNo = "QT-" + System.currentTimeMillis();
        quotation.setQuotationNo(quotationNo);
        
        quotationMapper.insert(quotation);
        
        // 更新公司状态
        Company company = companyMapper.selectById(quotation.getCompanyId());
        if (company != null) {
            company.setStatus("Quoted");
            companyMapper.updateById(company);
        }
        
        return quotation;
    }

    @Override
    @Transactional
    public Quotation updateQuotationStatus(Long quotationId, String status) {
        Quotation quotation = quotationMapper.selectById(quotationId);
        if (quotation == null) {
            throw new RuntimeException("Quotation not found: " + quotationId);
        }
        quotation.setStatus(status);
        
        if ("Sent".equals(status)) {
            quotation.setSentAt(LocalDateTime.now());
        } else if ("Accepted".equals(status)) {
            quotation.setAcceptedAt(LocalDateTime.now());
            Company company = companyMapper.selectById(quotation.getCompanyId());
            if (company != null) {
                company.setStatus("Won");
                companyMapper.updateById(company);
            }
        } else if ("Rejected".equals(status)) {
            Company company = companyMapper.selectById(quotation.getCompanyId());
            if (company != null) {
                company.setStatus("Lost");
                companyMapper.updateById(company);
            }
        }
        
        quotationMapper.updateById(quotation);
        return quotation;
    }

    @Override
    public List<Quotation> getCompanyQuotations(Long companyId) {
        LambdaQueryWrapper<Quotation> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Quotation::getCompanyId, companyId);
        wrapper.orderByDesc(Quotation::getCreatedAt);
        return quotationMapper.selectList(wrapper);
    }

    @Override
    @Transactional
    public void advanceCompanyStatus(Long companyId) {
        Company company = companyMapper.selectById(companyId);
        if (company == null) return;

        String currentStatus = company.getStatus();
        String nextStatus = switch (currentStatus) {
            case "New" -> "Contacted";
            case "Contacted" -> "Replied";
            case "Replied" -> "Quoted";
            case "Quoted" -> "Negotiation";
            case "Negotiation" -> "Sample_Sent";
            default -> null;
        };

        if (nextStatus != null) {
            company.setStatus(nextStatus);
            companyMapper.updateById(company);
            log.info("Company {} status advanced: {} -> {}", companyId, currentStatus, nextStatus);
        }
    }
}
