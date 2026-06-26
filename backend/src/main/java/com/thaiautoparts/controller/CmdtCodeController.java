package com.thaiautoparts.controller;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.CmdtCode;
import com.thaiautoparts.service.CmdtCodeService;
import jakarta.annotation.Resource;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cmdt")
public class CmdtCodeController {

    @Resource
    private CmdtCodeService cmdtCodeService;

    @GetMapping("/search")
    public Result<IPage<CmdtCode>> search(
            @RequestParam(required = false) String keyword,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "20") Integer size) {
        IPage<CmdtCode> result = cmdtCodeService.search(keyword, page, size);
        return Result.success(result);
    }

    @GetMapping("/sections")
    public Result<List<CmdtCode>> listSections() {
        List<CmdtCode> result = cmdtCodeService.listSections();
        return Result.success(result);
    }

    @GetMapping("/chapters")
    public Result<List<CmdtCode>> listChaptersBySection(@RequestParam String sectionCode) {
        List<CmdtCode> result = cmdtCodeService.listChaptersBySection(sectionCode);
        return Result.success(result);
    }

    @GetMapping("/section/{sectionCode}")
    public Result<IPage<CmdtCode>> getBySection(
            @PathVariable String sectionCode,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "20") Integer size) {
        IPage<CmdtCode> result = cmdtCodeService.getBySection(sectionCode, page, size);
        return Result.success(result);
    }

    @GetMapping("/chapter/{chapterCode}")
    public Result<IPage<CmdtCode>> getByChapter(
            @PathVariable String chapterCode,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "20") Integer size) {
        IPage<CmdtCode> result = cmdtCodeService.getByChapter(chapterCode, page, size);
        return Result.success(result);
    }

    @GetMapping("/{id}")
    public Result<CmdtCode> getById(@PathVariable Long id) {
        CmdtCode result = cmdtCodeService.getById(id);
        return Result.success(result);
    }
}