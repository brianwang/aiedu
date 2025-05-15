<template>
  <div class="community">
    <NCard title="社区互动">
      <NInput
        v-model:value="newPost"
        type="textarea"
        placeholder="分享你的想法..."
        :autosize="{ minRows: 3 }"
      />
      <NButton type="primary" @click="addPost" style="margin-top: 1rem">
        发布
      </NButton>

      <NList style="margin-top: 2rem">
        <NListItem v-for="post in posts" :key="post.id">
          <div class="post">
            <div class="post-header">
              <strong>{{ post.author }}</strong>
              <span>{{ post.time }}</span>
            </div>
            <p>{{ post.content }}</p>
          </div>
        </NListItem>
      </NList>
    </NCard>
  </div>
</template>

<script setup lang="ts">
import { NCard, NInput, NButton, NList, NListItem } from "naive-ui";
import { ref } from "vue";

const posts = ref([
  { id: 1, author: "张三", content: "这个课程很有帮助！", time: "2025-04-01" },
  {
    id: 2,
    author: "李四",
    content: "有没有一起学习的同学？",
    time: "2025-04-02",
  },
]);

const newPost = ref("");
const addPost = () => {
  if (newPost.value.trim()) {
    posts.value.unshift({
      id: posts.value.length + 1,
      author: "当前用户",
      content: newPost.value,
      time: new Date().toISOString().split("T")[0],
    });
    newPost.value = "";
  }
};
</script>

<style scoped>
.community {
  max-width: 800px;
  margin: 2rem auto;
}

.post {
  padding: 1rem;
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  color: #666;
}
</style>
