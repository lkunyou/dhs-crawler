package com.thaiautoparts.controller;

import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.SysUser;
import com.thaiautoparts.service.SysUserService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/sys-users")
@RequiredArgsConstructor
public class SysUserController {

    private final SysUserService sysUserService;

    @GetMapping
    public Result<List<SysUser>> listAll() {
        return Result.success(sysUserService.listAll());
    }

    @GetMapping("/{id}")
    public Result<SysUser> getById(@PathVariable Long id) {
        return Result.success(sysUserService.getById(id));
    }

    @PostMapping
    public Result<SysUser> createUser(@RequestBody SysUser user) {
        return Result.success(sysUserService.createUser(user));
    }

    @PutMapping("/{id}")
    public Result<SysUser> updateUser(@PathVariable Long id, @RequestBody SysUser user) {
        return Result.success(sysUserService.updateUser(id, user));
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteUser(@PathVariable Long id) {
        sysUserService.deleteUser(id);
        return Result.success();
    }
}
