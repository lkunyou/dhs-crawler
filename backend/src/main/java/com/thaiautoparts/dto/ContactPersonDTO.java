package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class ContactPersonDTO {
    private Long id;
    private Long companyId;
    private String firstName;
    private String lastName;
    private String fullName;
    private String nameTh;
    private String jobTitle;
    private String department;
    private Boolean isDecisionMaker;
    private String seniorityLevel;
    private String email;
    private Boolean emailVerified;
    private String phone;
    private String whatsapp;
    private String linkedinUrl;
    private Integer contactCount;
    private Integer replyCount;
    private String notes;
}
