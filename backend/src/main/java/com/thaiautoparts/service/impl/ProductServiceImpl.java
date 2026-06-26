package com.thaiautoparts.service.impl;

import cn.hutool.core.bean.BeanUtil;
import cn.hutool.core.util.StrUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.entity.Product;
import com.thaiautoparts.repository.ProductMapper;
import com.thaiautoparts.service.ProductService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class ProductServiceImpl implements ProductService {

    private final ProductMapper productMapper;

    @Override
    public PageResult<Product> listProducts(int page, int size, String productName, String category, String status, String brand, String carModel, String productCode) {
        LambdaQueryWrapper<Product> wrapper = new LambdaQueryWrapper<>();

        if (StrUtil.isNotBlank(productName) && StrUtil.isNotBlank(productCode)) {
            wrapper.and(w -> w.like(Product::getProductName, productName).or().like(Product::getProductCode, productCode));
        } else if (StrUtil.isNotBlank(productName)) {
            wrapper.like(Product::getProductName, productName);
        } else if (StrUtil.isNotBlank(productCode)) {
            wrapper.like(Product::getProductCode, productCode);
        }
        if (StrUtil.isNotBlank(category)) {
            wrapper.eq(Product::getCategory, category);
        }
        if (StrUtil.isNotBlank(status)) {
            wrapper.eq(Product::getStatus, status);
        }
        if (StrUtil.isNotBlank(brand)) {
            wrapper.like(Product::getBrand, brand);
        }
        if (StrUtil.isNotBlank(carModel)) {
            wrapper.like(Product::getCarModel, carModel);
        }
        
        wrapper.orderByDesc(Product::getCreatedAt);

        Page<Product> pageParam = new Page<>(page, size);
        Page<Product> result = productMapper.selectPage(pageParam, wrapper);

        return new PageResult<>(result.getTotal(), page, size, result.getRecords());
    }

    @Override
    public Product getProductById(Long id) {
        Product product = productMapper.selectById(id);
        if (product == null) {
            throw new RuntimeException("Product not found: " + id);
        }
        return product;
    }

    @Override
    @Transactional
    public Product createProduct(Product product) {
        if (product.getStatus() == null) {
            product.setStatus("active");
        }
        
        productMapper.insert(product);
        return product;
    }

    @Override
    @Transactional
    public Product updateProduct(Long id, Product product) {
        Product existing = productMapper.selectById(id);
        if (existing == null) {
            throw new RuntimeException("Product not found: " + id);
        }

        BeanUtil.copyProperties(product, existing, "id", "createdAt");
        productMapper.updateById(existing);
        
        return existing;
    }

    @Override
    @Transactional
    public void deleteProduct(Long id) {
        productMapper.deleteById(id);
    }

    @Override
    public List<Product> listAll() {
        return productMapper.selectList(new LambdaQueryWrapper<Product>().orderByDesc(Product::getCreatedAt));
    }

    @Override
    public void saveBatch(List<Product> list) {
        for (Product p : list) {
            if (p.getStatus() == null) {
                p.setStatus("active");
            }
            productMapper.insert(p);
        }
    }

    @Override
    public List<Product> searchProducts(String keyword, int limit) {
        LambdaQueryWrapper<Product> wrapper = new LambdaQueryWrapper<>();
        if (StrUtil.isNotBlank(keyword)) {
            wrapper.and(w -> w.like(Product::getProductName, keyword).or().like(Product::getProductCode, keyword));
        }
        wrapper.orderByDesc(Product::getCreatedAt);
        wrapper.last("LIMIT " + limit);
        return productMapper.selectList(wrapper);
    }
}