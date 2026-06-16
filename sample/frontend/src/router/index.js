import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/orders'
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('../views/OrdersView.vue')
  },
  {
    path: '/orders/create',
    name: 'OrderCreate',
    component: () => import('../views/OrderCreateView.vue')
  },
  {
    path: '/orders/edit/:id',
    name: 'OrderEdit',
    component: () => import('../views/OrderCreateView.vue')
  },
  {
    path: '/todos',
    name: 'Todos',
    component: () => import('../views/TodosView.vue')
  },
  {
    path: '/todos/create',
    name: 'TodoCreate',
    component: () => import('../views/TodoCreateView.vue')
  },
  {
    path: '/todos/edit/:id',
    name: 'TodoEdit',
    component: () => import('../views/TodoCreateView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
