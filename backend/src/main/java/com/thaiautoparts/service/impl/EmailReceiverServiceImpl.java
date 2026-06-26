package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.InboundEmail;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.InboundEmailMapper;
import com.thaiautoparts.service.EmailReceiverService;
import com.thaiautoparts.service.SystemConfigService;
import jakarta.mail.*;
import jakarta.mail.internet.InternetAddress;
import jakarta.mail.internet.MimeMessage;
import jakarta.mail.search.FlagTerm;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.Properties;

@Slf4j
@Service
@RequiredArgsConstructor
public class EmailReceiverServiceImpl implements EmailReceiverService {

    private final InboundEmailMapper inboundEmailMapper;
    private final CompanyMapper companyMapper;
    private final SystemConfigService systemConfigService;

    @Value("${spring.mail.host-imap:}")
    private String mailHostImapYml;

    @Value("${spring.mail.port-imap:993}")
    private int mailPortImapYml;

    @Value("${spring.mail.username:}")
    private String mailUsernameYml;

    @Value("${spring.mail.password:}")
    private String mailPasswordYml;

    private String getMailConfig(String key, String defaultValue) {
        return systemConfigService.getValue(key, defaultValue);
    }

    private Session createSession() {
        String mailHostImap = getMailConfig("mail.host-imap", mailHostImapYml);
        int mailPortImap = Integer.parseInt(getMailConfig("mail.port-imap", String.valueOf(mailPortImapYml)));
        String mailUsername = getMailConfig("mail.username", mailUsernameYml);
        String mailPassword = getMailConfig("mail.password", mailPasswordYml);

        Properties props = new Properties();
        props.setProperty("mail.store.protocol", "imap");
        props.setProperty("mail.imap.host", mailHostImap);
        props.setProperty("mail.imap.port", String.valueOf(mailPortImap));
        props.setProperty("mail.imap.ssl.enable", "true");
        props.setProperty("mail.imap.socketFactory.class", "javax.net.ssl.SSLSocketFactory");
        props.setProperty("mail.imap.socketFactory.fallback", "false");
        props.setProperty("mail.imap.socketFactory.port", String.valueOf(mailPortImap));
        props.setProperty("mail.imap.auth", "true");
        props.setProperty("mail.imap.auth.mechanisms", "LOGIN");
        props.setProperty("mail.imap.connectiontimeout", "10000");
        props.setProperty("mail.imap.timeout", "10000");
        
        return Session.getInstance(props, new Authenticator() {
            @Override
            protected PasswordAuthentication getPasswordAuthentication() {
                return new PasswordAuthentication(mailUsername, mailPassword);
            }
        });
    }

    @Override
    @Async
    public void fetchEmails() {
        log.info("Starting to fetch emails...");
        Store store = null;
        Folder inbox = null;
        
        try {
            store = createSession().getStore("imap");
            store.connect(
                getMailConfig("mail.host-imap", mailHostImapYml),
                Integer.parseInt(getMailConfig("mail.port-imap", String.valueOf(mailPortImapYml))),
                getMailConfig("mail.username", mailUsernameYml),
                getMailConfig("mail.password", mailPasswordYml)
            );
            
            inbox = store.getFolder("INBOX");
            inbox.open(Folder.READ_WRITE);
            
            // 检查是否首次部署（数据库中是否有邮件记录）
            LambdaQueryWrapper<InboundEmail> countWrapper = new LambdaQueryWrapper<>();
            long emailCount = inboundEmailMapper.selectCount(countWrapper);
            boolean isFirstTime = emailCount == 0;
            
            Message[] messages;
            if (isFirstTime) {
                // 首次部署：获取最近100封邮件
                int totalMessages = inbox.getMessageCount();
                int fetchCount = Math.min(10, totalMessages);
                int start = Math.max(1, totalMessages - fetchCount + 1);
                messages = inbox.getMessages(start, totalMessages);
                log.info("首次部署，获取最近 {} 封邮件", fetchCount);
            } else {
                // 非首次：只获取未读邮件
                messages = inbox.search(new FlagTerm(new Flags(Flags.Flag.SEEN), false));
                log.info("获取 {} 封新邮件", messages.length);
            }
            
            for (Message message : messages) {
                try {
                    saveInboundEmail(message);
                    if (!isFirstTime) {
                        message.setFlag(Flags.Flag.SEEN, true);
                    }
                } catch (Exception e) {
                    log.error("Failed to process email: {}", e.getMessage());
                }
            }
            
            log.info("Email fetch completed");
        } catch (Exception e) {
            log.error("Failed to fetch emails: {}", e.getMessage());
        } finally {
            try {
                if (inbox != null && inbox.isOpen()) {
                    inbox.close(true);
                }
                if (store != null && store.isConnected()) {
                    store.close();
                }
            } catch (Exception e) {
                log.error("Failed to close mail connection: {}", e.getMessage());
            }
        }
    }

    private void saveInboundEmail(Message message) throws Exception {
        String fromEmail = "";
        String fromName = "";
        
        Address[] fromAddresses = message.getFrom();
        if (fromAddresses != null && fromAddresses.length > 0) {
            InternetAddress address = (InternetAddress) fromAddresses[0];
            fromEmail = address.getAddress();
            fromName = address.getPersonal();
        }
        
        String subject = message.getSubject();
        String content = extractContent(message);
        
        // getMessageID() is only available on MimeMessage
        String messageId = "";
        if (message instanceof MimeMessage) {
            messageId = ((MimeMessage) message).getMessageID();
        }
        
        // getHeader() only takes one parameter
        String[] inReplyToHeaders = message.getHeader("In-Reply-To");
        String inReplyTo = inReplyToHeaders != null && inReplyToHeaders.length > 0 ? inReplyToHeaders[0] : "";
        
        LambdaQueryWrapper<InboundEmail> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(InboundEmail::getMessageId, messageId);
        if (inboundEmailMapper.selectCount(wrapper) > 0) {
            log.info("Email already exists: {}", messageId);
            return;
        }
        
        Long companyId = findCompanyByEmail(fromEmail);
        
        InboundEmail inboundEmail = new InboundEmail();
        inboundEmail.setCompanyId(companyId);
        inboundEmail.setFromEmail(fromEmail);
        inboundEmail.setFromName(fromName);
        inboundEmail.setToEmail(getMailConfig("mail.username", mailUsernameYml));
        inboundEmail.setSubject(subject);
        inboundEmail.setContent(content);
        inboundEmail.setMessageId(messageId);
        inboundEmail.setInReplyTo(inReplyTo);
        inboundEmail.setIsRead(false);
        inboundEmail.setIsStarred(false);
        
        if (message.getSentDate() != null) {
            inboundEmail.setCreatedAt(LocalDateTime.ofInstant(
                message.getSentDate().toInstant(), ZoneId.systemDefault()));
        } else {
            inboundEmail.setCreatedAt(LocalDateTime.now());
        }
        
        inboundEmailMapper.insert(inboundEmail);
        log.info("Saved email from {}: {}", fromEmail, subject);
    }

    private String extractContent(Message message) throws Exception {
        Object content = message.getContent();
        if (content instanceof String) {
            return (String) content;
        } else if (content instanceof Multipart) {
            Multipart multipart = (Multipart) content;
            for (int i = 0; i < multipart.getCount(); i++) {
                BodyPart part = multipart.getBodyPart(i);
                if ("text/plain".equals(part.getContentType()) || 
                    "text/html".equals(part.getContentType())) {
                    return (String) part.getContent();
                }
            }
        }
        return "";
    }

    private Long findCompanyByEmail(String email) {
        if (email == null || email.isEmpty()) {
            return null;
        }
        LambdaQueryWrapper<Company> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Company::getEmail, email);
        Company company = companyMapper.selectOne(wrapper);
        return company != null ? company.getId() : null;
    }

    @Override
    public List<InboundEmail> getInbox() {
        LambdaQueryWrapper<InboundEmail> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByDesc(InboundEmail::getCreatedAt);
        return inboundEmailMapper.selectList(wrapper);
    }

    @Override
    public List<InboundEmail> getUnreadEmails() {
        LambdaQueryWrapper<InboundEmail> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(InboundEmail::getIsRead, false);
        wrapper.orderByDesc(InboundEmail::getCreatedAt);
        return inboundEmailMapper.selectList(wrapper);
    }

    @Override
    public InboundEmail getEmailById(Long id) {
        return inboundEmailMapper.selectById(id);
    }

    @Override
    @Transactional
    public void markAsRead(Long id) {
        InboundEmail email = inboundEmailMapper.selectById(id);
        if (email != null) {
            email.setIsRead(true);
            inboundEmailMapper.updateById(email);
        }
    }

    @Override
    @Transactional
    public void markAsStarred(Long id, boolean starred) {
        InboundEmail email = inboundEmailMapper.selectById(id);
        if (email != null) {
            email.setIsStarred(starred);
            inboundEmailMapper.updateById(email);
        }
    }

    @Override
    @Transactional
    public void setPriority(Long id, String priority) {
        InboundEmail email = inboundEmailMapper.selectById(id);
        if (email != null) {
            email.setPriority(priority);
            inboundEmailMapper.updateById(email);
        }
    }

    @Override
    @Transactional
    public void deleteEmail(Long id) {
        inboundEmailMapper.deleteById(id);
    }

    @Override
    public Integer getUnreadCount() {
        LambdaQueryWrapper<InboundEmail> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(InboundEmail::getIsRead, false);
        return inboundEmailMapper.selectCount(wrapper).intValue();
    }
}