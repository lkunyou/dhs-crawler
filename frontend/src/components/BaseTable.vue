<template>
  <div class="base-table">
    <div class="table-scroll-wrapper">
      <el-table
        :data="data"
        :loading="loading"
        :stripe="stripe"
        :border="border"
        :size="size"
        :highlight-current-row="highlightCurrentRow"
        :show-summary="showSummary"
        :summary-method="summaryMethod"
        :max-height="maxHeight"
        ref="tableRef"
        @selection-change="handleSelectionChange"
        @current-change="handleCurrentChange"
        @row-click="handleRowClick"
        class="table-content"
      >
      <template v-if="showSelection">
        <el-table-column type="selection" width="55" fixed="left" />
      </template>

      <el-table-column
        v-for="column in columns"
        :key="column.prop || column.label"
        :prop="column.prop"
        :label="column.label"
        :width="column.width"
        :min-width="column.minWidth"
        :fixed="column.fixed"
        :sortable="column.sortable"
        :align="column.align || 'left'"
        :header-align="column.headerAlign || 'center'"
      >
        <template #default="{ row, $index }">
          <slot :name="'cell-' + (column.prop || column.label)" :row="row" :index="$index">
            <template v-if="column.type === 'tag'">
              <el-tag :type="column.tagType ? (typeof column.tagType === 'function' ? column.tagType(row) : column.tagType) : ''" size="small">
                {{ column.tagLabel ? (typeof column.tagLabel === 'function' ? column.tagLabel(row) : row[column.prop]) : row[column.prop] }}
              </el-tag>
            </template>
            <template v-else-if="column.type === 'link'">
              <el-link :type="column.linkType || 'primary'" @click="() => handleLinkClick(row, column)">
                {{ row[column.prop] }}
              </el-link>
            </template>
            <template v-else-if="column.type === 'button'">
              <el-button
                v-for="btn in column.buttons"
                :key="btn.label"
                :type="btn.type"
                :size="btn.size || 'small'"
                :icon="btn.icon"
                @click="() => btn.handler(row, $index)"
              >
                {{ btn.label }}
              </el-button>
            </template>
            <template v-else-if="column.type === 'custom' && column.render">
              <span
                v-html="column.render(row, $index)"
                :style="column.onClick ? 'cursor:pointer' : ''"
                @click="column.onClick && column.onClick(row, $index)"
              ></span>
            </template>
            <template v-else>
              {{ row[column.prop] }}
            </template>
          </slot>
        </template>
      </el-table-column>
      </el-table>
    </div>

    <template v-if="showPagination && pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="pageSizes"
        :layout="paginationLayout"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        class="pagination"
      />
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  data: { type: Array, default: () => [] },
  columns: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  stripe: { type: Boolean, default: true },
  border: { type: Boolean, default: false },
  size: { type: String, default: 'default' },
  highlightCurrentRow: { type: Boolean, default: false },
  showSelection: { type: Boolean, default: false },
  showPagination: { type: Boolean, default: true },
  showSummary: { type: Boolean, default: false },
  summaryMethod: { type: Function, default: null },
  maxHeight: { type: [String, Number], default: null },
  pagination: { type: Object, default: () => ({ page: 1, size: 20, total: 0 }) },
  pageSizes: { type: Array, default: () => [10, 20, 50, 100] },
  paginationLayout: { type: String, default: 'total, sizes, prev, pager, next' }
})

const emit = defineEmits(['selection-change', 'current-change', 'row-click', 'link-click', 'size-change', 'page-change'])

const tableRef = ref(null)

function handleSelectionChange(rows) {
  emit('selection-change', rows)
}

function handleCurrentChange(currentRow) {
  emit('current-change', currentRow)
}

function handleRowClick(row, column, event) {
  emit('row-click', { row, column, event })
}

function handleLinkClick(row, column) {
  emit('link-click', { row, column })
}

function handleSizeChange(size) {
  emit('size-change', size)
}

function handleCurrentPageChange(page) {
  emit('page-change', page)
}

function getSelectedRows() {
  return tableRef.value?.getSelectionRows?.() || []
}

function clearSelection() {
  tableRef.value?.clearSelection?.()
}

defineExpose({
  tableRef,
  getSelectedRows,
  clearSelection
})
</script>

<style scoped>
.base-table {
  width: 100%;
  display: flex;
  flex-direction: column;
}

.table-scroll-wrapper {
  width: 100%;
  overflow-x: auto;
}

.table-content {
  flex: 1;
  min-width: max-content;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 16px;
  padding: 12px 0;
}
</style>