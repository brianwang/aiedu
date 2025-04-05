<script setup lang="ts">
import { NMenu, NButton, NSpace, NAvatar, NDropdown } from "naive-ui";
import { useRouter } from "vue-router";
import { ref } from "vue";

const router = useRouter();
const isLoggedIn = ref(false); // 实际应用中应从状态管理获取
const isTeacher = ref(true); // 实际应用中应从状态管理获取

const menuOptions = [
  {
    label: "首页",
    key: "home",
  },
  {
    label: "课程",
    key: "courses",
  },
  {
    label: "教师",
    key: "teachers",
  },
  {
    label: "社区",
    key: "community",
  },
];

const handleMenuSelect = (key: string) => {
  router.push(`/${key === "home" ? "" : key}`);
};

const goToAuth = () => {
  router.push("/auth");
};

const goToDashboard = () => {
  if (isTeacher.value) {
    router.push("/teacher-dashboard");
  } else {
    router.push("/member");
  }
};
</script>

<template>
  <div class="nav-bar">
    <NSpace justify="space-between" align="center">
      <NMenu
        mode="horizontal"
        :options="menuOptions"
        @update:value="handleMenuSelect"
      />
      <NSpace>
        <NButton v-if="isLoggedIn" type="info" @click="goToDashboard">
          <NAvatar round size="small" src="https://example.com/avatar.jpg" />
          <span style="margin-left: 8px">{{
            isTeacher ? "教师后台" : "会员中心"
          }}</span>
        </NButton>
        <NButton v-else type="primary" @click="goToAuth"> 登录/注册 </NButton>
      </NSpace>
    </NSpace>
  </div>
</template>

<style scoped>
.nav-bar {
  padding: 1rem 2rem;
  border-bottom: 1px solid #eee;
}
</style>
