package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.SysUser;
import com.thaiautoparts.repository.SysUserMapper;
import com.thaiautoparts.service.SysUserService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class SysUserServiceImpl implements SysUserService {

    private final SysUserMapper sysUserMapper;

    @Override
    public List<SysUser> listAll() {
        return sysUserMapper.selectList(new LambdaQueryWrapper<SysUser>().orderByDesc(SysUser::getCreatedAt));
    }

    @Override
    public SysUser getById(Long id) {
        return sysUserMapper.selectById(id);
    }

    @Override
    public SysUser getByUsername(String username) {
        return sysUserMapper.selectOne(
            new LambdaQueryWrapper<SysUser>().eq(SysUser::getUsername, username)
        );
    }

    @Override
    @Transactional
    public SysUser createUser(SysUser user) {
        user.setCreatedAt(LocalDateTime.now());
        user.setUpdatedAt(LocalDateTime.now());
        if (user.getStatus() == null) {
            user.setStatus("active");
        }
        sysUserMapper.insert(user);
        return user;
    }

    @Override
    @Transactional
    public SysUser updateUser(Long id, SysUser user) {
        SysUser existing = sysUserMapper.selectById(id);
        if (existing == null) {
            throw new RuntimeException("用户不存在: " + id);
        }
        user.setId(id);
        user.setUpdatedAt(LocalDateTime.now());
        sysUserMapper.updateById(user);
        return sysUserMapper.selectById(id);
    }

    @Override
    @Transactional
    public void deleteUser(Long id) {
        sysUserMapper.deleteById(id);
    }
}
