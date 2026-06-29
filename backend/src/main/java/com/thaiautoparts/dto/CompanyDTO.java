package com.thaiautoparts.dto;

import lombok.Data;
import java.util.List;

@Data
public class CompanyDTO {
    private Long id;
    private String companyName;
    private String companyNameTh;
    private String companyNameEn;
    private String country;
    private String companyType;
    private String website;
    private String address;
    private String city;
    private String province;
    private String phone;
    private String whatsapp;
    private String email;
    private Integer leadScore;
    private String leadGrade;
    private Boolean isAutoPartsCore;
    private Boolean isImporterDistributor;
    private Boolean hasOemCooperation;
    private String employeeCount;
    private String source;
    private String status;
    private List<ContactPersonDTO> contacts;

    private Integer emailCount;
    private Integer whatsappCount;
    private Integer quoteCount;
    
    private String emailSubject;
    private String developmentEmailTemplate;
    private String description;
}
