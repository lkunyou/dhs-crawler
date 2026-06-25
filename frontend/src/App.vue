<template>
  <router-view v-slot="{ Component }">
    <Transition name="fade" mode="out-in">
      <component :is="Component" />
    </Transition>
  </router-view>
</template>

<script setup>
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-size: 12px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.el-button {
  font-size: 12px;
}

.el-table {
  font-size: 12px;
}

.el-form-item__label {
  font-size: 12px;
}

.el-input__inner,
.el-textarea__inner {
  font-size: 12px;
}

.el-dialog__title {
  font-size: 12px;
}

.el-card__header {
  font-size: 12px;
}

.el-menu {
  font-size: 12px;
}

.el-pagination {
  font-size: 12px;
}

.el-tag {
  font-size: 10px;
}

.el-descriptions__label,
.el-descriptions__content {
  font-size: 12px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>