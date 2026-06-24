package com.thaiautoparts.controller;

import com.thaiautoparts.dto.LoginRequest;
import com.thaiautoparts.dto.LoginResponse;
import com.thaiautoparts.dto.Result;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;
import java.util.concurrent.TimeUnit;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final StringRedisTemplate redisTemplate;

    @Value("${spring.security.user.name:admin}")
    private String defaultUsername;

    @Value("${spring.security.user.password:password}")
    private String defaultPassword;

    public AuthController(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @PostMapping("/login")
    public Result<LoginResponse> login(@RequestBody LoginRequest request) {
        if (defaultUsername.equals(request.getUsername()) && 
            defaultPassword.equals(request.getPassword())) {
            String token = UUID.randomUUID().toString();
            redisTemplate.opsForValue().set("token:" + token, request.getUsername(), 24, TimeUnit.HOURS);
            return Result.success(new LoginResponse(token, request.getUsername()));
        }
        return Result.error(401, "用户名或密码错误");
    }

    @PostMapping("/logout")
    public Result<String> logout(@RequestHeader("Authorization") String authHeader) {
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            redisTemplate.delete("token:" + token);
        }
        return Result.success("退出成功");
    }

    @GetMapping("/check")
    public Result<String> checkAuth() {
        return Result.success("已登录");
    }
}