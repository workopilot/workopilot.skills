<template>
  <div class="max-w-4xl">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ isEdit ? '编辑订单' : '新建订单' }}</h1>
      <p class="mt-1 text-sm text-gray-500">{{ isEdit ? '修改订单信息' : '填写订单基本信息' }}</p>
    </div>

    <!-- 表单卡片 -->
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="saveOrder" class="space-y-6">
          <!-- 客户信息 -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">客户信息</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">
                  客户姓名 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.customerName"
                  type="text"
                  class="input"
                  placeholder="请输入客户姓名"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">
                  联系电话 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.customerPhone"
                  type="text"
                  class="input"
                  placeholder="请输入联系电话"
                  required
                />
              </div>
            </div>
          </div>

          <!-- 产品信息 -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">产品信息</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">
                  产品名称 <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="formData.productName"
                  type="text"
                  class="input"
                  placeholder="请输入产品名称"
                  required
                />
              </div>

              <div class="grid grid-cols-3 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">
                    数量 <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model.number="formData.quantity"
                    @input="calculateTotal"
                    type="number"
                    class="input"
                    placeholder="1"
                    min="1"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">
                    单价 (元) <span class="text-red-500">*</span>
                  </label>
                  <input
                    v-model.number="formData.unitPrice"
                    @input="calculateTotal"
                    type="number"
                    step="0.01"
                    class="input"
                    placeholder="0.00"
                    min="0"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1.5">总价 (元)</label>
                  <input
                    v-model.number="formData.totalPrice"
                    type="number"
                    step="0.01"
                    class="input bg-gray-50"
                    placeholder="0.00"
                    readonly
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- 订单详情 -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">订单详情</h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">订单状态</label>
                <select v-model="formData.status" class="input">
                  <option value="pending">待处理</option>
                  <option value="processing">处理中</option>
                  <option value="completed">已完成</option>
                  <option value="cancelled">已取消</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">付款方式</label>
                <select v-model="formData.paymentMethod" class="input">
                  <option value="">请选择</option>
                  <option value="cash">现金</option>
                  <option value="alipay">支付宝</option>
                  <option value="wechat">微信</option>
                  <option value="bank">银行转账</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 收货信息 -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">收货信息</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">收货地址</label>
                <input
                  v-model="formData.deliveryAddress"
                  type="text"
                  class="input"
                  placeholder="请输入收货地址"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5">交付日期</label>
                <input
                  v-model="formData.deliveryDate"
                  type="date"
                  class="input"
                />
              </div>
            </div>
          </div>

          <!-- 备注 -->
          <div>
            <h3 class="text-sm font-semibold text-gray-900 mb-4 pb-2 border-b border-gray-200">其他信息</h3>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">备注</label>
              <textarea
                v-model="formData.remarks"
                rows="4"
                class="input"
                placeholder="请输入备注信息"
              ></textarea>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <router-link to="/orders" class="btn btn-secondary">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              取消
            </router-link>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <svg v-if="!loading" class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              <svg v-else class="w-4 h-4 mr-2 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              {{ loading ? '保存中...' : (isEdit ? '保存修改' : '创建订单') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { orderApi } from '../api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => route.name === 'OrderEdit')
const loading = ref(false)

const formData = reactive({
  customerName: '',
  customerPhone: '',
  productName: '',
  quantity: 1,
  unitPrice: 0,
  totalPrice: 0,
  status: 'pending',
  paymentMethod: '',
  deliveryAddress: '',
  deliveryDate: '',
  remarks: ''
})

const calculateTotal = () => {
  formData.totalPrice = (formData.quantity || 0) * (formData.unitPrice || 0)
}

const loadOrder = async () => {
  if (!isEdit.value) return

  try {
    const res = await orderApi.getDetail(route.params.id)
    Object.assign(formData, res.data)
  } catch (error) {
    console.error('加载订单失败:', error)
    alert('加载订单失败')
    router.push('/orders')
  }
}

const saveOrder = async () => {
  loading.value = true
  try {
    if (isEdit.value) {
      await orderApi.update(route.params.id, formData)
    } else {
      await orderApi.create(formData)
    }

    router.push('/orders')
  } catch (error) {
    console.error('保存订单失败:', error)
    alert('保存订单失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadOrder()
})
</script>
