import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Exam from "@/views/Exam.vue";
import { useAuthStore } from "../stores/auth";
import Register from "@/views/Register.vue";
import QuestionBank from "@/views/QuestionBank.vue";
import AIStudy from "@/views/AIStudy.vue";
import MemberCenter from "@/views/MemberCenter.vue";
import TeacherDashboard from "@/views/TeacherDashboard.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
      meta: { requiresAuth: true },
    },
    {
      path: "/login",
      name: "login",
      component: Login,
      meta: { guestOnly: true },
    },
    {
      path: "/register",
      name: "register",
      component: Register,
      meta: { guestOnly: true },
    },
    {
      path: "/questions",
      name: "questions",
      component: QuestionBank,
      meta: { requiresAuth: true },
    },
    {
      path: "/exam/:id",
      name: "exam",
      component: Exam,
      meta: { requiresAuth: true },
    },
    {
      path: "/ai-study",
      name: "ai-study",
      component: AIStudy,
      meta: { requiresAuth: true },
    },
    {
      path: "/member-center",
      name: "member-center",
      component: MemberCenter,
      meta: { requiresAuth: true },
    },
    {
      path: "/teacher-dashboard",
      name: "teacher-dashboard",
      component: TeacherDashboard,
      meta: { requiresAuth: true, requiresTeacher: true },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // 检查是否需要认证
  if (to.meta.requiresAuth && !authStore.isAuthenticated()) {
    next({ name: "login" });
    return;
  }

  // 检查是否仅限访客
  if (to.meta.guestOnly && authStore.isAuthenticated()) {
    next({ name: "home" });
    return;
  }

  // 检查教师权限
  if (to.meta.requiresTeacher && authStore.user?.role !== "teacher") {
    next({ name: "home" });
    return;
  }

  next();
});

export default router;
