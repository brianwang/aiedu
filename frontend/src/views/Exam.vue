<template>
  <div class="exam-container">
    <div class="exam-header">
      <h1>{{ exam.title }}</h1>
      <div v-if="examStatus === 'not_started'" class="exam-status">
        考试未开始，距离开始还有: {{ formatTime(timeLeft) }}
      </div>
      <div v-else-if="examStatus === 'in_progress'" class="exam-status">
        考试进行中，剩余时间: {{ formatTime(timeLeft) }}
      </div>
      <div v-else class="exam-status">考试已结束</div>
    </div>
    <div
      v-for="(question, index) in exam.questions"
      :key="question.id"
      class="question-item"
    >
      <div class="question-header">
        <span class="question-number">第{{ index + 1 }}题</span>
        <span class="question-type">{{ getQuestionType(question.type) }}</span>
        <span class="question-score">({{ question.score }}分)</span>
      </div>

      <div class="question-content" v-html="question.content"></div>

      <!-- 选择题 -->
      <div v-if="question.type === 'choice'" class="options">
        <div
          v-for="(option, optIndex) in question.options"
          :key="optIndex"
          class="option"
        >
          <input
            type="radio"
            :id="`q${index}_opt${optIndex}`"
            :name="`q${index}`"
            :value="option.value"
            v-model="answers[index]"
          />
          <label :for="`q${index}_opt${optIndex}`">{{ option.label }}</label>
        </div>
      </div>

      <!-- 判断题 -->
      <div v-if="question.type === 'true_false'" class="options">
        <div class="option">
          <input
            type="radio"
            :id="`q${index}_true`"
            :name="`q${index}`"
            value="true"
            v-model="answers[index]"
          />
          <label :for="`q${index}_true`">正确</label>
        </div>
        <div class="option">
          <input
            type="radio"
            :id="`q${index}_false`"
            :name="`q${index}`"
            value="false"
            v-model="answers[index]"
          />
          <label :for="`q${index}_false`">错误</label>
        </div>
      </div>

      <!-- 填空题 -->
      <div v-if="question.type === 'fill_blank'">
        <input
          type="text"
          v-model="answers[index]"
          :placeholder="`请输入答案`"
        />
      </div>

      <!-- 问答题 -->
      <div v-if="question.type === 'essay'">
        <textarea
          v-model="answers[index]"
          :placeholder="`请输入您的回答`"
          rows="5"
        ></textarea>
      </div>
    </div>

    <button @click="submitExam" class="submit-btn">提交试卷</button>
  </div>
</template>

<script lang="ts" setup>
import { defineComponent, reactive, ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { submitExamResult } from "../api/exam";

interface Question {
  id: string;
  type: "choice" | "true_false" | "fill_blank" | "essay";
  content: string;
  options?: Array<{ label: string; value: string }>;
  answer: string;
  score: number;
}

interface Exam {
  id: string;
  title: string;
  start_time: string;
  end_time: string;
  duration: number; // 考试时长，单位为秒
  questions: Question[];
}

const router = useRouter();
const authStore = useAuthStore();

const exam = reactive<Exam>({
  id: "",
  title: "",
  questions: [],
  start_time: "",
  end_time: "",
  duration: 0,
});

const timeLeft = ref(0);
const timer = ref<NodeJS.Timeout>();
const examStatus = ref<"not_started" | "in_progress" | "ended">("not_started");

const updateExamStatus = () => {
  const now = new Date();
  const start = new Date(exam.start_time);
  const end = new Date(exam.end_time);

  if (now < start) {
    examStatus.value = "not_started";
    timeLeft.value = Math.floor((start.getTime() - now.getTime()) / 1000);
  } else if (now > end) {
    examStatus.value = "ended";
    timeLeft.value = 0;
  } else {
    examStatus.value = "in_progress";
    timeLeft.value = Math.floor((end.getTime() - now.getTime()) / 1000);
  }
};

const startTimer = () => {
  timer.value = setInterval(() => {
    timeLeft.value--;
    if (timeLeft.value <= 0) {
      clearInterval(timer.value);
      if (examStatus.value === "in_progress") {
        submitExam();
      }
    }
  }, 1000);
};

onMounted(async () => {
  const examId = router.currentRoute.value.params.examId as string;
  try {
    const response = await getExam(examId);
    Object.assign(exam, response.data);
    updateExamStatus();
    if (examStatus.value === "in_progress") {
      startTimer();
    }
  } catch (error) {
    console.error("获取考试失败:", error);
  }
});

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value);
  }
});

const answers = ref<(string | null)[]>();
const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}分${secs}秒`;
};

const getQuestionType = (type: string) => {
  const typeMap: Record<string, string> = {
    choice: "单选题",
    true_false: "判断题",
    fill_blank: "填空题",
    essay: "问答题",
  };
  return typeMap[type] || type;
};

const calculateScore = () => {
  let totalScore = 0;
  exam.questions.forEach((question, index) => {
    if (answers.value[index] === question.answer) {
      totalScore += question.score;
    }
  });
  return totalScore;
};

const submitExam = async () => {
  const score = calculateScore();
  const result = {
    examId: exam.id,
    studentId: authStore.user?.id || "",
    answers: answers.value,
    score,
    totalScore: exam.questions.reduce((sum, q) => sum + q.score, 0),
  };

  try {
    await submitExamResult(result);
    router.push({
      name: "exam-result",
      params: { examId: exam.id },
      query: { score },
    });
  } catch (error) {
    console.error("提交考试失败:", error);
  }
};
</script>

<style scoped>
.exam-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.exam-header {
  margin-bottom: 20px;
}

.exam-status {
  font-size: 16px;
  color: #666;
  margin-top: 10px;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
}

.question-item {
  margin-bottom: 30px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 5px;
}

.question-header {
  margin-bottom: 10px;
  font-weight: bold;
}

.question-number {
  margin-right: 10px;
}

.question-type {
  margin-right: 10px;
  color: #666;
}

.question-content {
  margin-bottom: 15px;
}

.options {
  margin-left: 20px;
}

.option {
  margin: 8px 0;
}

input[type="radio"] {
  margin-right: 8px;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

textarea {
  resize: vertical;
}

.submit-btn {
  display: block;
  width: 200px;
  margin: 30px auto;
  padding: 12px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #3aa876;
}
</style>
