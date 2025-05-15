import { createRouter, createWebHistory } from "vue-router";
import QuestionBank from "@/views/QuestionBank.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/Home.vue"),
    },
    {
      path: "/questions",
      name: "questions",
      component: QuestionBank,
      meta: {
        requiresAuth: true,
      },
    },
    {
      path: "/auth",
      name: "auth",
      component: () => import("@/views/Auth.vue"),
    },
  ],
});

export default router;
