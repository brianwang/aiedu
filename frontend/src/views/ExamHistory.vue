<template>
  <div class="exam-history-container">
    <h2>历史试卷管理</h2>
    <div class="search-bar">
      <el-input v-model="searchTitle" placeholder="搜索试卷名称/学科" style="width: 220px; margin-right: 12px;" clearable />
      <el-button @click="fetchExams" type="primary">搜索</el-button>
    </div>
    <el-table :data="exams" style="width: 100%" v-loading="loading" stripe border>
      <el-table-column prop="title" label="试卷名称" min-width="180" />
      <el-table-column prop="subject" label="学科" min-width="100" />
      <el-table-column prop="difficulty" label="难度" min-width="80">
        <template #default="scope">
          <el-tag v-if="scope && scope.row" :type="difficultyType(scope.row.difficulty)">{{ difficultyText(scope.row.difficulty) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="total_score" label="总分" min-width="80" />
      <el-table-column prop="created_at" label="创建时间" min-width="140" />
      <el-table-column prop="score" label="成绩" min-width="90">
        <template #default="scope">
          <span v-if="scope && scope.row" :class="scoreClass(scope.row.score)">{{ scope.row.score ?? '-' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="160">
        <template #default="scope">
          <el-button v-if="scope && scope.row" size="small" @click="goToExam(scope.row)">查看详情</el-button>
          <el-popconfirm v-if="scope && scope.row" title="确定删除该试卷吗？" @confirm="deleteExam(scope.row)">
            <el-button size="small" type="danger" style="margin-left:8px;">删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="exams.length === 0 && !loading" description="暂无历史试卷" style="margin:40px 0;" />
    <el-pagination
      v-if="total > pageSize"
      style="margin-top: 24px; text-align: right;"
      background
      layout="prev, pager, next, jumper"
      :total="total"
      :page-size="pageSize"
      :current-page.sync="page"
      @current-change="fetchExams"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const exams = ref<any[]>([]);
const loading = ref(false);
const total = ref(0);
const page = ref(1);
const pageSize = 10;
const searchTitle = ref("");

const fetchExams = async () => {
  loading.value = true;
  try {
    const params: any = { page: page.value, limit: pageSize };
    if (searchTitle.value) {
      params.q = searchTitle.value;
    }
    const res = await axios.get("/exam/list", { params });
    exams.value = res.data.items || res.data; // 兼容后端返回格式
    total.value = res.data.total || res.data.length || 0;
  } catch (e) {
    exams.value = [];
    total.value = 0;
  } finally {
    loading.value = false;
  }
};

const goToExam = (exam: any) => {
  router.push(`/exam/${exam.id}`);
};

const deleteExam = async (exam: any) => {
  try {
    await axios.delete(`/exam/${exam.id}`);
    fetchExams();
  } catch (e) {
    // 可加错误提示
  }
};

const difficultyText = (d: number) => {
  switch (d) {
    case 1: return '基础';
    case 2: return '简单';
    case 3: return '中等';
    case 4: return '困难';
    case 5: return '专家';
    default: return d;
  }
};
const difficultyType = (d: number) => {
  switch (d) {
    case 1: return 'success';
    case 2: return 'info';
    case 3: return 'warning';
    case 4: return 'danger';
    case 5: return 'danger';
    default: return '';
  }
};
const scoreClass = (score: number) => {
  if (score == null) return '';
  if (score >= 90) return 'score-high';
  if (score >= 60) return 'score-mid';
  return 'score-low';
};

onMounted(fetchExams);
</script>

<style scoped>
.exam-history-container {
  max-width: 900px;
  margin: 40px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.search-bar {
  margin-bottom: 18px;
  display: flex;
  align-items: center;
}
.score-high { color: #43a047; font-weight: bold; }
.score-mid { color: #ffa726; font-weight: bold; }
.score-low { color: #e53935; font-weight: bold; }
</style> 