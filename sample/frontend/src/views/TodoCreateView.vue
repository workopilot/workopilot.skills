<template>
  <div class="max-w-3xl">
    <!-- 页面标题 -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900">{{ isEdit ? '编辑任务' : '新建任务' }}</h1>
      <p class="mt-1 text-sm text-gray-500">{{ isEdit ? '修改任务信息' : '创建一个新的待办任务' }}</p>
    </div>

    <!-- 表单卡片 -->
    <div class="card">
      <div class="card-body">
        <form @submit.prevent="saveTodo" class="space-y-6">
          <!-- 任务基本信息 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">
              任务标题 <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formData.title"
              type="text"
              class="input"
              placeholder="请输入任务标题"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">任务描述</label>
            <textarea
              v-model="formData.description"
              rows="4"
              class="input"
              placeholder="请输入任务描述"
            ></textarea>
          </div>

          <!-- 优先级和截止日期 -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">
                优先级 <span class="text-red-500">*</span>
              </label>
              <select v-model="formData.priority" class="input" required>
                <option value="low">低</option>
                <option value="medium">中</option>
                <option value="high">高</option>
                <option value="urgent">紧急</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1.5">截止日期</label>
              <input
                v-model="formData.dueDate"
                type="date"
                class="input"
              />
            </div>
          </div>

          <!-- 标签 -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">标签</label>
            <input
              v-model="tagsInput"
              type="text"
              class="input"
              placeholder="输入标签，用逗号分隔，如: 工作, 生活, 学习"
            />
            <p class="mt-1.5 text-xs text-gray-500">多个标签用逗号分隔</p>
          </div>

          <!-- 操作按钮 -->
          <div class="flex justify-end space-x-3 pt-4 border-t border-gray-200">
            <router-link to="/todos" class="btn btn-secondary">
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
              {{ loading ? '保存中...' : (isEdit ? '保存修改' : '创建任务') }}
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
import { todoApi } from '../api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => route.name === 'TodoEdit')
const loading = ref(false)
const tagsInput = ref('')

const formData = reactive({
  title: '',
  description: '',
  priority: 'medium',
  dueDate: '',
  tags: []
})

const loadTodo = async () => {
  if (!isEdit.value) return

  try {
    const res = await todoApi.getList()
    const todo = res.data.find(t => t.id === parseInt(route.params.id))
    if (todo) {
      Object.assign(formData, todo)
      tagsInput.value = (todo.tags || []).join(', ')
    }
  } catch (error) {
    console.error('加载任务失败:', error)
    alert('加载任务失败')
    router.push('/todos')
  }
}

const saveTodo = async () => {
  // 处理标签
  formData.tags = tagsInput.value
    .split(',')
    .map(t => t.trim())
    .filter(t => t)

  loading.value = true
  try {
    if (isEdit.value) {
      await todoApi.update(route.params.id, formData)
    } else {
      await todoApi.create(formData)
    }

    router.push('/todos')
  } catch (error) {
    console.error('保存任务失败:', error)
    alert('保存任务失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadTodo()
})
</script>
