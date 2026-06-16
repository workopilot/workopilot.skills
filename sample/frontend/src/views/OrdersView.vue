<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">订单管理</h1>
        <p class="mt-1 text-sm text-gray-500">管理和跟踪所有订单信息</p>
      </div>
      <router-link to="/orders/create" class="btn btn-primary">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        新建订单
      </router-link>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-4 gap-4">
      <div class="stat-card p-5 group">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-xs font-medium text-gray-500 mb-1">待处理</div>
            <div class="text-2xl font-bold text-yellow-600">{{ stats.pending }}</div>
          </div>
          <div class="icon-box w-12 h-12 from-yellow-500 to-yellow-600 shadow-lg shadow-yellow-500/30 group-hover:scale-110">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="stat-card p-5 group">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-xs font-medium text-gray-500 mb-1">处理中</div>
            <div class="text-2xl font-bold text-blue-600">{{ stats.processing }}</div>
          </div>
          <div class="icon-box w-12 h-12 from-blue-500 to-blue-600 shadow-lg shadow-blue-500/30 group-hover:scale-110">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="stat-card p-5 group">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-xs font-medium text-gray-500 mb-1">已完成</div>
            <div class="text-2xl font-bold text-green-600">{{ stats.completed }}</div>
          </div>
          <div class="icon-box w-12 h-12 from-green-500 to-green-600 shadow-lg shadow-green-500/30 group-hover:scale-110">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="stat-card p-5 group">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-xs font-medium text-gray-500 mb-1">已取消</div>
            <div class="text-2xl font-bold text-red-600">{{ stats.cancelled }}</div>
          </div>
          <div class="icon-box w-12 h-12 from-red-500 to-red-600 shadow-lg shadow-red-500/30 group-hover:scale-110">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="card">
      <div class="card-body">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="flex items-center space-x-2">
              <button
                v-for="status in statusFilters"
                :key="status.value"
                @click="filterStatus = status.value; loadOrders()"
                class="px-3 py-1.5 text-xs font-medium rounded-lg transition-colors"
                :class="filterStatus === status.value
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-100'"
              >
                {{ status.label }}
              </button>
            </div>
          </div>

          <div class="flex items-center space-x-3">
            <input
              v-model="searchKeyword"
              @input="handleSearch"
              type="text"
              placeholder="搜索订单号、客户、产品..."
              class="input input-sm w-64"
            />
            <button @click="loadOrders" class="btn btn-secondary btn-sm">
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              刷新
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 订单表格 -->
    <div class="card">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-3 py-2.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">订单号</th>
              <th class="px-3 py-2.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">客户信息</th>
              <th class="px-3 py-2.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">产品</th>
              <th class="px-3 py-2.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-20">数量</th>
              <th class="px-3 py-2.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-28">单价</th>
              <th class="px-3 py-2.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-28">总价</th>
              <th class="px-3 py-2.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">状态</th>
              <th class="px-3 py-2.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32">创建时间</th>
              <th class="px-3 py-2.5 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-32">操作</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-3 py-2.5 whitespace-nowrap">
                <div class="text-sm font-mono font-medium text-primary-600">{{ order.orderNo }}</div>
              </td>
              <td class="px-3 py-2.5">
                <div class="text-sm font-medium text-gray-900">{{ order.customerName }}</div>
                <div class="text-xs text-gray-500">{{ order.customerPhone }}</div>
              </td>
              <td class="px-3 py-2.5">
                <div class="text-sm text-gray-900">{{ order.productName }}</div>
              </td>
              <td class="px-3 py-2.5 text-right">
                <div class="text-sm text-gray-900">{{ order.quantity }}</div>
              </td>
              <td class="px-3 py-2.5 text-right">
                <div class="text-sm text-gray-900">¥{{ formatMoney(order.unitPrice) }}</div>
              </td>
              <td class="px-3 py-2.5 text-right">
                <div class="text-sm font-medium text-gray-900">¥{{ formatMoney(order.totalPrice) }}</div>
              </td>
              <td class="px-3 py-2.5">
                <span :class="getStatusBadgeClass(order.status)">
                  {{ getStatusText(order.status) }}
                </span>
              </td>
              <td class="px-3 py-2.5 whitespace-nowrap">
                <div class="text-xs text-gray-500">{{ formatDateTime(order.createTime) }}</div>
              </td>
              <td class="px-3 py-2.5 text-right">
                <div class="flex justify-end space-x-1">
                  <router-link :to="`/orders/edit/${order.id}`" class="p-1.5 text-primary-600 hover:bg-primary-50 rounded transition-colors" title="编辑">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </router-link>
                  <button @click="deleteOrder(order)" class="p-1.5 text-red-600 hover:bg-red-50 rounded transition-colors" title="删除">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="orders.length === 0">
              <td colspan="9" class="px-3 py-12 text-center">
                <div class="flex flex-col items-center">
                  <svg class="w-12 h-12 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                  </svg>
                  <div class="text-sm text-gray-500">暂无订单数据</div>
                  <router-link to="/orders/create" class="mt-4 btn btn-primary btn-sm">
                    创建第一个订单
                  </router-link>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { orderApi } from '../api'

const orders = ref([])
const stats = ref({
  total: 0,
  pending: 0,
  processing: 0,
  completed: 0,
  cancelled: 0,
  totalAmount: 0
})

const searchKeyword = ref('')
const filterStatus = ref('')

const statusFilters = [
  { label: '全部', value: '' },
  { label: '待处理', value: 'pending' },
  { label: '处理中', value: 'processing' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'cancelled' }
]

const loadOrders = async () => {
  try {
    const params = {}
    if (searchKeyword.value) params.search = searchKeyword.value
    if (filterStatus.value) params.status = filterStatus.value

    const res = await orderApi.getList(params)
    orders.value = res.data
  } catch (error) {
    console.error('加载订单失败:', error)
  }
}

const loadStats = async () => {
  try {
    const res = await orderApi.getStats()
    stats.value = res.data
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const handleSearch = () => {
  loadOrders()
}

const deleteOrder = async (order) => {
  if (!confirm(`确定要删除订单 ${order.orderNo} 吗？`)) return

  try {
    await orderApi.delete(order.id)
    loadOrders()
    loadStats()
  } catch (error) {
    console.error('删除订单失败:', error)
  }
}

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'badge badge-warning',
    processing: 'badge badge-primary',
    completed: 'badge badge-success',
    cancelled: 'badge badge-gray'
  }
  return classes[status] || 'badge badge-gray'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return texts[status] || status
}

const formatMoney = (value) => {
  if (!value) return '0.00'
  return Number(value).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '/').substring(5, 16)
}

onMounted(() => {
  loadOrders()
  loadStats()
})
</script>
