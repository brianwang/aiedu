<script setup lang="ts">
import CourseList from "@/views/CourseList.vue";
import TeacherList from "@/views/TeacherList.vue";
</script>

<template>
  <div class="home">
    <h1>精选课程</h1>
    <CourseList />

    <h1>推荐教师</h1>
    <TeacherList />
  </div>
</template>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin: 2rem 0 1rem;
  font-size: 1.5rem;
}
</style>
