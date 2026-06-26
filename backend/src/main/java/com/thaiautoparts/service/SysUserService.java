package com.thaiautoparts.service;

import com.thaiautoparts.entity.SysUser;
import java.util.List;

public interface SysUserService {
    List<SysUser> listAll();
    SysUser getById(Long id);
    SysUser getByUsername(String username);
    SysUser createUser(SysUser user);
    SysUser updateUser(Long id, SysUser user);
    void deleteUser(Long id);
}
