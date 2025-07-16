<template>
  <el-drawer v-model="visible" :title="isEdit ? '编辑试卷' : '新建试卷'" size="60%" :with-header="true" @close="onClose">
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" class="exam-form">
      <el-form-item label="试卷名称" prop="title">
        <el-input v-model="form.title" placeholder="请输入试卷名称" />
      </el-form-item>
      <el-form-item label="学科" prop="subject">
        <el-select v-model="form.subject" placeholder="请选择学科">
          <el-option v-for="item in subjectOptions" :key="item" :label="item" :value="item" />
        </el-select>
      </el-form-item>
      <el-form-item label="难度" prop="difficulty">
        <el-select v-model="form.difficulty" placeholder="请选择难度">
          <el-option label="简单" value="easy" />
          <el-option label="中等" value="medium" />
          <el-option label="困难" value="hard" />
        </el-select>
      </el-form-item>
      <el-form-item label="技能点" prop="skill_points">
        <el-select v-model="form.skill_points" multiple filterable allow-create placeholder="请选择技能点">
          <el-option v-for="item in skillPointOptions" :key="item" :label="item" :value="item" />
        </el-select>
      </el-form-item>
      <el-divider>题目列表</el-divider>
      <div v-for="(q, idx) in form.questions" :key="idx" class="question-block">
        <el-form-item :label="`题目${idx + 1}`" :prop="`questions.${idx}.content`" required>
          <el-input v-model="q.content" placeholder="请输入题目内容" />
        </el-form-item>
        <el-form-item :label="`题型`" :prop="`questions.${idx}.type`" required>
          <el-select v-model="q.type" placeholder="请选择题型">
            <el-option label="单选题" value="choice" />
            <el-option label="多选题" value="multiple" />
            <el-option label="判断题" value="true_false" />
            <el-option label="填空题" value="fill_blank" />
            <el-option label="问答题" value="essay" />
          </el-select>
        </el-form-item>
        <el-form-item :label="`分值`" :prop="`questions.${idx}.score`" required>
          <el-input-number v-model="q.score" :min="1" :max="100" />
        </el-form-item>
        <template v-if="q.type === 'choice' || q.type === 'multiple'">
          <el-form-item label="选项" required>
            <div v-for="(opt, oidx) in q.options" :key="oidx" class="option-row">
              <el-input v-model="opt.label" placeholder="选项内容" style="width: 200px; margin-right: 8px;" />
              <el-input v-model="opt.value" placeholder="选项值" style="width: 100px; margin-right: 8px;" />
              <el-button icon="el-icon-delete" type="danger" @click="removeOption(idx, oidx)" circle size="small" />
            </div>
            <el-button type="primary" @click="addOption(idx)" size="small">添加选项</el-button>
          </el-form-item>
        </template>
        <el-form-item label="标准答案" :prop="`questions.${idx}.answer`" required>
          <el-input v-model="q.answer" placeholder="请输入标准答案" />
        </el-form-item>
        <el-button type="danger" @click="removeQuestion(idx)" size="small" style="margin-bottom: 12px;">删除题目</el-button>
        <el-divider />
      </div>
      <el-button type="primary" @click="addQuestion" style="margin-bottom: 16px;">添加题目</el-button>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">{{ isEdit ? '保存修改' : '创建试卷' }}</el-button>
        <el-button @click="onClose">取消</el-button>
      </el-form-item>
    </el-form>
  </el-drawer>
</template>

<script setup lang="ts">
import { ref, reactive, watch, nextTick } from 'vue';
import { ElMessage } from 'element-plus';

const props = defineProps<{
  visible: boolean;
  isEdit?: boolean;
  exam?: any;
}>();
const emit = defineEmits(['update:visible', 'close', 'submit']);

const visible = ref(props.visible);
watch(() => props.visible, v => (visible.value = v));
const isEdit = props.isEdit || false;

const subjectOptions = ['语文', '数学', '英语', '物理', '化学', '生物'];
const skillPointOptions = ['阅读', '写作', '计算', '逻辑', '实验'];

const formRef = ref();
const form = reactive({
  title: '',
  subject: '',
  difficulty: '',
  skill_points: [],
  questions: [] as any[],
});

const rules = {
  title: [{ required: true, message: '请输入试卷名称', trigger: 'blur' }],
  subject: [{ required: true, message: '请选择学科', trigger: 'change' }],
  difficulty: [{ required: true, message: '请选择难度', trigger: 'change' }],
  skill_points: [{ required: true, message: '请选择技能点', trigger: 'change' }],
  questions: [{ type: 'array', required: true, min: 1, message: '请至少添加一道题目', trigger: 'change' }],
};

const addQuestion = () => {
  form.questions.push({
    content: '',
    type: '',
    score: 1,
    options: [],
    answer: '',
  });
};
const removeQuestion = (idx: number) => {
  form.questions.splice(idx, 1);
};
const addOption = (qidx: number) => {
  form.questions[qidx].options = form.questions[qidx].options || [];
  form.questions[qidx].options.push({ label: '', value: '' });
};
const removeOption = (qidx: number, oidx: number) => {
  form.questions[qidx].options.splice(oidx, 1);
};

const resetForm = () => {
  form.title = '';
  form.subject = '';
  form.difficulty = '';
  form.skill_points = [];
  form.questions = [];
};

const onClose = () => {
  emit('update:visible', false);
  emit('close');
};

const onSubmit = () => {
  formRef.value.validate((valid: boolean) => {
    if (!valid) return;
    emit('submit', { ...form });
    ElMessage.success(isEdit ? '修改成功' : '创建成功');
    onClose();
  });
};

watch(
  () => props.exam,
  (val) => {
    if (isEdit && val) {
      nextTick(() => {
        Object.assign(form, JSON.parse(JSON.stringify(val)));
      });
    } else {
      resetForm();
    }
  },
  { immediate: true }
);
</script>

<style scoped>
.exam-form {
  max-height: 70vh;
  overflow-y: auto;
}
.question-block {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
}
.option-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}
</style> 