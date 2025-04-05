<template>
  <div class="teacher-list">
    <n-card v-for="teacher in teachers" :key="teacher.id" class="teacher-card">
      <n-space align="center">
        <n-avatar :src="teacher.avatar" round size="large" />
        <n-space vertical>
          <h3>{{ teacher.name }}</h3>
          <n-space align="center">
            <n-rate readonly :value="teacher.rating" />
            <span>{{ teacher.rating }}</span>
          </n-space>
          <span>专业: {{ teacher.specialty }}</span>
        </n-space>
        <n-button :type="teacher.isFollowing ? 'default' : 'primary'">
          {{ teacher.isFollowing ? "已关注" : "关注" }}
        </n-button>
      </n-space>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { NAvatar, NSpace, NButton, NRate, NCard } from "naive-ui";

const teachers = [
  {
    id: 1,
    name: "张教授",
    avatar: "https://randomuser.me/api/portraits/men/1.jpg",
    rating: 4.8,
    specialty: "人工智能",
    isFollowing: false,
  },
  {
    id: 2,
    name: "李老师",
    avatar: "https://randomuser.me/api/portraits/women/2.jpg",
    rating: 4.5,
    specialty: "机器学习",
    isFollowing: true,
  },
];
</script>

<style scoped>
.teacher-card {
  margin-bottom: 1rem;
}
</style>
