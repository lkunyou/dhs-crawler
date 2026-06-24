<template>
  <el-form
    :model="form"
    :rules="rules"
    :label-width="labelWidth"
    :inline="inline"
    :size="size"
    ref="formRef"
    class="base-form"
    @submit.prevent="handleSubmit"
  >
    <slot></slot>
    
    <template v-if="showFooter">
      <div class="form-footer">
        <el-button @click="handleReset">重置</el-button>
        <el-button type="primary" :loading="loading" @click="handleSubmit">
          {{ submitText }}
        </el-button>
      </div>
    </template>
  </el-form>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  modelValue: { type: Object, default: () => ({}) },
  rules: { type: Object, default: () => ({}) },
  labelWidth: { type: String, default: '100px' },
  inline: { type: Boolean, default: false },
  size: { type: String, default: 'default' },
  showFooter: { type: Boolean, default: false },
  submitText: { type: String, default: '提交' },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['submit', 'reset'])

const formRef = ref(null)
const form = reactive({ ...props.modelValue })

watch(() => props.modelValue, (newVal) => {
  Object.assign(form, newVal)
}, { deep: true })

function handleSubmit() {
  formRef.value?.validate((valid) => {
    if (valid) {
      emit('submit', { ...form })
    }
  })
}

function handleReset() {
  formRef.value?.resetFields()
  emit('reset')
}

function validate(field) {
  return formRef.value?.validateField(field)
}

function validateAll() {
  return new Promise((resolve) => {
    formRef.value?.validate((valid) => {
      resolve(valid)
    })
  })
}

defineExpose({
  form,
  formRef,
  validate,
  validateAll,
  handleReset
})
</script>

<style scoped>
.base-form {
  width: 100%;
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #EBEEF5;
}
</style>