package com.thaiautoparts.repository;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.thaiautoparts.entity.AiAgentWorkflowExec;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Update;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface AiAgentWorkflowExecMapper extends BaseMapper<AiAgentWorkflowExec> {
    
    @Update("UPDATE ai_agent_workflow_exec SET status = #{status}, updated_at = NOW() WHERE id = #{id}")
    void updateStatusById(@Param("id") Long id, @Param("status") String status);
    
    @Update("UPDATE ai_agent_workflow_exec SET current_step = #{step}, updated_at = NOW() WHERE id = #{id}")
    void updateCurrentStepById(@Param("id") Long id, @Param("step") Integer step);
    
    @Update("UPDATE ai_agent_workflow_exec SET error_message = #{error}, status = 'failed', updated_at = NOW() WHERE id = #{id}")
    void updateErrorById(@Param("id") Long id, @Param("error") String error);
    
    @Update("UPDATE ai_agent_workflow_exec SET output = #{output}, updated_at = NOW() WHERE id = #{id}")
    void updateOutputById(@Param("id") Long id, @Param("output") String output);
}
