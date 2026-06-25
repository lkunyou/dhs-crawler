package com.thaiautoparts.event;

import lombok.Getter;
import org.springframework.context.ApplicationEvent;

@Getter
public class CrawlerTaskStartedEvent extends ApplicationEvent {

    private final Long taskId;

    public CrawlerTaskStartedEvent(Object source, Long taskId) {
        super(source);
        this.taskId = taskId;
    }
}
