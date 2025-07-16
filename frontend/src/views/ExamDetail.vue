<template>
  <el-drawer v-model="visible" title="试卷详情" size="50%" :with-header="true" @close="onClose">
    <div class="exam-detail-info">
      <h2>{{ exam.title }}</h2>
      <div class="meta">
        <span>学科：{{ exam.subject }}</span>
        <span>难度：{{ difficultyMap[exam.difficulty] }}</span>
        <span>技能点：
          <el-tag v-for="sp in exam.skill_points" :key="sp" style="margin-right: 4px;">{{ sp }}</el-tag>
        </span>
        <span>题目数：{{ exam.question_count }}</span>
        <span>创建人：{{ exam.creator }}</span>
        <span>创建时间：{{ exam.created_at }}</span>
        <el-tag :type="exam.status === 'published' ? 'success' : 'info'">
          {{ exam.status === 'published' ? '已发布' : '未发布' }}
        </el-tag>
      </div>
    </div>
    <el-divider>题目列表</el-divider>
    <el-table :data="exam.questions" border size="small">
      <el-table-column prop="index" label="#" width="50">
        <template #default="scope">{{ scope.$index + 1 }}</template>
      </el-table-column>
      <el-table-column prop="type" label="题型" width="80">
        <template #default="scope">{{ getQuestionType(scope.row.type) }}</template>
      </el-table-column>
      <el-table-column prop="content" label="题目内容" min-width="200" />
      <el-table-column prop="score" label="分值" width="60" />
    </el-table>
    <el-divider>分数分布</el-divider>
    <div class="score-distribution">
      <el-progress :percentage="scorePercent" status="success" />
      <div>总分：{{ totalScore }}，已答：{{ answeredScore }}</div>
    </div>
    <el-divider>考试记录</el-divider>
    <el-table :data="exam.records" border size="small">
      <el-table-column prop="student_name" label="学生" width="120" />
      <el-table-column prop="score" label="得分" width="80" />
      <el-table-column prop="submit_time" label="提交时间" width="160" />
    </el-table>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue';

const props = defineProps<{
  visible: boolean;
  exam: any;
}>();
const emit = defineEmits(['update:visible', 'close']);

const difficultyMap: Record<string, string> = {
  easy: '简单',
  medium: '中等',
  hard: '困难',
};

const getQuestionType = (type: string) => {
  const map: Record<string, string> = {
    choice: '单选题',
    multiple: '多选题',
    true_false: '判断题',
    fill_blank: '填空题',
    essay: '问答题',
  };
  return map[type] || type;
};

const totalScore = computed(() =>
  props.exam.questions?.reduce((sum: number, q: any) => sum + (q.score || 0), 0) || 0
);
const answeredScore = computed(() =>
  props.exam.records?.reduce((sum: number, r: any) => sum + (r.score || 0), 0) || 0
);
const scorePercent = computed(() =>
  totalScore.value ? Math.round((answeredScore.value / totalScore.value) * 100) : 0
);

const visible = ref(props.visible);
watch(() => props.visible, v => (visible.value = v));
const onClose = () => {
  emit('update:visible', false);
  emit('close');
};
</script>

<style scoped>
.exam-detail-info {
  margin-bottom: 16px;
}
.exam-detail-info .meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 8px;
  align-items: center;
}
.score-distribution {
  margin-bottom: 16px;
}
</style> 