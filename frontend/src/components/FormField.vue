<template>
  <el-form-item :label="label" :prop="prop" :rules="rules">
    <el-input
      v-if="type === 'input'"
      :model-value="modelValue"
      :type="inputType"
      :placeholder="placeholder"
      :clearable="clearable"
      :disabled="disabled"
      :readonly="readonly"
      :prefix-icon="prefixIcon"
      :suffix-icon="suffixIcon"
      :show-password="showPassword"
      :maxlength="maxlength"
      :show-word-limit="showWordLimit"
      @update:model-value="handleChange"
    />
    
    <el-input-number
      v-else-if="type === 'number'"
      :model-value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :min="min"
      :max="max"
      :step="step"
      :precision="precision"
      @update:model-value="handleChange"
    />
    
    <el-select
      v-else-if="type === 'select'"
      :model-value="modelValue"
      :placeholder="placeholder"
      :clearable="clearable"
      :disabled="disabled"
      :multiple="multiple"
      :filterable="filterable"
      :allow-create="allowCreate"
      @update:model-value="handleChange"
    >
      <el-option
        v-for="option in options"
        :key="option.value"
        :label="option.label"
        :value="option.value"
      />
    </el-select>
    
    <el-date-picker
      v-else-if="type === 'date'"
      :model-value="modelValue"
      :type="dateType"
      :placeholder="placeholder"
      :disabled="disabled"
      :clearable="clearable"
      :format="format"
      :value-format="valueFormat"
      @update:model-value="handleChange"
    />
    
    <el-date-picker
      v-else-if="type === 'daterange'"
      :model-value="modelValue"
      type="daterange"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      :disabled="disabled"
      :clearable="clearable"
      @update:model-value="handleChange"
    />
    
    <el-switch
      v-else-if="type === 'switch'"
      :model-value="modelValue"
      :disabled="disabled"
      :active-text="activeText"
      :inactive-text="inactiveText"
      @update:model-value="handleChange"
    />
    
    <el-textarea
      v-else-if="type === 'textarea'"
      :model-value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :rows="rows"
      :maxlength="maxlength"
      :show-word-limit="showWordLimit"
      :resize="resize"
      @update:model-value="handleChange"
    />
    
    <el-cascader
      v-else-if="type === 'cascader'"
      :model-value="modelValue"
      :options="options"
      :placeholder="placeholder"
      :disabled="disabled"
      :clearable="clearable"
      :props="cascaderProps"
      @update:model-value="handleChange"
    />
    
    <el-color-picker
      v-else-if="type === 'color'"
      :model-value="modelValue"
      :disabled="disabled"
      :show-alpha="showAlpha"
      @update:model-value="handleChange"
    />
    
    <el-rate
      v-else-if="type === 'rate'"
      :model-value="modelValue"
      :disabled="disabled"
      :max="max || 5"
      @update:model-value="handleChange"
    />
    
    <component
      v-else-if="type === 'component'"
      :is="customComponent"
      :model-value="modelValue"
      @update:model-value="handleChange"
      v-bind="componentProps"
    />
  </el-form-item>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number, Boolean, Array, Object], default: '' },
  type: { type: String, default: 'input' },
  label: { type: String, default: '' },
  prop: { type: String, default: '' },
  rules: { type: [Array, Object], default: null },
  
  placeholder: { type: String, default: '' },
  clearable: { type: Boolean, default: true },
  disabled: { type: Boolean, default: false },
  readonly: { type: Boolean, default: false },
  
  inputType: { type: String, default: 'text' },
  prefixIcon: { type: Object, default: null },
  suffixIcon: { type: Object, default: null },
  showPassword: { type: Boolean, default: false },
  maxlength: { type: Number, default: null },
  showWordLimit: { type: Boolean, default: false },
  
  min: { type: Number, default: null },
  max: { type: Number, default: null },
  step: { type: Number, default: 1 },
  precision: { type: Number, default: null },
  
  multiple: { type: Boolean, default: false },
  filterable: { type: Boolean, default: false },
  allowCreate: { type: Boolean, default: false },
  options: { type: Array, default: () => [] },
  
  dateType: { type: String, default: 'date' },
  format: { type: String, default: '' },
  valueFormat: { type: String, default: '' },
  
  activeText: { type: String, default: '' },
  inactiveText: { type: String, default: '' },
  
  rows: { type: Number, default: 3 },
  resize: { type: String, default: 'none' },
  
  cascaderProps: { type: Object, default: () => ({}) },
  showAlpha: { type: Boolean, default: false },
  
  customComponent: { type: Object, default: null },
  componentProps: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['update:modelValue', 'change'])

function handleChange(value) {
  emit('update:modelValue', value)
  emit('change', value)
}
</script>