<script setup lang="ts">
import { NCard, NButton, NSpace, NTag } from "naive-ui";
import { useRouter } from "vue-router";

const router = useRouter();
const teacher = {
  id: 1,
  name: "张教授",
  avatar: "https://example.com/teacher1.jpg",
  title: "人工智能专家",
  university: "清华大学",
  courses: [
    { id: 1, name: "AI基础课程" },
    { id: 2, name: "机器学习进阶" },
  ],
  bio: "10年人工智能教学经验，发表论文20余篇...",
};

const viewCourse = (courseId: number) => {
  router.push(`/courses/${courseId}`);
};
</script>

<template>
  <div class="teacher-detail">
    <NCard :title="teacher.name">
      <div class="teacher-info">
        <img :src="teacher.avatar" :alt="teacher.name" class="avatar" />
        <div>
          <p><strong>职称:</strong> {{ teacher.title }}</p>
          <p><strong>院校:</strong> {{ teacher.university }}</p>
          <p><strong>简介:</strong> {{ teacher.bio }}</p>
        </div>
      </div>

      <h3>主讲课程</h3>
      <NSpace>
        <NTag
          v-for="course in teacher.courses"
          :key="course.id"
          type="info"
          @click="viewCourse(course.id)"
        >
          {{ course.name }}
        </NTag>
      </NSpace>
    </NCard>
  </div>
</template>

<style scoped>
.teacher-detail {
  max-width: 800px;
  margin: 2rem auto;
}

.teacher-info {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

h3 {
  margin: 1.5rem 0 1rem;
}
</style>
