import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import QuestionBank from '@/views/QuestionBank.vue'
import AIStudy from '@/views/AIStudy.vue'
import Exam from '@/views/Exam.vue'
import MemberCenter from '@/views/MemberCenter.vue'
import TeacherDashboard from '@/views/TeacherDashboard.vue'
import TeacherList from '@/views/TeacherList.vue'
import TeacherDetail from '@/views/TeacherDetail.vue'
import CourseList from '@/views/CourseList.vue'
import CourseDetail from '@/views/CourseDetail.vue'
import Community from '@/views/Community.vue'
import Auth from '@/views/Auth.vue'
import Teachers from '@/views/Teachers.vue'
import AITest from '@/views/AITest.vue'
import Analytics from '@/views/Analytics.vue'
import TestAuth from '@/views/TestAuth.vue'
import LearningPlan from '@/views/LearningPlan.vue'

// 扩展路由元数据类型
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    guestOnly?: boolean
    requiresTeacher?: boolean
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
      meta: { guestOnly: true }
    },
    {
      path: '/auth',
      name: 'auth',
      component: Auth,
      meta: { guestOnly: true }
    },
    {
      path: '/question-bank',
      name: 'question-bank',
      component: QuestionBank,
      meta: { requiresAuth: true }
    },
    {
      path: '/ai-study',
      name: 'ai-study',
      component: AIStudy,
      meta: { requiresAuth: true }
    },
    {
      path: '/exam',
      name: 'exam',
      component: Exam,
      meta: { requiresAuth: true }
    },
    {
      path: '/member-center',
      name: 'member-center',
      component: MemberCenter,
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher-dashboard',
      name: 'teacher-dashboard',
      component: TeacherDashboard,
      meta: { requiresAuth: true, requiresTeacher: true }
    },
    {
      path: '/teacher-list',
      name: 'teacher-list',
      component: TeacherList,
      meta: { requiresAuth: true }
    },
    {
      path: '/teacher-detail/:id',
      name: 'teacher-detail',
      component: TeacherDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/course-list',
      name: 'course-list',
      component: CourseList,
      meta: { requiresAuth: true }
    },
    {
      path: '/course-detail/:id',
      name: 'course-detail',
      component: CourseDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/community',
      name: 'community',
      component: Community,
      meta: { requiresAuth: true }
    },
    {
      path: '/teachers',
      name: 'teachers',
      component: Teachers,
      meta: { requiresAuth: true }
    },
    {
      path: '/ai-study-test',
      name: 'ai-study-test',
      component: AITest,
      meta: { requiresAuth: true }
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: Analytics,
      meta: { requiresAuth: true }
    },
    {
      path: '/test-auth',
      name: 'test-auth',
      component: TestAuth,
      meta: { guestOnly: true }
    },
    {
      path: '/learning-plan',
      name: 'LearningPlan',
      component: LearningPlan,
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
    return
  }
  
  // 检查是否仅限访客（已登录用户不能访问登录/注册页面）
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    next({ name: 'home' })
    return
  }
  
  // 检查教师权限
  if (to.meta.requiresTeacher && authStore.user?.role !== 'teacher') {
    next({ name: 'home' })
    return
  }
  
  next()
})

export default router
