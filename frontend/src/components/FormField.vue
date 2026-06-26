<template>
  <el-form-item :label="label" :prop="prop" :rules="rules">
    <el-input
      v-if="type === 'input'"
      v-model="value"
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
    />
    
    <el-input-number
      v-else-if="type === 'number'"
      v-model="value"
      :placeholder="placeholder"
      :disabled="disabled"
      :min="min"
      :max="max"
      :step="step"
      :precision="precision"
    />
    
    <el-select
      v-else-if="type === 'select'"
      v-model="value"
      :placeholder="placeholder"
      :clearable="clearable"
      :disabled="disabled"
      :multiple="multiple"
      :filterable="filterable"
      :allow-create="allowCreate"
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
      v-model="value"
      :type="dateType"
      :placeholder="placeholder"
      :disabled="disabled"
      :clearable="clearable"
      :format="format"
      :value-format="valueFormat"
    />
    
    <el-date-picker
      v-else-if="type === 'daterange'"
      v-model="value"
      type="daterange"
      range-separator="至"
      start-placeholder="开始日期"
      end-placeholder="结束日期"
      :disabled="disabled"
      :clearable="clearable"
    />
    
    <el-switch
      v-else-if="type === 'switch'"
      v-model="value"
      :disabled="disabled"
      :active-text="activeText"
      :inactive-text="inactiveText"
    />
    
    <el-input
      v-else-if="type === 'textarea'"
      v-model="value"
      type="textarea"
      :placeholder="placeholder"
      :disabled="disabled"
      :rows="rows"
      :maxlength="maxlength"
      :show-word-limit="showWordLimit"
      :resize="resize"
    />
    
    <el-cascader
      v-else-if="type === 'cascader'"
      v-model="value"
      :options="options"
      :placeholder="placeholder"
      :disabled="disabled"
      :clearable="clearable"
      :props="cascaderProps"
    />
    
    <el-color-picker
      v-else-if="type === 'color'"
      v-model="value"
      :disabled="disabled"
      :show-alpha="showAlpha"
    />
    
    <el-rate
      v-else-if="type === 'rate'"
      v-model="value"
      :disabled="disabled"
      :max="max || 5"
    />
    
    <component
      v-else-if="type === 'component'"
      :is="customComponent"
      v-model="value"
      v-bind="componentProps"
    />
  </el-form-item>
</template>

<script setup>
import { ref, watch } from 'vue'

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

const value = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  value.value = newVal
})

watch(value, (newVal) => {
  emit('update:modelValue', newVal)
  emit('change', newVal)
})
</script>