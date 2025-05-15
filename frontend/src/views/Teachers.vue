<script setup lang="ts">
import { NGrid, NGi, NCard, NButton } from "naive-ui";
import { useRouter } from "vue-router";

const router = useRouter();
const teachers = [
  { id: 1, name: "张教授", subject: "人工智能" },
  { id: 2, name: "李教授", subject: "机器学习" },
  { id: 3, name: "王教授", subject: "深度学习" },
  { id: 4, name: "赵教授", subject: "自然语言处理" },
  { id: 5, name: "刘教授", subject: "计算机视觉" },
  { id: 6, name: "陈教授", subject: "数据科学" },
  { id: 7, name: "杨教授", subject: "算法设计" },
  { id: 8, name: "周教授", subject: "大数据分析" },
];

const viewTeacher = (id: number) => {
  router.push(`/teachers/${id}`);
};
</script>

<template>
  <div class="home">
    <h2>推荐教师</h2>
    <NGrid :cols="4" :x-gap="16" :y-gap="16">
      <NGi v-for="teacher in teachers" :key="teacher.id">
        <NCard :title="teacher.name">
          <p>{{ teacher.subject }}</p>
          <template #footer>
            <NButton
              type="primary"
              size="small"
              @click="viewTeacher(teacher.id)"
            >
              查看详情
            </NButton>
          </template>
        </NCard>
      </NGi>
    </NGrid>
  </div>
</template>

<style scoped>
.home {
  padding: 2rem;
}
h2 {
  margin-bottom: 1.5rem;
}
</style>
