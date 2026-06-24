<template>
  <el-form :inline="true" :model="searchForm" :size="size" class="table-search">
    <template v-for="field in fields" :key="field.prop">
      <el-form-item :label="field.label" :style="{ marginBottom: '0' }">
        <el-input
          v-if="field.type === 'input'"
          v-model="searchForm[field.prop]"
          :placeholder="field.placeholder"
          :clearable="field.clearable !== false"
          :prefix-icon="field.prefixIcon"
          @keyup.enter="handleSearch"
        />
        
        <el-select
          v-else-if="field.type === 'select'"
          v-model="searchForm[field.prop]"
          :placeholder="field.placeholder"
          :clearable="field.clearable !== false"
          :multiple="field.multiple"
        >
          <el-option
            v-for="option in field.options"
            :key="option.value"
            :label="option.label"
            :value="option.value"
          />
        </el-select>
        
        <el-date-picker
          v-else-if="field.type === 'date'"
          v-model="searchForm[field.prop]"
          :type="field.dateType || 'date'"
          :placeholder="field.placeholder"
          :clearable="field.clearable !== false"
        />
        
        <el-date-picker
          v-else-if="field.type === 'date-range'"
          v-model="searchForm[field.prop]"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          :clearable="field.clearable !== false"
        />
        
        <el-input-number
          v-else-if="field.type === 'number'"
          v-model="searchForm[field.prop]"
          :placeholder="field.placeholder"
          :min="field.min"
          :max="field.max"
          :step="field.step || 1"
        />
        
        <component
          v-else-if="field.component"
          :is="field.component"
          v-model="searchForm[field.prop]"
          v-bind="field.props || {}"
        />
      </el-form-item>
    </template>
    
    <el-form-item :style="{ marginBottom: '0' }">
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button @click="handleReset">重置</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { reactive, watch } from 'vue'

const props = defineProps({
  fields: { type: Array, default: () => [] },
  modelValue: { type: Object, default: () => ({}) },
  size: { type: String, default: 'default' }
})

const emit = defineEmits(['search', 'reset', 'update:modelValue'])

const searchForm = reactive({ ...props.modelValue })

watch(() => props.modelValue, (newVal) => {
  Object.assign(searchForm, newVal)
}, { deep: true })

function handleSearch() {
  emit('search', { ...searchForm })
  emit('update:modelValue', { ...searchForm })
}

function handleReset() {
  props.fields.forEach(field => {
    if (field.type === 'select' && field.multiple) {
      searchForm[field.prop] = []
    } else {
      searchForm[field.prop] = ''
    }
  })
  emit('reset')
  emit('update:modelValue', { ...searchForm })
}

defineExpose({
  searchForm,
  handleSearch,
  handleReset
})
</script>

<style scoped>
.table-search {
  margin-bottom: 16px;
  padding: 12px 0;
}
</style>