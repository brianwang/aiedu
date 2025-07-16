<template>
  <div class="exam-generate-container">
    <h2>智能组卷</h2>
    <form @submit.prevent="handleGenerateExam">
      <div class="form-group">
        <label>学科：</label>
        <el-input v-model="form.subject" placeholder="请输入学科" :disabled="loading" />
      </div>
      <div class="form-group">
        <label>难度：</label>
        <el-select v-model.number="form.difficulty" :disabled="loading">
          <el-option :value="1">基础</el-option>
          <el-option :value="2">简单</el-option>
          <el-option :value="3">中等</el-option>
          <el-option :value="4">困难</el-option>
          <option :value="5">专家</option>
        </el-select>
      </div>
      <div class="form-group">
        <label>技能点（可多选）：</label>
        <el-select v-model="form.skills" multiple filterable allow-create default-first-option placeholder="请选择或输入技能点" style="width:100%" :disabled="loading" @change="handleSkillsChange">
          <el-option v-for="skill in skills" :key="skill" :label="skill" :value="skill" />
        </el-select>
      </div>
      <div class="form-group">
        <label>标签（可多选）：</label>
        <el-select v-model="form.tags" multiple filterable placeholder="请选择标签" style="width:100%" :disabled="loading">
          <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.name" />
        </el-select>
      </div>
      <div class="form-group">
        <label>题型分布（可选，JSON）：</label>
        <textarea v-model="questionDistributionInput" placeholder='{"single_choice":10,"fill_blank":5}' rows="2" :disabled="loading"></textarea>
      </div>
      <button type="submit" :disabled="loading">生成试卷</button>
      <el-progress v-if="loading" :percentage="70" status="active" style="margin-top:16px;" />
    </form>
    <div v-if="successMsg" class="success">{{ successMsg }}</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { generateExam } from "@/api/exam";
import axios from "axios";
import { ElMessage } from 'element-plus';

const router = useRouter();
const form = ref({
  subject: "",
  difficulty: 3,
  skills: [],
  tags: [],
});
const categories = ref<any[]>([]);
const skills = ref<string[]>([]);
const questionDistributionInput = ref("");
const loading = ref(false);
const error = ref("");
const successMsg = ref("");

onMounted(async () => {
  // 获取题目分类
  const catRes = await axios.get("/question-bank/categories");
  categories.value = catRes.data;
  // 获取技能点
  const skillRes = await axios.get("/api/v1/skills");
  skills.value = skillRes.data;
});

const handleGenerateExam = async () => {
  loading.value = true;
  error.value = "";
  successMsg.value = "";
  if (!form.value.subject) {
    error.value = "学科不能为空，请选择学科";
    loading.value = false;
    return;
  }
  try {
    let question_distribution = undefined;
    if (questionDistributionInput.value.trim()) {
      try {
        question_distribution = JSON.parse(questionDistributionInput.value);
      } catch (e) {
        error.value = "题型分布格式错误，请输入合法JSON";
        loading.value = false;
        return;
      }
    }
    const res: any = await generateExam({
      subject: form.value.subject,
      difficulty: form.value.difficulty,
      skill: form.value.skills.length > 0 ? form.value.skills.join(",") : undefined,
      tags: form.value.tags.length > 0 ? form.value.tags : undefined,
      question_distribution,
    });
    const examId = res.data.id || res.data.examId;
    if (examId) {
      successMsg.value = "试卷生成成功，正在跳转...";
      setTimeout(() => {
        router.push(`/exam/${examId}`);
      }, 800);
    } else {
      error.value = "试卷生成成功，但未获取到试卷ID";
    }
  } catch (e: any) {
    error.value = e?.message || "生成试卷失败";
  } finally {
    loading.value = false;
  }
};

const handleSkillsChange = async (val: string[]) => {
  // 找出新输入的技能点
  const newSkills = val.filter(skill => !skills.value.includes(skill));
  for (const skill of newSkills) {
    try {
      await axios.post('/api/v1/skills', null, { params: { name: skill } });
      ElMessage.success(`新技能点“${skill}”已添加`);
    } catch (e) {
      ElMessage.error(`添加技能点“${skill}”失败`);
    }
  }
  // 刷新技能点列表
  const skillRes = await axios.get('/api/v1/skills');
  skills.value = skillRes.data;
};
</script>

<style scoped>
.exam-generate-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 30px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.form-group {
  margin-bottom: 18px;
}
label {
  font-weight: 500;
  margin-bottom: 6px;
  display: block;
}
input, select, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
}
button[type="submit"] {
  width: 100%;
  padding: 12px;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}
button[disabled] {
  background: #ccc;
  cursor: not-allowed;
}
.error {
  color: #d32f2f;
  margin-top: 16px;
  text-align: center;
}
.success {
  color: #43a047;
  margin-top: 16px;
  text-align: center;
  font-weight: bold;
}
</style> 