package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.ContactPerson;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface ContactPersonMapper extends BaseMapper<ContactPerson> {
    
    @Select("SELECT * FROM p_contact_person WHERE company_id = #{companyId}")
    List<ContactPerson> findByCompanyId(@Param("companyId") Long companyId);
    
    @Select("SELECT * FROM p_contact_person WHERE email = #{email} LIMIT 1")
    ContactPerson findByEmail(@Param("email") String email);
}
