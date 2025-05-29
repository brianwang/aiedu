import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Login from "@/views/Login.vue";
import Exam from "@/views/Exam.vue";
import { useAuthStore } from "../stores/auth";
import Register from "@/views/Register.vue";
import QuestionBank from "@/views/QuestionBank.vue";

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
  ],
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth && !authStore.isAuthenticated()) {
    next({ name: "login" });
  } else if (to.meta.guestOnly && authStore.isAuthenticated()) {
    next({ name: "home" });
  } else {
    next();
  }
});

export default router;
