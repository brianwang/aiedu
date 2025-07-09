import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import Auth from "@/views/Auth.vue";
import QuestionBank from "@/views/QuestionBank.vue";
import Exam from "@/views/Exam.vue";
import MemberCenter from "@/views/MemberCenter.vue";
import Teachers from "@/views/Teachers.vue";
import TeacherList from "@/views/TeacherList.vue";
import TeacherDetail from "@/views/TeacherDetail.vue";
import TeacherDashboard from "@/views/TeacherDashboard.vue";
import CourseList from "@/views/CourseList.vue";
import CourseDetail from "@/views/CourseDetail.vue";
import Community from "@/views/Community.vue";
import AI from "@/views/AI.vue";

// 扩展路由元数据类型
declare module "vue-router" {
  interface RouteMeta {
    requiresAuth?: boolean;
    guestOnly?: boolean;
    requiresTeacher?: boolean;
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/register",
      name: "register",
      component: Register,
    },
    {
      path: "/auth",
      name: "auth",
      component: Auth,
    },
    {
      path: "/question-bank",
      name: "question-bank",
      component: QuestionBank,
      meta: { requiresAuth: true },
    },
    {
      path: "/exam",
      name: "exam",
      component: Exam,
      meta: { requiresAuth: true },
    },
    {
      path: "/member-center",
      name: "member-center",
      component: MemberCenter,
      meta: { requiresAuth: true },
    },
    {
      path: "/teachers",
      name: "teachers",
      component: Teachers,
    },
    {
      path: "/teacher-list",
      name: "teacher-list",
      component: TeacherList,
    },
    {
      path: "/teacher/:id",
      name: "teacher-detail",
      component: TeacherDetail,
    },
    {
      path: "/teacher-dashboard",
      name: "teacher-dashboard",
      component: TeacherDashboard,
      meta: { requiresAuth: true, requiresTeacher: true },
    },
    {
      path: "/courses",
      name: "courses",
      component: CourseList,
    },
    {
      path: "/course/:id",
      name: "course-detail",
      component: CourseDetail,
    },
    {
      path: "/community",
      name: "community",
      component: Community,
      meta: { requiresAuth: true },
    },
    {
      path: "/ai",
      name: "ai",
      component: AI,
      meta: { requiresAuth: true },
    },
  ],
});

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  const userRole = localStorage.getItem("userRole");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else if (
    to.meta.requiresTeacher &&
    userRole !== "teacher" &&
    userRole !== "admin"
  ) {
    next("/");
  } else {
    next();
  }
});

export default router;
