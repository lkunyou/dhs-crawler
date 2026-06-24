<template>
  <el-dialog
    :model-value="visible"
    :title="title"
    :width="width"
    :top="top"
    :close-on-click-modal="closeOnClickModal"
    :close-on-press-escape="closeOnPressEscape"
    :show-close="showClose"
    :before-close="handleBeforeClose"
    @update:model-value="handleVisibleChange"
  >
    <BaseForm
      v-if="visible"
      :model-value="formData"
      :rules="rules"
      :label-width="labelWidth"
      :size="size"
      ref="formRef"
    >
      <slot></slot>
    </BaseForm>
    
    <template #footer>
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" :loading="loading" @click="handleSubmit">
        {{ submitText }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import BaseForm from './BaseForm.vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  title: { type: String, default: '' },
  width: { type: String, default: '600px' },
  top: { type: String, default: '15vh' },
  closeOnClickModal: { type: Boolean, default: true },
  closeOnPressEscape: { type: Boolean, default: true },
  showClose: { type: Boolean, default: true },
  modelValue: { type: Object, default: () => ({}) },
  rules: { type: Object, default: () => ({}) },
  labelWidth: { type: String, default: '100px' },
  size: { type: String, default: 'default' },
  submitText: { type: String, default: '确定' },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['update:visible', 'update:modelValue', 'submit', 'cancel', 'close'])

const formRef = ref(null)
const formData = reactive({ ...props.modelValue })

watch(() => props.modelValue, (newVal) => {
  Object.assign(formData, newVal)
}, { deep: true })

watch(() => props.visible, (newVal) => {
  if (newVal) {
    Object.assign(formData, props.modelValue)
  }
})

function handleVisibleChange(val) {
  emit('update:visible', val)
  if (!val) {
    emit('close')
  }
}

function handleBeforeClose(done) {
  emit('cancel')
  done()
}

function handleCancel() {
  emit('cancel')
  emit('update:visible', false)
}

function handleSubmit() {
  formRef.value?.validateAll().then((valid) => {
    if (valid) {
      emit('submit', { ...formData })
    }
  })
}

function resetForm() {
  Object.keys(formData).forEach(key => {
    formData[key] = ''
  })
}

function setFormData(data) {
  Object.assign(formData, data)
}

defineExpose({
  formRef,
  formData,
  resetForm,
  setFormData
})
</script>