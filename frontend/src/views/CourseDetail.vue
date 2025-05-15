<script setup lang="ts">
import { useRoute } from "vue-router";
import { NCard, NButton, NSpace, NRate } from "naive-ui";
import { ref } from "vue";

const route = useRoute();
const courseId = route.params.id;
const course = ref({
  id: courseId,
  title: "AI基础课程",
  description: "学习人工智能基础知识",
  price: 299,
  rating: 4.8,
  teacher: "张教授",
  videoUrl: "https://example.com/video.mp4",
});
</script>

<template>
  <div class="course-detail">
    <NCard :title="course.title">
      <video :src="course.videoUrl" controls width="100%"></video>
      <p>{{ course.description }}</p>
      <NSpace align="center">
        <span>评分：</span>
        <NRate readonly :value="course.rating" />
        <span>{{ course.rating }}</span>
      </NSpace>
      <p>讲师：{{ course.teacher }}</p>
      <p>价格：¥{{ course.price }}</p>
      <template #footer>
        <NSpace justify="end">
          <NButton type="primary">立即购买</NButton>
          <NButton>加入收藏</NButton>
        </NSpace>
      </template>
    </NCard>
  </div>
</template>

<style scoped>
.course-detail {
  max-width: 800px;
  margin: 2rem auto;
}
</style>
