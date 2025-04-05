<script setup lang="ts">
import {
  NLayout,
  NLayoutSider,
  NLayoutContent,
  NMenu,
  NCard,
  NButton,
} from "naive-ui";
import { ref, h } from "vue";
import type { MenuOption } from "naive-ui";

const menuOptions: MenuOption[] = [
  {
    label: "课程管理",
    key: "courses",
    icon: () => h("div", { class: "i-carbon-book" }),
  },
  {
    label: "智能排课",
    key: "scheduling",
    icon: () => h("div", { class: "i-carbon-calendar" }),
  },
  {
    label: "内容编辑",
    key: "content",
    icon: () => h("div", { class: "i-carbon-edit" }),
  },
  {
    label: "数据统计",
    key: "analytics",
    icon: () => h("div", { class: "i-carbon-chart-line" }),
  },
];

const activeKey = ref("courses");
</script>

<template>
  <NLayout has-sider>
    <NLayoutSider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="240"
      show-trigger
    >
      <NMenu
        v-model:value="activeKey"
        :options="menuOptions"
        :collapsed-width="64"
        :collapsed-icon-size="22"
      />
    </NLayoutSider>

    <NLayoutContent>
      <NCard title="课程管理" v-if="activeKey === 'courses'">
        <div class="dashboard-content">
          <h3>我的课程</h3>
          <!-- 课程列表组件将放在这里 -->
          <NButton type="primary">创建新课程</NButton>
        </div>
      </NCard>

      <NCard title="智能排课" v-if="activeKey === 'scheduling'">
        <div class="dashboard-content">
          <h3>排课日历</h3>
          <!-- 排课组件将放在这里 -->
        </div>
      </NCard>

      <NCard title="内容编辑" v-if="activeKey === 'content'">
        <div class="dashboard-content">
          <h3>课程内容编辑器</h3>
          <!-- 富文本编辑器将放在这里 -->
        </div>
      </NCard>

      <NCard title="数据统计" v-if="activeKey === 'analytics'">
        <div class="dashboard-content">
          <h3>课程数据</h3>
          <!-- 统计图表将放在这里 -->
        </div>
      </NCard>
    </NLayoutContent>
  </NLayout>
</template>

<style scoped>
.dashboard-content {
  padding: 1rem;
}

h3 {
  margin-bottom: 1.5rem;
}
</style>
