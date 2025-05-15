<script setup lang="ts">
import { NCard, NSpace, NButton, NGrid, NGi } from "naive-ui";
import { useRouter } from "vue-router";

const router = useRouter();
const courses = [
  {
    id: 1,
    title: "AI基础课程",
    description: "学习人工智能基础知识",
    price: 299,
    hasTrial: true,
    image: "https://example.com/ai-basic.jpg",
  },
  {
    id: 2,
    title: "机器学习实战",
    description: "从零开始掌握机器学习",
    price: 499,
    hasTrial: false,
    image: "https://example.com/ml-practice.jpg",
  },
  {
    id: 3,
    title: "深度学习入门",
    description: "深度学习理论与应用",
    price: 399,
    hasTrial: true,
    image: "https://example.com/dl-intro.jpg",
  },
  {
    id: 4,
    title: "自然语言处理",
    description: "NLP核心技术讲解",
    price: 599,
    hasTrial: false,
    image: "https://example.com/nlp-core.jpg",
  },
];

const viewDetail = (courseId: number) => {
  router.push(`/courses/${courseId}`);
};
</script>

<template>
  <NGrid :cols="2" :x-gap="16" :y-gap="16">
    <NGi v-for="course in courses" :key="course.id">
      <NCard :title="course.title">
        <img
          :src="course.image"
          :alt="course.title"
          style="
            width: 100%;
            height: 160px;
            object-fit: cover;
            margin-bottom: 1rem;
          "
        />
        <p>{{ course.description }}</p>
        <template #footer>
          <NSpace justify="space-between">
            <span>¥{{ course.price }}</span>
            <NSpace>
              <NButton v-if="course.hasTrial" type="primary" size="small"
                >免费试听</NButton
              >
              <NButton type="info" size="small" @click="viewDetail(course.id)"
                >查看详情</NButton
              >
            </NSpace>
          </NSpace>
        </template>
      </NCard>
    </NGi>
  </NGrid>
</template>
