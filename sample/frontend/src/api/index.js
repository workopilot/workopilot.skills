import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// ============== 订单 API ==============

export const orderApi = {
  // 获取订单列表
  getList(params) {
    return api.get('/orders', { params })
  },

  // 获取单个订单
  getDetail(id) {
    return api.get(`/orders/${id}`)
  },

  // 创建订单
  create(data) {
    return api.post('/orders', data)
  },

  // 更新订单
  update(id, data) {
    return api.put(`/orders/${id}`, data)
  },

  // 删除订单
  delete(id) {
    return api.delete(`/orders/${id}`)
  },

  // 获取统计
  getStats() {
    return api.get('/orders/stats')
  }
}

// ============== Todo API ==============

export const todoApi = {
  // 获取待办列表
  getList(params) {
    return api.get('/todos', { params })
  },

  // 创建待办
  create(data) {
    return api.post('/todos', data)
  },

  // 更新待办
  update(id, data) {
    return api.put(`/todos/${id}`, data)
  },

  // 删除待办
  delete(id) {
    return api.delete(`/todos/${id}`)
  },

  // 切换完成状态
  toggle(id) {
    return api.post(`/todos/${id}/toggle`)
  },

  // 获取统计
  getStats() {
    return api.get('/todos/stats')
  }
}

export default api
