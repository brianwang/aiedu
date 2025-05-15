<template>
  <div class="question-bank">
    <h1>题库管理系统</h1>

    <div class="actions">
      <button @click="showCreateDialog = true">新增题目</button>
      <select v-model="selectedCategory">
        <option value="">全部分类</option>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
    </div>

    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>题目内容</th>
          <th>题型</th>
          <th>难度</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="question in filteredQuestions" :key="question.id">
          <td>{{ question.id }}</td>
          <td>{{ question.content }}</td>
          <td>{{ questionTypeText(question.question_type) }}</td>
          <td>{{ question.difficulty }}</td>
          <td>
            <button @click="editQuestion(question)">编辑</button>
            <button @click="deleteQuestion(question.id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 创建/编辑题目对话框 -->
    <dialog v-if="showCreateDialog || currentQuestion">
      <h2>{{ currentQuestion ? "编辑题目" : "新增题目" }}</h2>
      <form @submit.prevent="submitQuestion">
        <div>
          <label>题型:</label>
          <select v-model="questionForm.question_type">
            <option
              v-for="type in questionTypes"
              :key="type.value"
              :value="type.value"
            >
              {{ type.text }}
            </option>
          </select>
        </div>
        <div>
          <label>题目内容:</label>
          <textarea v-model="questionForm.content"></textarea>
        </div>
        <div v-if="hasOptions">
          <label>选项:</label>
          <div v-for="(option, index) in questionForm.options" :key="index">
            <input v-model="questionForm.options[index]" />
            <button @click="removeOption(index)">删除</button>
          </div>
          <button @click="addOption">添加选项</button>
        </div>
        <div>
          <label>答案:</label>
          <textarea v-model="questionForm.answer"></textarea>
        </div>
        <div>
          <label>解析:</label>
          <textarea v-model="questionForm.explanation"></textarea>
        </div>
        <div>
          <label>难度:</label>
          <input
            type="number"
            v-model="questionForm.difficulty"
            min="1"
            max="5"
          />
        </div>
        <div>
          <label>分类:</label>
          <select v-model="questionForm.category_id">
            <option value="">无分类</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
        <button type="submit">提交</button>
        <button type="button" @click="cancelEdit">取消</button>
      </form>
    </dialog>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import { useApi } from "@/composables/useApi";

interface Question {
  id: number;
  question_type: string;
  content: string;
  options?: string[];
  answer: string;
  explanation?: string;
  difficulty: number;
  category_id?: number;
}

interface Category {
  id: number;
  name: string;
}

export default defineComponent({
  name: "QuestionBank",
  setup() {
    const { get, post, put, del } = useApi();
    const questions = ref<Question[]>([]);
    const categories = ref<Category[]>([]);
    const selectedCategory = ref("");
    const showCreateDialog = ref(false);
    const currentQuestion = ref<Question | null>(null);

    const questionTypes = [
      { value: "single_choice", text: "单选题" },
      { value: "multiple_choice", text: "多选题" },
      { value: "fill_blank", text: "填空题" },
      { value: "short_answer", text: "简答题" },
      { value: "essay", text: "论述题" },
    ];

    const questionForm = ref({
      question_type: "single_choice",
      content: "",
      options: ["", ""],
      answer: "",
      explanation: "",
      difficulty: 1,
      category_id: undefined as number | undefined,
    });

    const hasOptions = computed(() => {
      return ["single_choice", "multiple_choice"].includes(
        questionForm.value.question_type
      );
    });

    const filteredQuestions = computed(() => {
      if (!selectedCategory.value) return questions.value;
      return questions.value.filter(
        (q) => q.category_id?.toString() === selectedCategory.value
      );
    });

    const questionTypeText = (type: string) => {
      const found = questionTypes.find((t) => t.value === type);
      return found ? found.text : type;
    };

    const fetchQuestions = async () => {
      questions.value = await get("/questions/");
    };

    const fetchCategories = async () => {
      categories.value = await get("/questions/categories/");
    };

    const addOption = () => {
      questionForm.value.options.push("");
    };

    const removeOption = (index: number) => {
      questionForm.value.options.splice(index, 1);
    };

    const editQuestion = (question: Question) => {
      currentQuestion.value = question;
      questionForm.value = {
        question_type: question.question_type,
        content: question.content,
        options: question.options || ["", ""],
        answer: question.answer,
        explanation: question.explanation || "",
        difficulty: question.difficulty,
        category_id: question.category_id,
      };
    };

    const deleteQuestion = async (id: number) => {
      if (confirm("确定删除此题?")) {
        await del(`/questions/${id}`);
        await fetchQuestions();
      }
    };

    const submitQuestion = async () => {
      const data = { ...questionForm.value };
      if (!hasOptions.value) {
        delete data.options;
      }

      if (currentQuestion.value) {
        await put(`/questions/${currentQuestion.value.id}`, data);
      } else {
        await post("/questions/", data);
      }

      resetForm();
      await fetchQuestions();
    };

    const cancelEdit = () => {
      resetForm();
    };

    const resetForm = () => {
      currentQuestion.value = null;
      showCreateDialog.value = false;
      questionForm.value = {
        question_type: "single_choice",
        content: "",
        options: ["", ""],
        answer: "",
        explanation: "",
        difficulty: 1,
        category_id: undefined,
      };
    };

    onMounted(async () => {
      await Promise.all([fetchQuestions(), fetchCategories()]);
    });

    return {
      questions,
      categories,
      selectedCategory,
      showCreateDialog,
      currentQuestion,
      questionTypes,
      questionForm,
      hasOptions,
      filteredQuestions,
      questionTypeText,
      addOption,
      removeOption,
      editQuestion,
      deleteQuestion,
      submitQuestion,
      cancelEdit,
    };
  },
});
</script>

<style scoped>
.question-bank {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

dialog {
  width: 600px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

form div {
  margin-bottom: 10px;
}

label {
  display: inline-block;
  width: 80px;
}

textarea,
input[type="text"],
select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  margin-right: 5px;
  padding: 5px 10px;
  cursor: pointer;
}
</style>
