<template>
  <div class="exam-container">
    <h1>{{ exam.title }}</h1>
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

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
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
  questions: Question[];
}

export default defineComponent({
  name: "ExamView",
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();

    const exam = reactive<Exam>({
      id: "exam-001",
      title: "数学期末考试",
      questions: [
        {
          id: "q1",
          type: "choice",
          content: "1. 一元二次方程x²-2x-3=0的解是？",
          options: [
            { label: "A. x=1", value: "1" },
            { label: "B. x=3", value: "3" },
            { label: "C. x=-1", value: "-1" },
            { label: "D. x=3或x=-1", value: "3,-1" },
          ],
          answer: "3,-1",
          score: 5,
        },
        {
          id: "q2",
          type: "true_false",
          content: "2. 判断：π是一个有理数。",
          answer: "false",
          score: 2,
        },
        {
          id: "q3",
          type: "fill_blank",
          content: "3. 函数f(x)=2x+1，当x=3时，f(x)=____。",
          answer: "7",
          score: 3,
        },
        {
          id: "q4",
          type: "essay",
          content: "4. 请简述微积分基本定理的主要内容。",
          answer: "",
          score: 10,
        },
      ],
    });

    const answers = ref<(string | null)[]>(
      Array(exam.questions.length).fill(null)
    );

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

    return {
      exam,
      answers,
      getQuestionType,
      submitExam,
    };
  },
});
</script>

<style scoped>
.exam-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
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
