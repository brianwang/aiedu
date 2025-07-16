<template>
  <div class="exam-list-container">
    <div class="exam-list-header">
      <h1>试卷管理</h1>
      <el-button type="primary" @click="onCreateExam">新建试卷</el-button>
    </div>
    <div class="exam-list-search">
      <el-input v-model="search.keyword" placeholder="试卷名称/创建人/标签" style="width: 220px; margin-right: 10px;" />
      <el-select v-model="search.subject" placeholder="学科" clearable style="width: 120px; margin-right: 10px;">
        <el-option v-for="item in subjectOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-select v-model="search.difficulty" placeholder="难度" clearable style="width: 120px; margin-right: 10px;">
        <el-option label="简单" value="easy" />
        <el-option label="中等" value="medium" />
        <el-option label="困难" value="hard" />
      </el-select>
      <el-select v-model="search.skillPoints" multiple filterable allow-create placeholder="技能点" style="width: 200px; margin-right: 10px;">
        <el-option v-for="item in skillPointOptions" :key="item" :label="item" :value="item" />
      </el-select>
      <el-date-picker v-model="search.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="margin-right: 10px;" />
      <el-button type="primary" @click="fetchExamList">搜索</el-button>
      <el-button @click="resetSearch">重置</el-button>
    </div>
    <el-table :data="examList" style="width: 100%; margin-top: 20px;" border>
      <el-table-column prop="title" label="试卷名称" min-width="160" />
      <el-table-column prop="subject" label="学科" width="100" />
      <el-table-column prop="difficulty" label="难度" width="100" />
      <el-table-column prop="skill_points" label="技能点" min-width="120">
        <template #default="scope">
          <el-tag v-for="sp in scope.row.skill_points" :key="sp" style="margin-right: 4px;">{{ sp }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="question_count" label="题目数" width="80" />
      <el-table-column prop="creator" label="创建人" width="100" />
      <el-table-column prop="created_at" label="创建时间" width="160" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="scope">
          <el-tag :type="scope.row.status === 'published' ? 'success' : 'info'">
            {{ scope.row.status === 'published' ? '已发布' : '未发布' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220">
        <template #default="scope">
          <el-button size="small" @click="onViewDetail(scope.row)">查看</el-button>
          <el-button size="small" @click="onEditExam(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="onDeleteExam(scope.row)">删除</el-button>
          <el-button size="small" type="success" v-if="scope.row.status !== 'published'" @click="onPublishExam(scope.row)">发布</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="exam-list-pagination">
      <el-pagination
        background
        layout="prev, pager, next, jumper, ->, total"
        :total="total"
        :page-size="pageSize"
        :current-page="page"
        @current-change="onPageChange"
      />
    </div>
    <!-- 详情弹窗、表单弹窗后续补充 -->
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
// import { fetchExamListApi, deleteExamApi, publishExamApi } from '@/api/exam';

const examList = ref<any[]>([]);
const total = ref(0);
const page = ref(1);
const pageSize = ref(10);

const search = reactive({
  keyword: '',
  subject: '',
  difficulty: '',
  skillPoints: [],
  dateRange: [],
});

const subjectOptions = ['语文', '数学', '英语', '物理', '化学', '生物'];
const skillPointOptions = ['阅读', '写作', '计算', '逻辑', '实验'];

const fetchExamList = async () => {
  // TODO: 调用后端API获取试卷列表，带分页和筛选参数
  // const res = await fetchExamListApi({ ...search, page: page.value, pageSize: pageSize.value });
  // examList.value = res.data.list;
  // total.value = res.data.total;
};

const resetSearch = () => {
  search.keyword = '';
  search.subject = '';
  search.difficulty = '';
  search.skillPoints = [];
  search.dateRange = [];
  fetchExamList();
};

const onPageChange = (val: number) => {
  page.value = val;
  fetchExamList();
};

const onCreateExam = () => {
  // TODO: 打开新建试卷表单弹窗
};
const onEditExam = (row: any) => {
  // TODO: 打开编辑试卷表单弹窗
};
const onViewDetail = (row: any) => {
  // TODO: 打开试卷详情弹窗
};
const onDeleteExam = (row: any) => {
  ElMessageBox.confirm('确定要删除该试卷吗？', '提示', { type: 'warning' })
    .then(() => {
      // TODO: 调用删除API
      ElMessage.success('删除成功');
      fetchExamList();
    })
    .catch(() => {});
};
const onPublishExam = (row: any) => {
  ElMessageBox.confirm('确定要发布该试卷吗？', '提示', { type: 'info' })
    .then(() => {
      // TODO: 调用发布API
      ElMessage.success('发布成功');
      fetchExamList();
    })
    .catch(() => {});
};

onMounted(() => {
  fetchExamList();
});
</script>

<style scoped>
.exam-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.exam-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.exam-list-search {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.exam-list-pagination {
  margin: 24px 0 0 0;
  text-align: right;
}
</style> 