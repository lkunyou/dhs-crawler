package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.thaiautoparts.entity.CmdtCode;
import com.thaiautoparts.repository.CmdtCodeMapper;
import com.thaiautoparts.service.CmdtCodeService;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CmdtCodeServiceImpl extends ServiceImpl<CmdtCodeMapper, CmdtCode> implements CmdtCodeService {

    @Override
    public IPage<CmdtCode> search(String keyword, Integer page, Integer size) {
        Page<CmdtCode> pageParam = new Page<>(page, size);
        if (keyword == null || keyword.trim().isEmpty()) {
            return baseMapper.selectPage(pageParam, null);
        }
        return baseMapper.searchByKeyword(pageParam, keyword.trim());
    }

    @Override
    public List<CmdtCode> listSections() {
        return baseMapper.listSections();
    }

    @Override
    public List<CmdtCode> listChaptersBySection(String sectionCode) {
        return baseMapper.listChaptersBySection(sectionCode);
    }

    @Override
    public IPage<CmdtCode> getBySection(String sectionCode, Integer page, Integer size) {
        Page<CmdtCode> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<CmdtCode> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(CmdtCode::getSectionCode, sectionCode);
        return baseMapper.selectPage(pageParam, wrapper);
    }

    @Override
    public IPage<CmdtCode> getByChapter(String chapterCode, Integer page, Integer size) {
        Page<CmdtCode> pageParam = new Page<>(page, size);
        LambdaQueryWrapper<CmdtCode> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(CmdtCode::getChapterCode, chapterCode);
        return baseMapper.selectPage(pageParam, wrapper);
    }
}