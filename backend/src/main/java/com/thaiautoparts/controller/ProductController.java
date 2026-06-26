package com.thaiautoparts.controller;

import com.alibaba.excel.EasyExcel;
import com.alibaba.excel.context.AnalysisContext;
import com.alibaba.excel.read.listener.ReadListener;
import com.thaiautoparts.dto.PageResult;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.Product;
import com.thaiautoparts.service.ProductService;
import com.thaiautoparts.service.SystemConfigService;
import jakarta.servlet.http.HttpServletResponse;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.math.BigDecimal;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

@RestController
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService productService;
    private final SystemConfigService systemConfigService;

    private final ConcurrentHashMap<String, List<Product>> tempProductStore = new ConcurrentHashMap<>();

    @GetMapping
    public Result<PageResult<Product>> listProducts(
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) String productName,
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String brand,
            @RequestParam(required = false) String carModel,
            @RequestParam(required = false) String productCode) {
        PageResult<Product> result = productService.listProducts(page, size, productName, category, status, brand, carModel, productCode);
        return Result.success(result);
    }

    @GetMapping("/{id}")
    public Result<Product> getProduct(@PathVariable Long id) {
        Product product = productService.getProductById(id);
        return Result.success(product);
    }

    @PostMapping
    public Result<Product> createProduct(@RequestBody Product product) {
        Product created = productService.createProduct(product);
        return Result.success(created);
    }

    @PutMapping("/{id}")
    public Result<Product> updateProduct(@PathVariable Long id, @RequestBody Product product) {
        Product updated = productService.updateProduct(id, product);
        return Result.success(updated);
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return Result.success();
    }

    @GetMapping("/export")
    public void exportProducts(HttpServletResponse response) throws IOException {
        response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
        response.setCharacterEncoding("utf-8");
        String fileName = URLEncoder.encode("产品列表", StandardCharsets.UTF_8).replaceAll("\\+", "%20");
        response.setHeader("Content-disposition", "attachment;filename*=utf-8''" + fileName + ".xlsx");

        List<Product> list = productService.listAll();
        List<ProductExcel> excelList = new ArrayList<>();
        for (Product p : list) {
            ProductExcel e = new ProductExcel();
            e.setProductName(p.getProductName());
            e.setProductCode(p.getProductCode());
            e.setCategory(p.getCategory());
            e.setBrand(p.getBrand());
            e.setModel(p.getModel());
            e.setCarModel(p.getCarModel());
            e.setSpecification(p.getSpecification());
            e.setUnitPrice(p.getUnitPrice());
            e.setStock(p.getStock());
            e.setWeight(p.getWeight());
            e.setQtyPerPkg(p.getQtyPerPkg());
            e.setPkgLength(p.getPkgLength());
            e.setPkgWidth(p.getPkgWidth());
            e.setPkgHeight(p.getPkgHeight());
            e.setStatus(p.getStatus());
            e.setDescription(p.getDescription());
            excelList.add(e);
        }
        EasyExcel.write(response.getOutputStream(), ProductExcel.class).sheet("产品").doWrite(excelList);
    }

    @PostMapping("/import-preview")
    public Result<Map<String, Object>> importProductsPreview(@RequestParam("file") MultipartFile file) throws IOException {
        List<Product> list = new ArrayList<>();
        EasyExcel.read(file.getInputStream(), ProductExcel.class, new ReadListener<ProductExcel>() {
            @Override
            public void invoke(ProductExcel data, AnalysisContext context) {
                Product p = new Product();
                p.setProductName(data.getProductName());
                p.setProductCode(data.getProductCode());
                p.setCategory(data.getCategory());
                p.setBrand(data.getBrand());
                p.setModel(data.getModel());
                p.setCarModel(data.getCarModel());
                p.setSpecification(data.getSpecification());
                p.setUnitPrice(data.getUnitPrice());
                p.setStock(data.getStock());
                p.setWeight(data.getWeight());
                p.setQtyPerPkg(data.getQtyPerPkg());
                p.setPkgLength(data.getPkgLength());
                p.setPkgWidth(data.getPkgWidth());
                p.setPkgHeight(data.getPkgHeight());
                p.setStatus(data.getStatus());
                p.setDescription(data.getDescription());
                list.add(p);
            }
            @Override
            public void doAfterAllAnalysed(AnalysisContext context) {}
        }).sheet().doRead();

        String tempId = UUID.randomUUID().toString();
        tempProductStore.put(tempId, list);

        Map<String, Object> result = new HashMap<>();
        result.put("tempId", tempId);
        result.put("total", list.size());
        result.put("list", list);
        return Result.success(result);
    }

    @PostMapping("/import-confirm")
    public Result<Void> importProductsConfirm(@RequestParam("tempId") String tempId) {
        List<Product> list = tempProductStore.remove(tempId);
        if (list == null || list.isEmpty()) {
            return Result.error("预览数据已过期或不存在，请重新上传");
        }
        productService.saveBatch(list);
        return Result.success();
    }

    @PostMapping("/import-cancel")
    public Result<Void> importProductsCancel(@RequestParam("tempId") String tempId) {
        tempProductStore.remove(tempId);
        return Result.success();
    }

    @PostMapping("/upload-image")
    public Result<String> uploadImage(@RequestParam("file") MultipartFile file) throws IOException {
        if (file.isEmpty()) {
            return Result.error("请选择图片文件");
        }
        String contentType = file.getContentType();
        if (contentType == null || !contentType.startsWith("image/")) {
            return Result.error("只支持上传图片文件");
        }
        String originalFilename = file.getOriginalFilename();
        String ext = "";
        if (originalFilename != null && originalFilename.contains(".")) {
            ext = originalFilename.substring(originalFilename.lastIndexOf("."));
        }
        String newFileName = UUID.randomUUID().toString() + ext;
        // 从配置表获取上传基础路径
        String uploadBasePath = systemConfigService.getValue("upload_base_path", "./uploads");
        java.nio.file.Path uploadDir = java.nio.file.Paths.get(uploadBasePath, "products");
        java.nio.file.Files.createDirectories(uploadDir);
        java.nio.file.Path filePath = uploadDir.resolve(newFileName);
        java.nio.file.Files.copy(file.getInputStream(), filePath);
        String imageUrl = "/uploads/products/" + newFileName;
        return Result.success(imageUrl);
    }

    @Data
    public static class ProductExcel {
        @com.alibaba.excel.annotation.ExcelProperty("产品名称")
        private String productName;
        @com.alibaba.excel.annotation.ExcelProperty("产品编码")
        private String productCode;
        @com.alibaba.excel.annotation.ExcelProperty("分类")
        private String category;
        @com.alibaba.excel.annotation.ExcelProperty("品牌")
        private String brand;
        @com.alibaba.excel.annotation.ExcelProperty("型号")
        private String model;
        @com.alibaba.excel.annotation.ExcelProperty("适用车型")
        private String carModel;
        @com.alibaba.excel.annotation.ExcelProperty("规格")
        private String specification;
        @com.alibaba.excel.annotation.ExcelProperty("单价")
        private BigDecimal unitPrice;
        @com.alibaba.excel.annotation.ExcelProperty("库存")
        private Integer stock;
        @com.alibaba.excel.annotation.ExcelProperty("重量")
        private BigDecimal weight;
        @com.alibaba.excel.annotation.ExcelProperty("每箱数量")
        private Integer qtyPerPkg;
        @com.alibaba.excel.annotation.ExcelProperty("包装长")
        private Integer pkgLength;
        @com.alibaba.excel.annotation.ExcelProperty("包装宽")
        private Integer pkgWidth;
        @com.alibaba.excel.annotation.ExcelProperty("包装高")
        private Integer pkgHeight;
        @com.alibaba.excel.annotation.ExcelProperty("状态")
        private String status;
        @com.alibaba.excel.annotation.ExcelProperty("描述")
        private String description;
    }
}