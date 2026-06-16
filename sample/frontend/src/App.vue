<template>
  <div class="flex h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-purple-50/20 overflow-hidden">
    <!-- 左侧边栏 - 现代化设计 -->
    <aside class="w-64 bg-white/70 backdrop-blur-xl border-r border-gray-200/50 flex flex-col shadow-xl">
      <!-- Logo 区域 - 渐变设计 -->
      <div class="h-16 flex items-center px-5 border-b border-gray-200/50 bg-gradient-to-r from-primary-50/50 to-purple-50/50">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-gradient-to-br from-primary-500 via-primary-600 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-primary-500/30 transform transition-transform hover:scale-110">
            <span class="text-white font-bold text-base">WK</span>
          </div>
          <div>
            <div class="text-sm font-bold bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">喔壳 Skills</div>
            <div class="text-xs text-gray-500">Demo System</div>
          </div>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="flex-1 overflow-y-auto py-5 px-3">
        <div class="space-y-1.5">
          <!-- 订单管理 -->
          <router-link
            to="/orders"
            class="menu-item flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-300"
            :class="$route.path.startsWith('/orders')
              ? 'active bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg shadow-primary-500/30'
              : 'text-gray-700 hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100'"
          >
            <div class="icon-box w-8 h-8 mr-3" :class="$route.path.startsWith('/orders') ? 'from-white/20 to-white/10' : 'from-primary-100 to-primary-200'">
              <svg class="w-4 h-4" :class="$route.path.startsWith('/orders') ? 'text-white' : 'text-primary-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </div>
            <span>订单管理</span>
          </router-link>

          <!-- Todo 清单 -->
          <router-link
            to="/todos"
            class="menu-item flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-300"
            :class="$route.path.startsWith('/todos')
              ? 'active bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg shadow-primary-500/30'
              : 'text-gray-700 hover:bg-gradient-to-r hover:from-gray-50 hover:to-gray-100'"
          >
            <div class="icon-box w-8 h-8 mr-3" :class="$route.path.startsWith('/todos') ? 'from-white/20 to-white/10' : 'from-green-100 to-green-200'">
              <svg class="w-4 h-4" :class="$route.path.startsWith('/todos') ? 'text-white' : 'text-green-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
              </svg>
            </div>
            <span>Todo 清单</span>
          </router-link>
        </div>
      </nav>

      <!-- 底部用户信息 - 渐变卡片 -->
      <div class="border-t border-gray-200/50 p-4 bg-gradient-to-r from-gray-50/50 to-blue-50/50">
        <div class="flex items-center p-3 rounded-xl bg-white/50 backdrop-blur-sm border border-gray-200/50 shadow-sm hover:shadow-md transition-all">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-400 via-pink-500 to-red-500 flex items-center justify-center flex-shrink-0 shadow-lg">
            <span class="text-white text-sm font-medium">演</span>
          </div>
          <div class="ml-3 flex-1 min-w-0">
            <div class="text-sm font-semibold text-gray-900 truncate">演示系统</div>
            <div class="text-xs text-gray-500 truncate">Demo Mode</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 右侧主内容区 -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- 顶部导航栏 - 玻璃态设计 -->
      <header class="h-16 bg-white/70 backdrop-blur-xl border-b border-gray-200/50 flex items-center justify-between px-8 shadow-sm">
        <div class="flex items-center">
          <!-- 面包屑导航 -->
          <nav class="flex items-center space-x-2 text-sm">
            <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
            </svg>
            <span class="text-gray-400">/</span>
            <span class="font-medium text-gray-700">{{ getBreadcrumb() }}</span>
          </nav>
        </div>

        <!-- 右侧信息 -->
        <div class="flex items-center space-x-4">
          <div class="text-xs text-gray-500 bg-gray-50 px-3 py-2 rounded-lg border border-gray-200">
            {{ currentTime }}
          </div>
          <button class="p-2.5 text-gray-400 hover:text-gray-600 rounded-xl hover:bg-gray-50 transition-all relative group">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
            </svg>
            <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full animate-ping"></span>
            <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
        </div>
      </header>

      <!-- 主内容滚动区域 -->
      <main class="flex-1 overflow-auto p-8">
        <div class="fade-in">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const currentTime = ref('')

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

const getBreadcrumb = () => {
  const path = route.path
  if (path.startsWith('/orders/create')) return '订单管理 / 新建订单'
  if (path.startsWith('/orders/edit')) return '订单管理 / 编辑订单'
  if (path.startsWith('/orders')) return '订单管理 / 订单列表'
  if (path.startsWith('/todos/create')) return 'Todo 清单 / 新建任务'
  if (path.startsWith('/todos/edit')) return 'Todo 清单 / 编辑任务'
  if (path.startsWith('/todos')) return 'Todo 清单 / 任务列表'
  return '首页'
}

let timer
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>
