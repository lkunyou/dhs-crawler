package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.FollowUpRecord;
import com.thaiautoparts.entity.Quotation;
import com.thaiautoparts.entity.Task;
import com.thaiautoparts.service.CrmService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/crm")
@RequiredArgsConstructor
public class CrmController {

    private final CrmService crmService;

    // 跟进记录
    @PostMapping("/follow-up")
    public Result<FollowUpRecord> addFollowUp(@RequestBody FollowUpRecord record) {
        return Result.success(crmService.addFollowUp(record));
    }

    @GetMapping("/follow-up/{companyId}")
    public Result<List<FollowUpRecord>> getFollowUpRecords(@PathVariable Long companyId) {
        return Result.success(crmService.getFollowUpRecords(companyId));
    }

    // 任务管理
    @PostMapping("/task")
    public Result<Task> createTask(@RequestBody Task task) {
        return Result.success(crmService.createTask(task));
    }

    @PutMapping("/task/{taskId}/status")
    public Result<Task> updateTaskStatus(@PathVariable Long taskId, @RequestParam String status) {
        return Result.success(crmService.updateTaskStatus(taskId, status));
    }

    @GetMapping("/task/pending")
    public Result<List<Task>> getPendingTasks(@RequestParam Long assignedTo) {
        return Result.success(crmService.getPendingTasks(assignedTo));
    }

    @GetMapping("/task/company/{companyId}")
    public Result<List<Task>> getCompanyTasks(@PathVariable Long companyId) {
        return Result.success(crmService.getCompanyTasks(companyId));
    }

    // 报价管理
    @PostMapping("/quotation")
    public Result<Quotation> createQuotation(@RequestBody Quotation quotation) {
        return Result.success(crmService.createQuotation(quotation));
    }

    @PutMapping("/quotation/{quotationId}/status")
    public Result<Quotation> updateQuotationStatus(@PathVariable Long quotationId, @RequestParam String status) {
        return Result.success(crmService.updateQuotationStatus(quotationId, status));
    }

    @GetMapping("/quotation/company/{companyId}")
    public Result<List<Quotation>> getCompanyQuotations(@PathVariable Long companyId) {
        return Result.success(crmService.getCompanyQuotations(companyId));
    }

    // 客户状态推进
    @PostMapping("/company/{companyId}/advance-status")
    public Result<Void> advanceCompanyStatus(@PathVariable Long companyId) {
        crmService.advanceCompanyStatus(companyId);
        return Result.success();
    }
}
