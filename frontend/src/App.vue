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
  font-size: 13px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f8fafc;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.el-button {
  font-size: 13px;
  border-radius: 6px;
  padding: 8px 16px;
}

.el-button--primary {
  background-color: #2563eb;
  border-color: #2563eb;
}

.el-button--primary:hover {
  background-color: #1d4ed8;
  border-color: #1d4ed8;
}

.el-table {
  font-size: 13px;
  border-radius: 8px;
  overflow: hidden;
}

.el-table th.el-table__cell {
  background-color: #f8fafc;
  color: #64748b;
  font-weight: 500;
  padding: 12px 16px;
}

.el-table td.el-table__cell {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
  background-color: #ffffff;
}

.el-table__body tr:hover > td.el-table__cell {
  background-color: #eff6ff;
}

.el-form-item__label {
  font-size: 13px;
  color: #64748b;
}

.el-input__inner,
.el-textarea__inner {
  font-size: 13px;
  border-radius: 6px;
  border-color: #e2e8f0;
  padding: 8px 12px;
}

.el-input__inner:focus,
.el-textarea__inner:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.el-dialog {
  border-radius: 12px;
}

.el-dialog__header {
  border-bottom: 1px solid #f1f5f9;
  padding: 20px 24px;
}

.el-dialog__title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.el-dialog__body {
  padding: 24px;
}

.el-card {
  border-radius: 8px;
  border-color: #e2e8f0;
}

.el-card__header {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.el-card__body {
  padding: 20px;
}

.el-pagination {
  font-size: 13px;
}

.el-tag {
  font-size: 12px;
  border-radius: 4px;
}

.el-descriptions__label,
.el-descriptions__content {
  font-size: 13px;
}

.el-descriptions__label {
  color: #64748b;
}

.el-select .el-input__inner {
  padding-right: 32px;
}

.el-badge__content {
  background-color: #ef4444;
  border-radius: 9999px;
  padding: 0 6px;
  font-size: 11px;
}

@media (max-width: 768px) {
  .el-card {
    overflow-x: auto;
  }
  .el-table {
    min-width: max-content;
  }
  .el-card__body {
    padding: 12px;
  }
  .el-card__header {
    padding: 12px 16px;
  }
  .el-dialog {
    width: 90vw !important;
    max-width: 90vw;
  }
  .el-dialog__body {
    padding: 16px;
  }
  .el-form-item {
    margin-bottom: 14px;
  }
  .el-form-item__label {
    padding-bottom: 4px;
  }
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