import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Teachers from "../views/Teachers.vue";
import Community from "../views/Community.vue";
import CourseDetail from "../views/CourseDetail.vue";
import Auth from "../views/Auth.vue";
import TeacherDetail from "../views/TeacherDetail.vue";
import MemberCenter from "../views/MemberCenter.vue";
import TeacherDashboard from "../views/TeacherDashboard.vue";
import CourseList from "../views/CourseList.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home,
    },
    {
      path: "/courses",
      name: "CourseList",
      component: CourseList,
    },
    {
      path: "/courses/:id",
      name: "CourseDetail",
      component: CourseDetail,
    },
    {
      path: "/teachers",
      name: "Teachers",
      component: Teachers,
    },
    {
      path: "/teachers/:id",
      name: "TeacherDetail",
      component: TeacherDetail,
    },
    {
      path: "/community",
      name: "Community",
      component: Community,
    },
    {
      path: "/auth",
      name: "Auth",
      component: Auth,
    },
    {
      path: "/member",
      name: "MemberCenter",
      component: MemberCenter,
      meta: { requiresAuth: true },
    },
    {
      path: "/teacher-dashboard",
      name: "TeacherDashboard",
      component: TeacherDashboard,
      meta: { requiresAuth: true, requiresTeacherRole: true },
    },
  ],
});

export default router;
