package com.thaiautoparts.service;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.service.IService;
import com.thaiautoparts.entity.CmdtCode;

import java.util.List;

public interface CmdtCodeService extends IService<CmdtCode> {

    IPage<CmdtCode> search(String keyword, Integer page, Integer size);

    List<CmdtCode> listSections();

    List<CmdtCode> listChaptersBySection(String sectionCode);

    IPage<CmdtCode> getBySection(String sectionCode, Integer page, Integer size);

    IPage<CmdtCode> getByChapter(String chapterCode, Integer page, Integer size);
}