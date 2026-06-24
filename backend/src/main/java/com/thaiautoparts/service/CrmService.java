package com.thaiautoparts.service;

import com.thaiautoparts.entity.FollowUpRecord;
import com.thaiautoparts.entity.Task;
import com.thaiautoparts.entity.Quotation;
import java.util.List;

public interface CrmService {
    // 跟进记录
    FollowUpRecord addFollowUp(FollowUpRecord record);
    List<FollowUpRecord> getFollowUpRecords(Long companyId);
    
    // 任务管理
    Task createTask(Task task);
    Task updateTaskStatus(Long taskId, String status);
    List<Task> getPendingTasks(Long assignedTo);
    List<Task> getCompanyTasks(Long companyId);
    
    // 报价管理
    Quotation createQuotation(Quotation quotation);
    Quotation updateQuotationStatus(Long quotationId, String status);
    List<Quotation> getCompanyQuotations(Long companyId);
    
    // 客户状态流转
    void advanceCompanyStatus(Long companyId);
}
