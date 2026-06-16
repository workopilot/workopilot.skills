<template>
  <div class="space-y-6">
    <!-- 页面标题 -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Todo 清单</h1>
        <p class="mt-1 text-sm text-gray-500">管理和跟踪所有待办任务</p>
      </div>
      <router-link to="/todos/create" class="btn btn-primary">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        新建任务
      </router-link>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-6 gap-4">
      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-xs text-gray-500 mb-1">总任务</div>
              <div class="text-2xl font-bold text-gray-900">{{ stats.total }}</div>
            </div>
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-xs text-gray-500 mb-1">进行中</div>
              <div class="text-2xl font-bold text-blue-600">{{ stats.active }}</div>
            </div>
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-xs text-gray-500 mb-1">已完成</div>
              <div class="text-2xl font-bold text-green-600">{{ stats.completed }}</div>
            </div>
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-xs text-gray-500 mb-1">紧急</div>
              <div class="text-2xl font-bold text-red-600">{{ stats.urgent }}</div>
            </div>
            <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-xs text-gray-500 mb-1">高优先级</div>
              <div class="text-2xl font-bold text-orange-600">{{ stats.high }}</div>
            </div>
            <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-body">
          <div class="flex items-center justify-between">
            <div>
              <div class="text-xs text-gray-500 mb-1">已逾期</div>
              <div class="text-2xl font-bold text-purple-600">{{ stats.overdue }}</div>
            </div>
            <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="card">
      <div class="card-body">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <button @click="showCreateModal = true" class="btn btn-primary btn-sm">
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              新建任务
            </button>

            <div class="flex items-center space-x-2">
              <button
                v-for="filter in statusFilters"
                :key="filter.value"
                @click="filterStatus = filter.value"
                class="px-3 py-1.5 text-xs font-medium rounded-lg transition-colors"
                :class="filterStatus === filter.value
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-100'"
              >
                {{ filter.label }}
              </button>
            </div>

            <div class="h-5 w-px bg-gray-300"></div>

            <div class="flex items-center space-x-2">
              <button
                v-for="filter in priorityFilters"
                :key="filter.value"
                @click="filterPriority = filter.value"
                class="px-3 py-1.5 text-xs font-medium rounded-lg transition-colors"
                :class="filterPriority === filter.value
                  ? 'bg-primary-100 text-primary-700'
                  : 'text-gray-600 hover:bg-gray-100'"
              >
                {{ filter.label }}
              </button>
            </div>
          </div>

          <button @click="loadTodos" class="btn btn-secondary btn-sm">
            <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            刷新
          </button>
        </div>
      </div>
    </div>

    <!-- Todo 列表 -->
    <div class="grid grid-cols-1 gap-3">
      <div
        v-for="todo in todos"
        :key="todo.id"
        class="card hover:shadow-md transition-shadow"
      >
        <div class="card-body">
          <div class="flex items-start space-x-3">
            <!-- 复选框 -->
            <button
              @click="toggleTodo(todo)"
              class="mt-0.5 flex-shrink-0 w-5 h-5 rounded border-2 transition-all flex items-center justify-center"
              :class="todo.completed
                ? 'bg-green-500 border-green-500'
                : 'border-gray-300 hover:border-primary-500'"
            >
              <svg v-if="todo.completed" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7"/>
              </svg>
            </button>

            <!-- 内容区 -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-2 mb-1">
                    <h4
                      class="text-sm font-medium transition-all"
                      :class="todo.completed
                        ? 'line-through text-gray-400'
                        : 'text-gray-900'"
                    >
                      {{ todo.title }}
                    </h4>
                    <span :class="getPriorityBadgeClass(todo.priority)">
                      {{ getPriorityText(todo.priority) }}
                    </span>
                    <span
                      v-if="isOverdue(todo)"
                      class="badge badge-danger text-xs"
                    >
                      已逾期
                    </span>
                  </div>

                  <p
                    v-if="todo.description"
                    class="text-xs mb-2 transition-all"
                    :class="todo.completed ? 'text-gray-400' : 'text-gray-600'"
                  >
                    {{ todo.description }}
                  </p>

                  <div class="flex items-center space-x-3 text-xs text-gray-500">
                    <div v-if="todo.dueDate" class="flex items-center">
                      <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                      </svg>
                      截止: {{ todo.dueDate }}
                    </div>
                    <div class="flex items-center">
                      <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      创建: {{ formatDateTime(todo.createTime) }}
                    </div>
                    <div v-if="todo.completedTime" class="flex items-center">
                      <svg class="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                      </svg>
                      完成: {{ formatDateTime(todo.completedTime) }}
                    </div>
                  </div>

                  <div v-if="todo.tags && todo.tags.length" class="flex flex-wrap gap-1.5 mt-2">
                    <span
                      v-for="tag in todo.tags"
                      :key="tag"
                      class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-700"
                    >
                      #{{ tag }}
                    </span>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="flex space-x-1 ml-3">
                  <router-link :to="`/todos/edit/${todo.id}`" class="p-1.5 text-primary-600 hover:bg-primary-50 rounded transition-colors" title="编辑">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </router-link>
                  <button @click="deleteTodo(todo)" class="p-1.5 text-red-600 hover:bg-red-50 rounded transition-colors" title="删除">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="todos.length === 0" class="card">
        <div class="card-body py-12">
          <div class="flex flex-col items-center">
            <svg class="w-12 h-12 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
            <div class="text-sm text-gray-500">暂无待办任务</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { todoApi } from '../api'

const todos = ref([])
const stats = ref({
  total: 0,
  active: 0,
  completed: 0,
  urgent: 0,
  high: 0,
  overdue: 0
})

const filterStatus = ref('')
const filterPriority = ref('')

const statusFilters = [
  { label: '全部', value: '' },
  { label: '进行中', value: 'active' },
  { label: '已完成', value: 'completed' }
]

const priorityFilters = [
  { label: '全部', value: '' },
  { label: '低', value: 'low' },
  { label: '中', value: 'medium' },
  { label: '高', value: 'high' },
  { label: '紧急', value: 'urgent' }
]

const loadTodos = async () => {
  try {
    const params = {}
    if (filterStatus.value) params.status = filterStatus.value
    if (filterPriority.value) params.priority = filterPriority.value

    const res = await todoApi.getList(params)
    todos.value = res.data
  } catch (error) {
    console.error('加载待办失败:', error)
  }
}

const loadStats = async () => {
  try {
    const res = await todoApi.getStats()
    stats.value = res.data
  } catch (error) {
    console.error('加载统计失败:', error)
  }
}

const resetForm = () => {
  // 已移除，不再需要
}

const editTodo = (todo) => {
  // 已移除，改用路由跳转
}

const saveTodo = async () => {
  // 已移除，改用独立页面
}

const toggleTodo = async (todo) => {
  try {
    await todoApi.toggle(todo.id)
    loadTodos()
    loadStats()
  } catch (error) {
    console.error('切换状态失败:', error)
  }
}

const deleteTodo = async (todo) => {
  if (!confirm(`确定要删除任务"${todo.title}"吗？`)) return

  try {
    await todoApi.delete(todo.id)
    loadTodos()
    loadStats()
  } catch (error) {
    console.error('删除待办失败:', error)
  }
}

const getPriorityBadgeClass = (priority) => {
  const classes = {
    low: 'badge badge-gray',
    medium: 'badge badge-primary',
    high: 'badge badge-warning',
    urgent: 'badge badge-danger'
  }
  return classes[priority] || 'badge badge-gray'
}

const getPriorityText = (priority) => {
  const texts = {
    low: '低',
    medium: '中',
    high: '高',
    urgent: '紧急'
  }
  return texts[priority] || priority
}

const isOverdue = (todo) => {
  if (!todo.dueDate || todo.completed) return false
  return new Date(todo.dueDate) < new Date()
}

const formatDateTime = (dateStr) => {
  if (!dateStr) return ''
  return dateStr.replace(/-/g, '/').substring(5, 16)
}

onMounted(() => {
  loadTodos()
  loadStats()
})
</script>
