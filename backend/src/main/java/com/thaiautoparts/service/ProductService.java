package com.thaiautoparts.service;

import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.entity.Product;

public interface ProductService {
    PageResult<Product> listProducts(int page, int size, String productName, String category, String status, String brand, String carModel, String productCode);
    Product getProductById(Long id);
    Product createProduct(Product product);
    Product updateProduct(Long id, Product product);
    void deleteProduct(Long id);
    java.util.List<Product> listAll();
    void saveBatch(java.util.List<Product> list);
    java.util.List<Product> searchProducts(String keyword, int limit);
}