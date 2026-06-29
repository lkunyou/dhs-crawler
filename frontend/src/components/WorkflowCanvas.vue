<template>
  <div class="workflow-editor">
    <!-- 顶部工具栏 -->
    <div class="editor-header">
      <div class="header-left">
        <el-button size="small" @click="handleExport">
          <el-icon><Download /></el-icon> 导出JSON
        </el-button>
      </div>
      <div class="header-center">
        <el-button size="small" @click="zoomIn" title="放大"><el-icon><ZoomIn /></el-icon></el-button>
        <el-button size="small" @click="zoomOut" title="缩小"><el-icon><ZoomOut /></el-icon></el-button>
        <el-button size="small" @click="resetZoom" title="重置"><el-icon><Refresh /></el-icon></el-button>
        <el-button size="small" @click="fitView" title="适应"><el-icon><FullScreen /></el-icon></el-button>
      </div>
      <div class="header-right">
        <el-button size="small" @click="clearCanvas" title="清空"><el-icon><Delete /></el-icon> 清空</el-button>
      </div>
    </div>

    <div class="editor-body">
      <!-- 左侧节点库 -->
      <div class="node-panel">
        <div class="panel-title">节点库</div>
        <div class="node-hint">点击节点添加到画布</div>
        <div class="node-list">
          <div class="node-category">
            <div class="category-title">AI 节点</div>
            <div class="node-item node-llm" @click="addNodeToCanvas('llm')">
              <el-icon><Cpu /></el-icon><span>LLM</span>
            </div>
            <div class="node-item node-classifier" @click="addNodeToCanvas('classifier')">
              <el-icon><Grid /></el-icon><span>分类器</span>
            </div>
            <div class="node-item node-extractor" @click="addNodeToCanvas('extractor')">
              <el-icon><Edit /></el-icon><span>变量提取器</span>
            </div>
          </div>
          <div class="node-category">
            <div class="category-title">知识库</div>
            <div class="node-item node-knowledge" @click="addNodeToCanvas('knowledge')">
              <el-icon><Reading /></el-icon><span>知识库</span>
            </div>
            <div class="node-item node-knowledge-write" @click="addNodeToCanvas('knowledgeWrite')">
              <el-icon><Document /></el-icon><span>知识库写入</span>
            </div>
          </div>
          <div class="node-category">
            <div class="category-title">逻辑控制</div>
            <div class="node-item node-condition" @click="addNodeToCanvas('condition')">
              <el-icon><Share /></el-icon><span>条件分支</span>
            </div>
            <div class="node-item node-loop" @click="addNodeToCanvas('loop')">
              <el-icon><RefreshRight /></el-icon><span>循环</span>
            </div>
            <div class="node-item node-subflow" @click="addNodeToCanvas('subflow')">
              <el-icon><Connection /></el-icon><span>子流程</span>
            </div>
          </div>
          <div class="node-category">
            <div class="category-title">数据处理</div>
            <div class="node-item node-aggregate" @click="addNodeToCanvas('aggregate')">
              <el-icon><Collection /></el-icon><span>变量聚合</span>
            </div>
            <div class="node-item node-script" @click="addNodeToCanvas('script')">
              <el-icon><EditPen /></el-icon><span>脚本执行</span>
            </div>
            <div class="node-item node-reply" @click="addNodeToCanvas('reply')">
              <el-icon><ChatDotRound /></el-icon><span>直接回复</span>
            </div>
          </div>
          <div class="node-category">
            <div class="category-title">工具 & 数据</div>
            <div class="node-item node-tool" @click="addNodeToCanvas('tool')">
              <el-icon><Tools /></el-icon><span>工具调用</span>
            </div>
            <div class="node-item node-http" @click="addNodeToCanvas('http')">
              <el-icon><Link /></el-icon><span>HTTP 请求</span>
            </div>
            <div class="node-item node-sql" @click="addNodeToCanvas('sql')">
              <el-icon><Coin /></el-icon><span>SQL自定义</span>
            </div>
            <div class="node-item node-java" @click="addNodeToCanvas('java')">
              <el-icon><Monitor /></el-icon><span>Java 增强</span>
            </div>
          </div>
          <div class="node-category">
            <div class="category-title">基础节点</div>
            <div class="node-item node-end" @click="addNodeToCanvas('end')">
              <el-icon><VideoPause /></el-icon><span>结束</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间画布 -->
      <div class="canvas-area" ref="lfContainer"></div>

      <!-- 右侧属性面板 -->
      <div class="property-panel" v-if="selectedNode" @click.stop>
        <div class="panel-title">
          节点属性
          <el-icon style="cursor:pointer; margin-left: auto;" @click="selectedNode = null"><Close /></el-icon>
        </div>
        <el-form :model="nodeForm" label-width="80px" size="small">
          <el-form-item label="节点名称">
            <el-input v-model="nodeForm.name" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="节点类型">
            <el-tag size="small">{{ getNodeTypeName(nodeForm.nodeType) }}</el-tag>
          </el-form-item>
          <el-form-item label="输入变量" v-if="nodeForm.nodeType !== 'end'">
            <el-input v-model="nodeForm.inputVars" type="textarea" :rows="2" placeholder="每行一个变量名" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="输出变量" v-if="nodeForm.nodeType !== 'end'">
            <el-input v-model="nodeForm.outputVars" type="textarea" :rows="2" placeholder="每行一个变量名" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="模型" v-if="nodeForm.nodeType === 'llm'">
            <el-select v-model="nodeForm.model" placeholder="选择模型" style="width: 100%" @change="applyNodeChanges">
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="Qwen" value="qwen" />
              <el-option label="Kimi" value="kimi" />
              <el-option label="GLM" value="glm" />
            </el-select>
          </el-form-item>
          <el-form-item label="提示词" v-if="nodeForm.nodeType === 'llm' || nodeForm.nodeType === 'classifier'">
            <el-input v-model="nodeForm.prompt" type="textarea" :rows="4" placeholder="系统提示词" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="提取字段" v-if="nodeForm.nodeType === 'extractor'">
            <el-input v-model="nodeForm.prompt" type="textarea" :rows="3" placeholder="定义要提取的字段" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="知识库ID" v-if="nodeForm.nodeType === 'knowledge' || nodeForm.nodeType === 'knowledgeWrite'">
            <el-input v-model="nodeForm.toolName" placeholder="知识库标识" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="条件表达式" v-if="nodeForm.nodeType === 'condition'">
            <el-input v-model="nodeForm.condition" placeholder="例如: input.count > 0" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="循环条件" v-if="nodeForm.nodeType === 'loop'">
            <el-input v-model="nodeForm.condition" placeholder="循环条件表达式" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="子流程ID" v-if="nodeForm.nodeType === 'subflow'">
            <el-input v-model="nodeForm.toolName" placeholder="子流程标识" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="聚合字段" v-if="nodeForm.nodeType === 'aggregate'">
            <el-input v-model="nodeForm.prompt" type="textarea" :rows="3" placeholder="聚合规则" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="脚本代码" v-if="nodeForm.nodeType === 'script'">
            <el-input v-model="nodeForm.scriptCode" type="textarea" :rows="4" placeholder="Groovy/JS代码" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="回复内容" v-if="nodeForm.nodeType === 'reply'">
            <el-input v-model="nodeForm.prompt" type="textarea" :rows="4" placeholder="回复内容模板" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="工具名" v-if="nodeForm.nodeType === 'tool'">
            <el-input v-model="nodeForm.toolName" placeholder="MCP工具名称" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="URL" v-if="nodeForm.nodeType === 'http'">
            <el-input v-model="nodeForm.toolName" placeholder="请求URL" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="SQL语句" v-if="nodeForm.nodeType === 'sql'">
            <el-input v-model="nodeForm.scriptCode" type="textarea" :rows="4" placeholder="SQL语句" @blur="applyNodeChanges" />
          </el-form-item>
          <el-form-item label="Java类名" v-if="nodeForm.nodeType === 'java'">
            <el-input v-model="nodeForm.toolName" placeholder="Java类全名" @blur="applyNodeChanges" />
          </el-form-item>
          <el-divider />
          <el-button type="danger" size="small" @click.stop="deleteSelectedNode" style="width: 100%">删除节点</el-button>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Check, Download, ZoomIn, ZoomOut, Refresh, FullScreen, Delete,
  VideoPause, Cpu, Tools, EditPen, Share, Close,
  Grid, Edit, Document, ChatDotRound, Link, Coin, Monitor,
  Connection, Collection, RefreshRight, Reading
} from '@element-plus/icons-vue'
import LogicFlow from '@logicflow/core'
import '@logicflow/core/es/style/index.css'

const props = defineProps({ modelValue: { type: Array, default: () => [] } })
const emit = defineEmits(['update:modelValue', 'save'])

const lfContainer = ref(null)
const lf = ref(null)
const selectedNode = ref(null)
const nodeForm = ref({
  id: '', name: '', nodeType: '',
  inputVars: '', outputVars: '',
  model: '', prompt: '', scriptCode: '',
  condition: '', toolName: ''
})
let resizeObserver = null
let nodeCounter = 0

// 节点类型配置：颜色、图标SVG路径
const nodeTypeMap = {
  llm:           { name: 'LLM',       color: '#409EFF', icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z' },
  classifier:    { name: '分类器',     color: '#409EFF', icon: 'M3 3h8v8H3V3zm0 10h8v8H3v-8zm10-10h8v8h-8V3zm0 10h8v8h-8v-8z' },
  extractor:     { name: '变量提取器', color: '#409EFF', icon: 'M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z' },
  knowledge:     { name: '知识库',     color: '#67C23A', icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z' },
  knowledgeWrite:{ name: '知识库写入', color: '#67C23A', icon: 'M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z' },
  condition:     { name: '条件分支',   color: '#E6A23C', icon: 'M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z' },
  loop:          { name: '循环',       color: '#E6A23C', icon: 'M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z' },
  subflow:       { name: '子流程',     color: '#E6A23C', icon: 'M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z' },
  aggregate:     { name: '变量聚合',   color: '#909399', icon: 'M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z' },
  script:        { name: '脚本执行',   color: '#909399', icon: 'M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z' },
  reply:         { name: '直接回复',   color: '#909399', icon: 'M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z' },
  tool:          { name: '工具调用',   color: '#F56C6C', icon: 'M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z' },
  http:          { name: 'HTTP 请求',  color: '#F56C6C', icon: 'M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z' },
  sql:           { name: 'SQL自定义',  color: '#F56C6C', icon: 'M12 2C6.48 2 2 4.02 2 6.5S6.48 11 12 11s10-2.02 10-4.5S17.52 2 12 2zm0 13c-5.52 0-10-2.02-10-4.5v3C2 16.02 6.48 18 12 18s10-1.98 10-4.5v-3C22 12.98 17.52 15 12 15zm0 5c-5.52 0-10-2.02-10-4.5v3C2 21.02 6.48 23 12 23s10-1.98 10-4.5v-3C22 17.98 17.52 20 12 20z' },
  java:          { name: 'Java 增强',  color: '#F56C6C', icon: 'M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zM5 15h14v3H5z' },
  end:           { name: '结束',       color: '#F56C6C', icon: 'M6 6h12v12H6z' }
}

const getNodeTypeName = (t) => nodeTypeMap[t]?.name || t

// SVG 图标映射
const nodeIcons = {
  llm: '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93z"/>',
  classifier: '<path d="M3 3h8v8H3V3zm0 10h8v8H3v-8zm10-10h8v8h-8V3zm0 10h8v8h-8v-8z"/>',
  extractor: '<path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>',
  knowledge: '<path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>',
  knowledgeWrite: '<path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z"/>',
  condition: '<path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>',
  loop: '<path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46C19.54 15.03 20 13.57 20 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74C4.46 8.97 4 10.43 4 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"/>',
  subflow: '<path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/>',
  aggregate: '<path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zM9 17H7v-7h2v7zm4 0h-2V7h2v10zm4 0h-2v-4h2v4z"/>',
  script: '<path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>',
  reply: '<path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17L4 17.17V4h16v12z"/>',
  tool: '<path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/>',
  http: '<path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/>',
  sql: '<path d="M12 2C6.48 2 2 4.02 2 6.5S6.48 11 12 11s10-2.02 10-4.5S17.52 2 12 2zm0 13c-5.52 0-10-2.02-10-4.5v3C2 16.02 6.48 18 12 18s10-1.98 10-4.5v-3C22 12.98 17.52 15 12 15zm0 5c-5.52 0-10-2.02-10-4.5v3C2 21.02 6.48 23 12 23s10-1.98 10-4.5v-3C22 17.98 17.52 20 12 20z"/>',
  java: '<path d="M21 3H3c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H3V5h18v14zM5 15h14v3H5z"/>',
  end: '<path d="M6 6h12v12H6z"/>'
}

onMounted(() => {
  nextTick(() => { setTimeout(() => initLogicFlow(), 300) })
})

onUnmounted(() => {
  if (resizeObserver) resizeObserver.disconnect()
  lf.value?.destroy()
})

// 监听容器尺寸变化，确保画布正确初始化
watch(lfContainer, () => {
  nextTick(() => {
    setTimeout(() => {
      if (lfContainer.value && lfContainer.value.clientWidth > 0 && lfContainer.value.clientHeight > 0) {
        if (!lf.value) {
          console.log('[WorkflowCanvas] Container visible, initializing LogicFlow')
          initLogicFlow()
        } else {
          lf.value.resize(lfContainer.value.clientWidth, lfContainer.value.clientHeight)
        }
      }
    }, 200)
  })
})

// 注册自定义节点
const registerCustomNodes = (LogicFlowClass) => {
  Object.keys(nodeTypeMap).forEach(type => {
    const config = nodeTypeMap[type]
    const iconPath = nodeIcons[type] || nodeIcons.llm

    class CustomNode extends LogicFlowClass.BaseNode {
      static extendKey = `customNode_${type}`

      getShape() {
        return 'custom-node'
      }
    }

    LogicFlowClass.register(CustomNode)
  })
}

const initLogicFlow = () => {
  if (!lfContainer.value) {
    console.warn('[WorkflowCanvas] Container not ready, retrying...')
    setTimeout(() => initLogicFlow(), 200)
    return
  }

  if (lf.value) { lf.value.destroy(); lf.value = null }

  const w = lfContainer.value.clientWidth || 600
  const h = lfContainer.value.clientHeight || 400
  console.log('[WorkflowCanvas] Init with size:', w, 'x', h)

  lf.value = new LogicFlow({
    container: lfContainer.value,
    width: w,
    height: h,
    grid: { size: 20, type: 'dot' },
    keyboard: { enabled: true },
    style: {
      rect: { width: 140, height: 60, radius: 8, fill: '#fff', stroke: '#dcdfe6', strokeWidth: 1.5 },
      text: { fontSize: 12, fill: '#303133' },
      edge: { stroke: '#909399', strokeWidth: 1.5 }
    }
  })

  lf.value.on('node:click', ({ data }) => selectNode(data))
  lf.value.on('blank:click', () => { selectedNode.value = null })
  lf.value.on('edge:click', ({ data }) => {
    if (confirm('确定删除此连线？')) lf.value.deleteEdge(data.id)
  })

  if (resizeObserver) resizeObserver.disconnect()
  resizeObserver = new ResizeObserver(() => {
    if (lf.value && lfContainer.value) {
      const newW = lfContainer.value.clientWidth
      const newH = lfContainer.value.clientHeight
      if (newW > 0 && newH > 0) lf.value.resize(newW, newH)
    }
  })
  resizeObserver.observe(lfContainer.value)

  // 加载初始数据（兼容数组和对象格式）
  const hasData = Array.isArray(props.modelValue) 
    ? props.modelValue.length > 0 
    : (props.modelValue?.steps?.length > 0)
  
  if (hasData) {
    loadStepsToCanvas(props.modelValue)
  }
}

let dragType = ''
const onDragStart = (event, type) => {
  dragType = type
  event.dataTransfer.effectAllowed = 'copy'
  event.dataTransfer.setData('text/plain', type)
}

const addNodeToCanvas = (type) => {
  console.log('[WorkflowCanvas] addNodeToCanvas called with type:', type)
  console.log('[WorkflowCanvas] lf.value:', lf.value)

  if (!lf.value) {
    console.warn('[WorkflowCanvas] LogicFlow not initialized, trying to init...')
    initLogicFlow()
    setTimeout(() => {
      if (lf.value) {
        doAddNode(type)
      } else {
        ElMessage.error('画布未初始化，请刷新页面重试')
      }
    }, 500)
    return
  }
  doAddNode(type)
}

const doAddNode = (type) => {
  const info = nodeTypeMap[type]
  if (!info) {
    console.error('[WorkflowCanvas] Unknown node type:', type)
    return
  }
  const id = `node_${Date.now()}`
  nodeCounter++
  const col = (nodeCounter - 1) % 3
  const row = Math.floor((nodeCounter - 1) / 3)
  const x = 200 + col * 220
  const y = 100 + row * 150

  console.log('[WorkflowCanvas] Adding node:', { id, type: 'custom-node', x, y, text: info.name, nodeType: type })

  try {
    lf.value.addNode({
      id, type: 'rect', x, y,
      text: info.name,
      properties: { nodeType: type, config: '{}' }
    })
    updateStepsFromCanvas()
    console.log('[WorkflowCanvas] Node added successfully')
  } catch (e) {
    console.error('[WorkflowCanvas] Failed to add node:', e)
    ElMessage.error('添加节点失败: ' + e.message)
  }
}

const selectNode = (data) => {
  const nodeModel = lf.value.getNodeModelById(data.id)
  const props = nodeModel?.properties || {}
  nodeForm.value = {
    id: data.id,
    name: data.text?.value || data.text || '',
    nodeType: props.nodeType || 'llm',
    inputVars: props.inputVars || '',
    outputVars: props.outputVars || '',
    model: props.model || '',
    prompt: props.prompt || '',
    scriptCode: props.scriptCode || '',
    condition: props.condition || '',
    toolName: props.toolName || ''
  }
  selectedNode.value = data
}

const applyNodeChanges = () => {
  if (!lf.value || !nodeForm.value.id) return
  const id = nodeForm.value.id

  // 更新节点文本
  lf.value.updateText(id, nodeForm.value.name)

  // 更新节点属性 - 使用 updateNode 确保数据持久化
  const nodeModel = lf.value.getNodeModelById(id)
  if (nodeModel) {
    const newProps = {
      nodeType: nodeForm.value.nodeType,
      inputVars: nodeForm.value.inputVars,
      outputVars: nodeForm.value.outputVars,
      model: nodeForm.value.model,
      prompt: nodeForm.value.prompt,
      scriptCode: nodeForm.value.scriptCode,
      condition: nodeForm.value.condition,
      toolName: nodeForm.value.toolName
    }
    // 直接修改 model 的 properties
    Object.assign(nodeModel.properties, newProps)
    nodeModel.setProperties(newProps)
  }

  updateStepsFromCanvas()
}

const deleteSelectedNode = () => {
  alert(`删除函数被调用，节点ID: ${nodeForm.value.id}`)
  console.log('[WorkflowCanvas] deleteSelectedNode called, lf:', !!lf.value, 'nodeId:', nodeForm.value.id)
  if (!lf.value || !nodeForm.value.id) {
    console.warn('[WorkflowCanvas] Delete aborted: lf or nodeId missing')
    ElMessage.warning('无法删除：节点未选中')
    return
  }
  const nodeId = nodeForm.value.id

  // 先检查节点是否存在
  const nodeModel = lf.value.getNodeModelById(nodeId)
  console.log('[WorkflowCanvas] Node model found:', !!nodeModel)

  if (!nodeModel) {
    ElMessage.warning('节点不存在或已被删除')
    selectedNode.value = null
    nodeForm.value = { id: '', name: '', nodeType: '', inputVars: '', outputVars: '', model: '', prompt: '', scriptCode: '', condition: '', toolName: '' }
    return
  }

  try {
    console.log('[WorkflowCanvas] Attempting to delete node via graphModel:', nodeId)
    // 直接使用 graphModel 删除
    lf.value.graphModel.deleteNode(nodeId)
    console.log('[WorkflowCanvas] graphModel.deleteNode succeeded')

    // 验证节点是否真的被删除
    const stillExists = lf.value.getNodeModelById(nodeId)
    console.log('[WorkflowCanvas] Node still exists after delete:', !!stillExists)

    if (stillExists) {
      throw new Error('节点删除后仍然存在')
    }
  } catch (e) {
    console.error('[WorkflowCanvas] Delete failed:', e)
    ElMessage.error('删除失败: ' + e.message)
    return
  }

  selectedNode.value = null
  nodeForm.value = { id: '', name: '', nodeType: '', inputVars: '', outputVars: '', model: '', prompt: '', scriptCode: '', condition: '', toolName: '' }
  updateStepsFromCanvas()
  ElMessage.success('节点已删除')
}

const zoomIn = () => lf.value?.zoom(true)
const zoomOut = () => lf.value?.zoom(false)
const resetZoom = () => lf.value?.resetZoom()
const fitView = () => lf.value?.fitView()

const clearCanvas = () => {
  lf.value?.clearData()
  selectedNode.value = null
  nodeCounter = 0
  updateStepsFromCanvas()
}

const handleSave = () => {
  updateStepsFromCanvas()
  emit('save', props.modelValue)
  ElMessage.success('工作流已保存')
}

const handleExport = () => {
  if (!lf.value) return
  const data = JSON.stringify(lf.value.getGraphData(), null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = 'workflow.json'; a.click()
  URL.revokeObjectURL(url)
}

const loadStepsToCanvas = (data) => {
  if (!lf.value) return

  // 兼容旧格式（数组）和新格式（对象）
  let steps = []
  let edges = []

  if (Array.isArray(data)) {
    // 旧格式：只有步骤数组
    steps = data
  } else if (data && typeof data === 'object') {
    // 新格式：包含 steps 和 edges
    steps = data.steps || []
    edges = data.edges || []
  }

  console.log('[WorkflowCanvas] loadStepsToCanvas:', {
    stepsCount: steps.length,
    edgesCount: edges.length,
    edges: JSON.parse(JSON.stringify(edges))
  })

  if (!steps.length) return

  lf.value.clearData()
  nodeCounter = 0

  // 加载节点 - 先记录所有节点ID
  const loadedNodeIds = new Set()
  steps.forEach((step, i) => {
    const nodeId = step.id || `node_${i}`
    loadedNodeIds.add(nodeId)
    const info = nodeTypeMap[step.nodeType] || nodeTypeMap.llm
    lf.value.addNode({
      id: nodeId, type: 'rect',
      x: step.x || (150 + (i % 4) * 200),
      y: step.y || (100 + Math.floor(i / 4) * 140),
      text: step.name || info.name,
      properties: {
        nodeType: step.nodeType,
        config: step.config || '{}',
        inputVars: step.inputVars || '',
        outputVars: step.outputVars || '',
        model: step.model || '',
        prompt: step.prompt || '',
        scriptCode: step.scriptCode || '',
        condition: step.condition || '',
        toolName: step.toolName || ''
      }
    })
    nodeCounter++
  })

  console.log('[WorkflowCanvas] Loaded node IDs:', Array.from(loadedNodeIds))

  // 加载连线
  if (edges.length > 0) {
    // 去重：同一 sourceNodeId -> targetNodeId 只保留最后一条
    const uniqueEdges = []
    const edgeKeys = new Set()
    // 反向遍历，保留最后出现的边
    for (let i = edges.length - 1; i >= 0; i--) {
      const edge = edges[i]
      const key = `${edge.sourceNodeId}->${edge.targetNodeId}`
      if (!edgeKeys.has(key)) {
        edgeKeys.add(key)
        uniqueEdges.unshift(edge)
      }
    }
    
    console.log('[WorkflowCanvas] Deduplicated edges:', edges.length, '->', uniqueEdges.length)

    uniqueEdges.forEach((edge, idx) => {
      console.log(`[WorkflowCanvas] Loading edge[${idx}]: ${edge.sourceNodeId} -> ${edge.targetNodeId}`)
      
      // 验证源节点和目标节点是否存在
      if (!loadedNodeIds.has(edge.sourceNodeId)) {
        console.warn(`[WorkflowCanvas] Edge[${idx}] source node '${edge.sourceNodeId}' not found!`)
        return
      }
      if (!loadedNodeIds.has(edge.targetNodeId)) {
        console.warn(`[WorkflowCanvas] Edge[${idx}] target node '${edge.targetNodeId}' not found!`)
        return
      }
      
      const edgeData = {
        id: edge.id,
        sourceNodeId: edge.sourceNodeId,
        targetNodeId: edge.targetNodeId,
        type: edge.type || 'polyline'
      }
      // 恢复路径坐标点
      if (edge.pointsList && edge.pointsList.length > 0) {
        edgeData.pointsList = edge.pointsList
      }
      
      lf.value.addEdge(edgeData)
    })
    
    // 验证加载后的边
    setTimeout(() => {
      const addedEdges = lf.value.getGraphData()?.edges || []
      console.log('[WorkflowCanvas] Edges after loading:', addedEdges.map(e => `${e.sourceNodeId}->${e.targetNodeId}`))
    }, 100)
  } else {
    // 旧数据没有连线信息，按顺序连接
    for (let i = 0; i < steps.length - 1; i++) {
      const srcId = steps[i].id || `node_${i}`
      const tgtId = steps[i + 1].id || `node_${i + 1}`
      lf.value.addEdge({ id: `edge_${i}`, sourceNodeId: srcId, targetNodeId: tgtId })
    }
  }
}

const updateStepsFromCanvas = () => {
  if (!lf.value) return
  const gd = lf.value.getGraphData()

  // 保存节点数据
  const steps = gd.nodes.map(node => {
    const nodeModel = lf.value.getNodeModelById(node.id)
    const props = nodeModel?.properties || node.properties || {}
    const nt = props.nodeType || 'llm'
    let stepType = 'agent'
    if (nt === 'end') stepType = 'end'
    else if (nt === 'knowledge' || nt === 'knowledgeWrite') stepType = 'knowledge'
    else if (nt === 'condition') stepType = 'condition'
    else if (nt === 'loop') stepType = 'loop'
    else if (nt === 'subflow') stepType = 'subflow'
    else if (nt === 'aggregate') stepType = 'aggregate'
    else if (nt === 'script') stepType = 'script'
    else if (nt === 'reply') stepType = 'reply'
    else if (nt === 'tool') stepType = 'mcp'
    else if (nt === 'http') stepType = 'http'
    else if (nt === 'sql') stepType = 'sql'
    else if (nt === 'java') stepType = 'java'
    else if (nt === 'classifier') stepType = 'classifier'
    else if (nt === 'extractor') stepType = 'extractor'
    const savedX = nodeModel?.x ?? node.x ?? 0
    const savedY = nodeModel?.y ?? node.y ?? 0
    return {
      id: node.id, name: node.text?.value || node.text || '',
      type: stepType, nodeType: nt,
      x: savedX, y: savedY,
      config: props.config || '{}',
      inputVars: props.inputVars || '',
      outputVars: props.outputVars || '',
      model: props.model || '', prompt: props.prompt || '',
      scriptCode: props.scriptCode || '', condition: props.condition || '',
      toolName: props.toolName || ''
    }
  })

  // 去重边：LogicFlow 在用户重新连接边时会创建新边而不会删除旧边
  // 去重 key 需要包含锚点信息，因为同一对节点之间可能有多条边（不同锚点）
  const edgeMap = new Map()
  
  gd.edges.forEach(edge => {
    const edgeModel = lf.value.getEdgeModelById(edge.id)
    if (!edgeModel) return
    
    const src = edgeModel.sourceNodeId || ''
    const tgt = edgeModel.targetNodeId || ''
    const srcAnchor = edgeModel.sourceAnchorId || ''
    const tgtAnchor = edgeModel.targetAnchorId || ''
    // 用 源节点+源锚点->目标节点+目标锚点 作为去重 key
    const key = `${src}_${srcAnchor}->${tgt}_${tgtAnchor}`
    
    // 如果已存在相同锚点的边，跳过（保留第一条）
    if (edgeMap.has(key)) return
    
    // 优先从 gd.edges 中获取 pointsList
    let pointsList = edge.pointsList
    if (!pointsList || pointsList.length === 0) {
      const edgeData = edgeModel.getData()
      pointsList = edgeData.pointsList
    }
    if (!pointsList || pointsList.length === 0) {
      const sp = edgeModel.startPoint
      const ep = edgeModel.endPoint
      if (sp && ep) {
        pointsList = [{ x: sp.x, y: sp.y }, { x: ep.x, y: ep.y }]
      } else {
        pointsList = []
      }
    }
    
    edgeMap.set(key, {
      id: edge.id,
      sourceNodeId: src,
      targetNodeId: tgt,
      type: edge.type || 'polyline',
      sourceAnchorId: srcAnchor,
      targetAnchorId: tgtAnchor,
      pointsList
    })
  })

  const edges = Array.from(edgeMap.values())
  
  console.log('[WorkflowCanvas] Saved edges (deduplicated):', edges.length, 'edges:', edges.map(e => `${e.sourceNodeId}->${e.targetNodeId}`))

  const data = { steps, edges }
  emit('update:modelValue', data)
}

defineExpose({
  getSteps: () => {
    if (!lf.value) return []
    const gd = lf.value.getGraphData()
    return gd.nodes.map(node => {
      const nodeModel = lf.value.getNodeModelById(node.id)
      const props = node.properties || {}
      const nt = props.nodeType || 'llm'
      let stepType = 'agent'
      if (nt === 'end') stepType = 'end'
      else if (nt === 'knowledge' || nt === 'knowledgeWrite') stepType = 'knowledge'
      else if (nt === 'condition') stepType = 'condition'
      else if (nt === 'loop') stepType = 'loop'
      else if (nt === 'subflow') stepType = 'subflow'
      else if (nt === 'aggregate') stepType = 'aggregate'
      else if (nt === 'script') stepType = 'script'
      else if (nt === 'reply') stepType = 'reply'
      else if (nt === 'tool') stepType = 'mcp'
      else if (nt === 'http') stepType = 'http'
      else if (nt === 'sql') stepType = 'sql'
      else if (nt === 'java') stepType = 'java'
      else if (nt === 'classifier') stepType = 'classifier'
      else if (nt === 'extractor') stepType = 'extractor'
      const savedX = nodeModel?.x ?? node.x ?? 0
      const savedY = nodeModel?.y ?? node.y ?? 0
      return {
        id: node.id, name: node.text?.value || node.text || '',
        type: stepType, nodeType: nt,
        x: savedX, y: savedY,
        config: props.config || '{}',
        inputVars: props.inputVars || '',
        outputVars: props.outputVars || '',
        model: props.model || '', prompt: props.prompt || '',
        scriptCode: props.scriptCode || '', condition: props.condition || '',
        toolName: props.toolName || ''
      }
    })
  },
  syncSteps: () => {
    // 直接返回当前画布数据，不依赖 emit
    if (!lf.value) return { steps: [], edges: [] }
    const gd = lf.value.getGraphData()
    
    const steps = gd.nodes.map(node => {
      const nodeModel = lf.value.getNodeModelById(node.id)
      const props = nodeModel?.properties || node.properties || {}
      const nt = props.nodeType || 'llm'
      let stepType = 'agent'
      if (nt === 'end') stepType = 'end'
      else if (nt === 'knowledge' || nt === 'knowledgeWrite') stepType = 'knowledge'
      else if (nt === 'condition') stepType = 'condition'
      else if (nt === 'loop') stepType = 'loop'
      else if (nt === 'subflow') stepType = 'subflow'
      else if (nt === 'aggregate') stepType = 'aggregate'
      else if (nt === 'script') stepType = 'script'
      else if (nt === 'reply') stepType = 'reply'
      else if (nt === 'tool') stepType = 'mcp'
      else if (nt === 'http') stepType = 'http'
      else if (nt === 'sql') stepType = 'sql'
      else if (nt === 'java') stepType = 'java'
      else if (nt === 'classifier') stepType = 'classifier'
      else if (nt === 'extractor') stepType = 'extractor'
      const savedX = nodeModel?.x ?? node.x ?? 0
      const savedY = nodeModel?.y ?? node.y ?? 0
      return {
        id: node.id, name: node.text?.value || node.text || '',
        type: stepType, nodeType: nt,
        x: savedX, y: savedY,
        config: props.config || '{}',
        inputVars: props.inputVars || '',
        outputVars: props.outputVars || '',
        model: props.model || '', prompt: props.prompt || '',
        scriptCode: props.scriptCode || '', condition: props.condition || '',
        toolName: props.toolName || ''
      }
    })

    const edges = gd.edges.map(edge => {
      const edgeModel = lf.value.getEdgeModelById(edge.id)
      return {
        id: edge.id,
        sourceNodeId: edgeModel?.sourceNodeId || edge.sourceNodeId || edge.source,
        targetNodeId: edgeModel?.targetNodeId || edge.targetNodeId || edge.target,
        type: edge.type || 'polyline',
        sourceAnchorId: edgeModel?.sourceAnchorId || edge.sourceAnchorId || '',
        targetAnchorId: edgeModel?.targetAnchorId || edge.targetAnchorId || '',
        pointsList: edgeModel?.pointsList || edge.pointsList || []
      }
    })

    const data = { steps, edges }
    console.log('[WorkflowCanvas] syncSteps:', JSON.stringify(data))
    return data
  },
  loadSteps: (steps) => {
    if (lf.value) loadStepsToCanvas(steps)
    else setTimeout(() => lf.value && loadStepsToCanvas(steps), 300)
  },
  clearCanvas: () => lf.value?.clearData(),
  refresh: () => {
    const tryInit = (attempt) => {
      if (attempt > 10) return
      if (lfContainer.value) {
        const w = lfContainer.value.clientWidth
        const h = lfContainer.value.clientHeight
        if (w > 0 && h > 0) {
          initLogicFlow()
        } else {
          setTimeout(() => tryInit(attempt + 1), 200)
        }
      }
    }
    tryInit(1)
  }
})
</script>

<style scoped>
.workflow-editor {
  width: 100%; height: 100%;
  display: flex; flex-direction: column;
  border: 1px solid #dcdfe6; border-radius: 4px; overflow: hidden;
  background: #fff;
}
.editor-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 12px; background: #fff;
  border-bottom: 1px solid #ebeef5; flex-shrink: 0;
}
.header-left, .header-center, .header-right {
  display: flex; align-items: center; gap: 4px;
}
.editor-body {
  display: flex; flex: 1; overflow: hidden;
}
.node-panel {
  width: 160px; flex-shrink: 0;
  border-right: 1px solid #ebeef5;
  background: #fafafa; overflow-y: auto;
}
.panel-title {
  padding: 10px 12px; font-size: 13px; font-weight: bold;
  color: #303133; border-bottom: 1px solid #ebeef5;
  display: flex; align-items: center;
}
.node-hint {
  padding: 6px 12px; font-size: 11px; color: #909399;
  background: #f0f9eb; border-bottom: 1px solid #ebeef5;
}
.node-list { padding: 8px; }
.node-category { margin-bottom: 12px; }
.category-title {
  font-size: 11px; color: #909399; margin-bottom: 6px; padding: 0 4px;
}
.node-item {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 10px; margin-bottom: 4px;
  border: 1px solid #ebeef5; border-radius: 6px;
  background: #fff; cursor: pointer; font-size: 12px;
  transition: all 0.2s;
  user-select: none;
}
.node-item:hover { border-color: #409EFF; box-shadow: 0 2px 6px rgba(64,158,255,0.15); transform: translateX(2px); }
.node-item:active { transform: scale(0.97); }
.node-llm { border-left: 3px solid #409EFF; }
.node-classifier { border-left: 3px solid #409EFF; }
.node-extractor { border-left: 3px solid #409EFF; }
.node-knowledge { border-left: 3px solid #67C23A; }
.node-knowledge-write { border-left: 3px solid #67C23A; }
.node-condition { border-left: 3px solid #E6A23C; }
.node-loop { border-left: 3px solid #E6A23C; }
.node-subflow { border-left: 3px solid #E6A23C; }
.node-aggregate { border-left: 3px solid #909399; }
.node-script { border-left: 3px solid #909399; }
.node-reply { border-left: 3px solid #909399; }
.node-tool { border-left: 3px solid #F56C6C; }
.node-http { border-left: 3px solid #F56C6C; }
.node-sql { border-left: 3px solid #F56C6C; }
.node-java { border-left: 3px solid #F56C6C; }
.node-end { border-left: 3px solid #F56C6C; }
.canvas-area {
  flex: 1; background: #f5f7fa;
  min-width: 0; position: relative;
}
.property-panel {
  width: 280px; flex-shrink: 0;
  border-left: 1px solid #ebeef5;
  background: #fff; overflow-y: auto;
  position: relative; z-index: 10;
}
</style>
