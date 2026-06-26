package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.entity.CmdtCode;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

public interface CmdtCodeMapper extends BaseMapper<CmdtCode> {

    @Select("SELECT * FROM p_cmdt_code WHERE cmdt_code LIKE CONCAT('%', #{keyword}, '%') " +
            "OR description_en LIKE CONCAT('%', #{keyword}, '%') " +
            "OR description_cn LIKE CONCAT('%', #{keyword}, '%')")
    IPage<CmdtCode> searchByKeyword(Page<CmdtCode> page, @Param("keyword") String keyword);

    @Select("SELECT DISTINCT section_code, section FROM p_cmdt_code ORDER BY section_code")
    java.util.List<CmdtCode> listSections();

    @Select("SELECT DISTINCT chapter_code, chapter FROM p_cmdt_code WHERE section_code = #{sectionCode} ORDER BY chapter_code")
    java.util.List<CmdtCode> listChaptersBySection(@Param("sectionCode") String sectionCode);
}