<script setup lang="ts">
import { NCard, NButton, NTag, NSpace } from "naive-ui";

const memberInfo = {
  name: "张三",
  avatar: "https://example.com/avatar.jpg",
  memberType: "高级会员",
  expireDate: "2026-04-05",
  courses: [
    { id: 1, name: "AI基础课程", progress: 80 },
    { id: 2, name: "机器学习实战", progress: 45 },
  ],
};

const renewMember = () => {
  // 续费会员逻辑
};
</script>

<template>
  <div class="member-center">
    <NCard title="会员中心">
      <div class="member-info">
        <img :src="memberInfo.avatar" :alt="memberInfo.name" class="avatar" />
        <div>
          <h3>{{ memberInfo.name }}</h3>
          <NSpace>
            <NTag type="success">{{ memberInfo.memberType }}</NTag>
            <span>有效期至: {{ memberInfo.expireDate }}</span>
          </NSpace>
        </div>
      </div>

      <h3>我的课程</h3>
      <NSpace vertical>
        <NCard
          v-for="course in memberInfo.courses"
          :key="course.id"
          :title="course.name"
        >
          <p>学习进度: {{ course.progress }}%</p>
        </NCard>
      </NSpace>

      <NButton type="primary" @click="renewMember" style="margin-top: 2rem">
        续费会员
      </NButton>
    </NCard>
  </div>
</template>

<style scoped>
.member-center {
  max-width: 800px;
  margin: 2rem auto;
}

.member-info {
  display: flex;
  gap: 2rem;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

h3 {
  margin: 1.5rem 0 1rem;
}
</style>
