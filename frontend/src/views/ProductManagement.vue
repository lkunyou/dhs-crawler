<template>
  <div class="product-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>产品管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="createDialogVisible = true">新建产品</el-button>
            <el-button type="success" :disabled="selectedProducts.length === 0" @click="openQuoteDialog">
              生成报价 ({{ selectedProducts.length }})
            </el-button>
            <el-button type="warning" @click="exportProducts">导出</el-button>
            <el-upload
              action=""
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleImport"
              accept=".xlsx,.xls"
              style="display: inline-block"
            >
              <el-button type="info">导入</el-button>
            </el-upload>
          </div>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="产品名称">
          <el-input v-model="searchForm.productName" placeholder="搜索产品名称" style="width: 200px" clearable @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="产品类别">
          <el-select v-model="searchForm.category" style="width: 140px" clearable>
            <el-option label="外观件" value="exterior" />
            <el-option label="刹车系统" value="brake" />
            <el-option label="发动机" value="engine" />
            <el-option label="悬挂系统" value="suspension" />
            <el-option label="电气系统" value="electrical" />
            <el-option label="轮胎" value="tire" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" style="width: 120px" clearable>
            <el-option label="在售" value="active" />
            <el-option label="下架" value="inactive" />
          </el-select>
        </el-form-item>
        <el-form-item label="品牌">
          <el-input v-model="searchForm.brand" placeholder="搜索品牌" style="width: 160px" clearable @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item label="适用车型">
          <el-input v-model="searchForm.carModel" placeholder="搜索车型" style="width: 160px" clearable @keyup.enter="handleSearch" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 统计卡片 -->
      <div class="stats-row">
        <el-card class="stat-card">
          <div class="stat-icon bg-blue">
            <el-icon :size="24"><Box /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">总产品</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-icon bg-green">
            <el-icon :size="24"><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.active }}</div>
            <div class="stat-label">在售</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-icon bg-orange">
            <el-icon :size="24"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.inactive }}</div>
            <div class="stat-label">下架</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-icon bg-purple">
            <el-icon :size="24"><TrendCharts /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ avgPrice }}</div>
            <div class="stat-label">平均价格(USD)</div>
          </div>
        </el-card>
      </div>

      <!-- 产品列表 -->
      <el-table :data="products" border style="margin-top: 20px" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" />
        <el-table-column label="图片" width="80">
          <template #default="{ row }">
            <el-image
              v-if="row.imageUrl"
              :src="row.imageUrl"
              fit="cover"
              style="width: 50px; height: 50px; border-radius: 4px; cursor: pointer;"
              :preview-src-list="[row.imageUrl]"
              :initial-index="0"
            />
            <div v-else style="width: 50px; height: 50px; background: #f5f5f5; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #ccc; font-size: 20px;">
              <el-icon><Picture /></el-icon>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="productName" label="产品名称" min-width="180">
          <template #default="{ row }">
            <el-link type="primary" @click="editProduct(row)">{{ row.productName }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="productCode" label="产品编码" width="140" />
        <el-table-column prop="brand" label="品牌" width="120" />
        <el-table-column prop="category" label="类别" width="100">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ getCategoryLabel(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="model" label="型号" width="120" />
        <el-table-column prop="dimensions" label="尺寸" width="130" />
        <el-table-column prop="carModel" label="适用车型" width="150" />
        <el-table-column prop="unitPrice" label="单价(USD)" width="110">
          <template #default="{ row }">
            {{ row.unitPrice?.toFixed(2) || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'info'" size="small">
              {{ row.status === 'active' ? '在售' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" :type="row.status === 'active' ? 'warning' : 'success'" @click="toggleStatus(row)">
              {{ row.status === 'active' ? '下架' : '上架' }}
            </el-button>
            <el-button size="small" type="danger" @click="deleteProduct(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 创建/编辑产品弹窗 -->
    <el-dialog v-model="createDialogVisible" :title="isEdit ? '编辑产品' : '新建产品'" width="800px">
      <el-form :model="productForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="产品名称" required>
              <el-input v-model="productForm.productName" placeholder="请输入产品名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品编码">
              <el-input v-model="productForm.productCode" placeholder="请输入产品编码" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="产品类别" required>
              <el-select v-model="productForm.category" style="width: 100%">
                <el-option label="外观件" value="exterior" />
                <el-option label="刹车系统" value="brake" />
                <el-option label="发动机" value="engine" />
                <el-option label="悬挂系统" value="suspension" />
                <el-option label="电气系统" value="electrical" />
                <el-option label="轮胎" value="tire" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="品牌">
              <el-input v-model="productForm.brand" placeholder="请输入品牌" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="型号">
              <el-input v-model="productForm.model" placeholder="请输入型号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品尺寸">
              <el-input v-model="productForm.dimensions" placeholder="如: 1215*392*143" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="适用车型">
              <el-input v-model="productForm.carModel" placeholder="请输入适用车型" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="量产日期">
              <el-date-picker v-model="productForm.productionDate" type="date" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="重量(g)">
              <el-input-number v-model="productForm.weight" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="库存">
              <el-input-number v-model="productForm.stock" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="每箱数量">
              <el-input-number v-model="productForm.qtyPerPkg" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="单价(USD)" required>
              <el-input-number v-model="productForm.unitPrice" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="包装尺寸(mm)">
              <el-row :gutter="8">
                <el-col :span="4">
                  <el-input-number v-model="productForm.pkgLength" :min="0" placeholder="长" style="width: 100%" />
                </el-col>
                <el-col :span="4">
                  <el-input-number v-model="productForm.pkgWidth" :min="0" placeholder="宽" style="width: 100%" />
                </el-col>
                <el-col :span="4">
                  <el-input-number v-model="productForm.pkgHeight" :min="0" placeholder="高" style="width: 100%" />
                </el-col>
              </el-row>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="产品图片">
          <div class="image-upload-wrapper">
            <el-upload
              action=""
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleImageUpload"
              accept="image/*"
            >
              <el-button type="primary" size="small">选择图片</el-button>
            </el-upload>
            <div v-if="productForm.imageUrl" class="image-preview">
              <el-image
                :src="productForm.imageUrl"
                fit="cover"
                style="width: 100px; height: 100px; border-radius: 4px; border: 1px solid #ddd;"
                :preview-src-list="[productForm.imageUrl]"
              />
              <el-button type="danger" size="small" link @click="productForm.imageUrl = ''" style="margin-left: 8px;">删除</el-button>
            </div>
          </div>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="productForm.description" type="textarea" :rows="3" placeholder="请输入产品描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProduct">{{ isEdit ? '保存修改' : '创建产品' }}</el-button>
      </template>
    </el-dialog>

    <!-- 生成报价弹窗 -->
    <el-dialog v-model="quoteDialogVisible" title="生成报价单" width="960px">
      <el-form label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户名称" required>
              <el-select v-model="quoteForm.companyId" style="width: 100%" placeholder="选择客户" filterable>
                <el-option v-for="opt in companyOptions" :key="opt.value" :label="opt.label" :value="opt.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报价编号">
              <el-input v-model="quoteForm.quoteNo" disabled placeholder="自动生成" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="有效期">
              <el-date-picker v-model="quoteForm.validDate" type="date" placeholder="选择有效期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总金额">
              <el-input :model-value="quoteTotal" disabled style="width: 100%">
                <template #prefix>USD</template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 产品明细 -->
        <el-form-item label="产品明细" required>
          <el-table :data="quoteForm.items" border size="small" style="width: 100%">
            <el-table-column label="产品名称" min-width="180">
              <template #default="{ $index }">
                <el-select
                  v-model="quoteForm.items[$index].productId"
                  filterable
                  remote
                  clearable
                  placeholder="搜索产品"
                  :remote-method="searchProducts"
                  style="width: 100%"
                  @change="(val) => handleProductChange($index, val)"
                >
                  <el-option
                    v-for="p in productOptions"
                    :key="p.id"
                    :label="p.name + (p.code ? ' (' + p.code + ')' : '')"
                    :value="p.id"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="产品型号" min-width="120">
              <template #default="{ $index }">
                <el-input v-model="quoteForm.items[$index].productModel" placeholder="型号" />
              </template>
            </el-table-column>
            <el-table-column label="数量" width="90">
              <template #default="{ $index }">
                <el-input
                  v-model.number="quoteForm.items[$index].quantity"
                  placeholder="10"
                  style="width: 100%"
                />
              </template>
            </el-table-column>
            <el-table-column label="单价(USD)" width="120">
              <template #default="{ $index }">
                <el-input
                  v-model="quoteForm.items[$index].unitPrice"
                  placeholder="单价"
                  style="width: 100%"
                  @input="(val) => { quoteForm.items[$index].unitPrice = parseFloat(val) || 0 }"
                />
              </template>
            </el-table-column>
            <el-table-column label="小计" width="100">
              <template #default="{ row }">
                {{ (row.quantity * row.unitPrice).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="70">
              <template #default="{ $index }">
                <el-button size="small" type="danger" link @click="removeItem($index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 8px">
            <el-button type="primary" link @click="addItem">
              <el-icon><Plus /></el-icon> 添加产品
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="备注">
          <el-input v-model="quoteForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="quoteDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="quoteLoading" @click="saveQuoteFromProducts">创建报价</el-button>
      </template>
    </el-dialog>

    <!-- 产品详情弹窗 -->
    <el-dialog v-model="viewDialogVisible" title="产品详情" width="800px">
      <div v-if="viewProductData" class="product-detail">
        <div v-if="viewProductData.imageUrl" style="margin-bottom: 20px; text-align: center;">
          <el-image
            :src="viewProductData.imageUrl"
            fit="contain"
            style="max-width: 400px; max-height: 300px; border-radius: 8px; border: 1px solid #ddd;"
            :preview-src-list="[viewProductData.imageUrl]"
          />
        </div>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="产品名称">{{ viewProductData.productName }}</el-descriptions-item>
          <el-descriptions-item label="产品编码">{{ viewProductData.productCode || '-' }}</el-descriptions-item>
          <el-descriptions-item label="类别">
            <el-tag type="info" size="small">{{ getCategoryLabel(viewProductData.category) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="品牌">{{ viewProductData.brand || '-' }}</el-descriptions-item>
          <el-descriptions-item label="型号">{{ viewProductData.model || '-' }}</el-descriptions-item>
          <el-descriptions-item label="产品尺寸">{{ viewProductData.dimensions || '-' }}</el-descriptions-item>
          <el-descriptions-item label="适用车型">{{ viewProductData.carModel || '-' }}</el-descriptions-item>
          <el-descriptions-item label="量产日期">{{ viewProductData.productionDate || '-' }}</el-descriptions-item>
          <el-descriptions-item label="重量">{{ viewProductData.weight ? viewProductData.weight + 'g' : '-' }}</el-descriptions-item>
          <el-descriptions-item label="库存">{{ viewProductData.stock || 0 }}</el-descriptions-item>
          <el-descriptions-item label="每箱数量">{{ viewProductData.qtyPerPkg ? viewProductData.qtyPerPkg + '件' : '-' }}</el-descriptions-item>
          <el-descriptions-item label="单价(USD)">{{ viewProductData.unitPrice?.toFixed(2) || '-' }}</el-descriptions-item>
          <el-descriptions-item label="包装尺寸">
            {{ viewProductData.pkgLength && viewProductData.pkgWidth && viewProductData.pkgHeight ? 
               `${viewProductData.pkgLength}x${viewProductData.pkgWidth}x${viewProductData.pkgHeight}mm` : '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="viewProductData.status === 'active' ? 'success' : 'info'" size="small">
              {{ viewProductData.status === 'active' ? '在售' : '下架' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(viewProductData.createdAt) }}</el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">{{ viewProductData.description || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 导入预览弹窗 -->
    <el-dialog v-model="importPreviewVisible" title="导入预览" width="900px" :close-on-click-modal="false" :before-close="cancelImport">
      <div style="margin-bottom: 12px;">共解析到 <b>{{ importPreviewTotal }}</b> 条数据，确认后导入正式表</div>
      <el-table :data="importPreviewList" height="400" border>
        <el-table-column prop="productName" label="产品名称" min-width="120" />
        <el-table-column prop="productCode" label="产品编码" min-width="120" />
        <el-table-column prop="category" label="分类" width="100" />
        <el-table-column prop="brand" label="品牌" width="100" />
        <el-table-column prop="model" label="型号" width="100" />
        <el-table-column prop="carModel" label="适用车型" width="120" />
        <el-table-column prop="unitPrice" label="单价" width="100" />
        <el-table-column prop="stock" label="库存" width="80" />
        <el-table-column prop="status" label="状态" width="80" />
      </el-table>
      <template #footer>
        <el-button @click="cancelImport">取消</el-button>
        <el-button type="primary" :loading="importLoading" @click="confirmImport">确认导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Box, Check, Warning, TrendCharts, Picture } from '@element-plus/icons-vue'
import { getProducts, createProduct, updateProduct, deleteProduct as deleteProductApi } from '@/api/product'
import { getCompanies } from '@/api/company'
import { createQuote } from '@/api/quote'
import request from '@/utils/request'
import { Plus } from '@element-plus/icons-vue'

const products = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)
const createDialogVisible = ref(false)
const viewDialogVisible = ref(false)
const isEdit = ref(false)
const viewProductData = ref(null)
const selectedProducts = ref([])
const quoteDialogVisible = ref(false)
const companyOptions = ref([])
const quoteLoading = ref(false)
const productOptions = ref([])
const importPreviewVisible = ref(false)
const importPreviewList = ref([])
const importPreviewTotal = ref(0)
const importTempId = ref('')
const importLoading = ref(false)

const quoteForm = reactive({
  companyId: null,
  quoteNo: '',
  validDate: '',
  remark: '',
  items: []
})

const quoteTotal = computed(() => {
  if (!quoteForm.items || quoteForm.items.length === 0) return '0.00'
  const total = quoteForm.items.reduce((sum, item) => {
    const qty = parseInt(item.quantity) || 0
    const price = parseFloat(item.unitPrice) || 0
    return sum + qty * price
  }, 0)
  return total.toFixed(2)
})

const searchForm = reactive({
  productName: '',
  category: '',
  status: '',
  brand: '',
  carModel: ''
})

const productForm = reactive({
  id: null,
  productName: '',
  productCode: '',
  category: '',
  brand: '',
  specification: '',
  unitPrice: 0,
  stock: 0,
  description: '',
  status: 'active',
  model: '',
  dimensions: '',
  pkgLength: null,
  pkgWidth: null,
  pkgHeight: null,
  qtyPerPkg: null,
  carModel: '',
  productionDate: '',
  weight: null,
  imageUrl: ''
})

const stats = computed(() => ({
  total: products.value.length,
  active: products.value.filter(p => p.status === 'active').length,
  inactive: products.value.filter(p => p.status === 'inactive').length
}))

const avgPrice = computed(() => {
  const prices = products.value.filter(p => p.unitPrice).map(p => p.unitPrice)
  if (prices.length === 0) return '0.00'
  return (prices.reduce((a, b) => a + b, 0) / prices.length).toFixed(2)
})

onMounted(() => {
  loadProducts()
})

async function loadProducts() {
  loading.value = true
  try {
    const res = await getProducts({
      page: currentPage.value,
      size: pageSize.value,
      productName: searchForm.productName,
      category: searchForm.category,
      status: searchForm.status,
      brand: searchForm.brand,
      carModel: searchForm.carModel
    })
    products.value = res.data?.records || res.data || []
    total.value = res.data?.total || products.value.length
  } catch (e) {
    console.error(e)
    ElMessage.error('加载产品失败')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  currentPage.value = 1
  loadProducts()
}

function handleReset() {
  searchForm.productName = ''
  searchForm.category = ''
  searchForm.status = ''
  searchForm.brand = ''
  searchForm.carModel = ''
  currentPage.value = 1
  loadProducts()
}

function handleSizeChange(size) {
  pageSize.value = size
  currentPage.value = 1
  loadProducts()
}

function handlePageChange(page) {
  currentPage.value = page
  loadProducts()
}

function viewProduct(row) {
  viewProductData.value = row
  viewDialogVisible.value = true
}

function editProduct(row) {
  isEdit.value = true
  Object.assign(productForm, {
    id: row.id,
    productName: row.productName,
    productCode: row.productCode,
    category: row.category,
    brand: row.brand,
    specification: row.specification,
    unitPrice: row.unitPrice,
    stock: row.stock,
    description: row.description,
    status: row.status,
    model: row.model,
    dimensions: row.dimensions,
    pkgLength: row.pkgLength,
    pkgWidth: row.pkgWidth,
    pkgHeight: row.pkgHeight,
    qtyPerPkg: row.qtyPerPkg,
    carModel: row.carModel,
    productionDate: row.productionDate,
    weight: row.weight,
    imageUrl: row.imageUrl
  })
  createDialogVisible.value = true
}

async function saveProduct() {
  if (!productForm.productName) {
    ElMessage.warning('请输入产品名称')
    return
  }
  if (!productForm.category) {
    ElMessage.warning('请选择产品类别')
    return
  }
  if (!productForm.unitPrice || productForm.unitPrice < 0) {
    ElMessage.warning('请输入有效单价')
    return
  }

  try {
    if (isEdit.value) {
      await updateProduct(productForm.id, productForm)
      ElMessage.success('产品已更新')
    } else {
      await createProduct(productForm)
      ElMessage.success('产品已创建')
    }
    createDialogVisible.value = false
    loadProducts()
    resetForm()
  } catch (e) {
    console.error(e)
    ElMessage.error('保存失败')
  }
}

async function toggleStatus(row) {
  const newStatus = row.status === 'active' ? 'inactive' : 'active'
  try {
    await updateProduct(row.id, { status: newStatus })
    ElMessage.success(newStatus === 'active' ? '产品已上架' : '产品已下架')
    loadProducts()
  } catch (e) {
    console.error(e)
    ElMessage.error('操作失败')
  }
}

async function deleteProduct(row) {
  await ElMessageBox.confirm('确定要删除该产品吗？', '确认删除', { type: 'warning' })
  try {
    await deleteProductApi(row.id)
    ElMessage.success('已删除')
    loadProducts()
  } catch (e) {
    console.error(e)
    ElMessage.error('删除失败')
  }
}

function resetForm() {
  isEdit.value = false
  Object.assign(productForm, {
    id: null,
    productName: '',
    productCode: '',
    category: '',
    brand: '',
    specification: '',
    unitPrice: 0,
    stock: 0,
    description: '',
    status: 'active',
    model: '',
    dimensions: '',
    pkgLength: null,
    pkgWidth: null,
    pkgHeight: null,
    qtyPerPkg: null,
    carModel: '',
    productionDate: '',
    weight: null,
    imageUrl: ''
  })
}

function getCategoryLabel(category) {
  switch (category) {
    case 'exterior': return '外观件'
    case 'brake': return '刹车系统'
    case 'engine': return '发动机'
    case 'suspension': return '悬挂系统'
    case 'electrical': return '电气系统'
    case 'tire': return '轮胎'
    case 'other': return '其他'
    default: return '未知'
  }
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

async function handleImageUpload(file) {
  const formData = new FormData()
  formData.append('file', file.raw)
  try {
    const res = await request.post('/products/upload-image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    if (res.data) {
      productForm.imageUrl = res.data
      ElMessage.success('图片上传成功')
    }
  } catch (e) {
    console.error(e)
    ElMessage.error('图片上传失败')
  }
  return false
}

function handleSelectionChange(selection) {
  selectedProducts.value = selection
}

async function openQuoteDialog() {
  quoteForm.companyId = null
  quoteForm.quoteNo = ''
  quoteForm.validDate = ''
  quoteForm.remark = ''
  quoteForm.items = selectedProducts.value.map(p => ({
    productId: p.id,
    productName: p.productName,
    productModel: p.model || '',
    quantity: 1,
    unitPrice: p.unitPrice || 0
  }))
  // 预填充产品选项，确保 el-select 能正确显示已选产品名称
  productOptions.value = selectedProducts.value.map(p => ({
    id: p.id,
    name: p.productName,
    code: p.productCode,
    model: p.model,
    unitPrice: p.unitPrice
  }))
  quoteDialogVisible.value = true
  try {
    const res = await getCompanies({ page: 1, size: 100 })
    companyOptions.value = (res.data?.records || []).map(c => ({ label: c.companyName, value: c.id }))
  } catch (e) {
    console.error(e)
  }
}

async function searchProducts(query) {
  if (!query || query.length < 1) {
    productOptions.value = []
    return
  }
  try {
    const res = await getProducts({ page: 1, size: 20, productName: query, productCode: query })
    productOptions.value = (res.data?.records || res.data || []).map(p => ({
      id: p.id,
      name: p.productName,
      code: p.productCode,
      model: p.model,
      unitPrice: p.unitPrice
    }))
  } catch (e) {
    console.error(e)
  }
}

function handleProductChange(index, productId) {
  const product = productOptions.value.find(p => p.id === productId)
  if (product) {
    quoteForm.items[index].productName = product.name
    quoteForm.items[index].productModel = product.model || ''
    quoteForm.items[index].unitPrice = product.unitPrice || 0
  }
}

function addItem() {
  quoteForm.items.push({
    productId: null,
    productName: '',
    productModel: '',
    quantity: 1,
    unitPrice: 0
  })
}

function removeItem(index) {
  quoteForm.items.splice(index, 1)
}

async function saveQuoteFromProducts() {
  if (!quoteForm.companyId) {
    ElMessage.warning('请选择客户')
    return
  }
  if (!quoteForm.items || quoteForm.items.length === 0) {
    ElMessage.warning('请至少添加一个产品')
    return
  }
  quoteLoading.value = true
  try {
    await createQuote({
      companyId: quoteForm.companyId,
      validDate: quoteForm.validDate,
      remark: quoteForm.remark,
      items: quoteForm.items.map(item => ({
        productId: item.productId,
        productName: item.productName,
        productModel: item.productModel || '',
        quantity: parseInt(item.quantity) || 1,
        unitPrice: parseFloat(item.unitPrice) || 0
      }))
    })
    ElMessage.success('报价单已生成')
    quoteDialogVisible.value = false
    selectedProducts.value = []
  } catch (e) {
    console.error(e)
    ElMessage.error('生成报价失败')
  } finally {
    quoteLoading.value = false
  }
}

async function exportProducts() {
  try {
    const res = await request.get('/products/export', { responseType: 'blob' })
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '产品列表.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error('导出失败')
  }
}

async function handleImport(file) {
  const formData = new FormData()
  formData.append('file', file.raw)
  try {
    const res = await request.post('/products/import-preview', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    if (res.data) {
      importTempId.value = res.data.tempId || ''
      importPreviewList.value = res.data.list || []
      importPreviewTotal.value = res.data.total || 0
      importPreviewVisible.value = true
    }
  } catch (e) {
    ElMessage.error('预览解析失败')
  }
}

async function confirmImport() {
  if (!importTempId.value) return
  importLoading.value = true
  try {
    await request.post('/products/import-confirm', null, { params: { tempId: importTempId.value } })
    ElMessage.success('导入成功')
    importPreviewVisible.value = false
    loadProducts()
  } catch (e) {
    ElMessage.error('导入失败')
  } finally {
    importLoading.value = false
  }
}

async function cancelImport() {
  if (importTempId.value) {
    try {
      await request.post('/products/import-cancel', null, { params: { tempId: importTempId.value } })
    } catch (e) {}
  }
  importPreviewVisible.value = false
  importTempId.value = ''
  importPreviewList.value = []
  importPreviewTotal.value = 0
}
</script>

<style scoped>
.product-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.search-form {
  margin-bottom: 20px;
}

.stats-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-icon.bg-blue {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
}

.stat-icon.bg-green {
  background: linear-gradient(135deg, #16a34a, #22c55e);
}

.stat-icon.bg-orange {
  background: linear-gradient(135deg, #d97706, #f59e0b);
}

.stat-icon.bg-purple {
  background: linear-gradient(135deg, #7c3aed, #a855f7);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #1e293b;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.product-detail {
  padding: 10px;
}

.image-upload-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 16px;
}

.image-preview {
  display: flex;
  align-items: center;
}
</style>