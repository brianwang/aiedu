<template>
  <div class="question-bank">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <svg viewBox="0 0 24 24" fill="currentColor" class="title-icon">
            <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
          </svg>
          题库练习
        </h1>
        <p class="page-subtitle">选择题目开始你的学习之旅</p>
      </div>
      
      <div class="header-stats">
        <div class="stat-item">
          <div class="stat-number">{{ questions.length }}</div>
          <div class="stat-label">总题目</div>
        </div>
        <div class="stat-item">
          <div class="stat-number">{{ categories.length }}</div>
          <div class="stat-label">学科分类</div>
        </div>
      </div>
    </div>

    <!-- 筛选和操作区域 -->
    <div class="filter-section">
      <div class="filter-controls">
        <div class="filter-group">
          <label class="filter-label">
            <svg viewBox="0 0 24 24" fill="currentColor" class="filter-icon">
              <path d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4-4h-2v10h2V7zM5 15h2V9H5v6zm16-10H3v2h18V5zm-8 4h-2v8h2v-8z"/>
            </svg>
            学科分类
          </label>
          <select v-model="selectedCategory" class="filter-select">
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

        <div class="filter-group">
          <label class="filter-label">
            <svg viewBox="0 0 24 24" fill="currentColor" class="filter-icon">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            难度等级
          </label>
          <select v-model="selectedDifficulty" class="filter-select">
            <option value="">全部难度</option>
            <option value="1">⭐ 入门</option>
            <option value="2">⭐⭐ 基础</option>
            <option value="3">⭐⭐⭐ 中级</option>
            <option value="4">⭐⭐⭐⭐ 困难</option>
            <option value="5">⭐⭐⭐⭐⭐ 专家</option>
          </select>
        </div>

        <div class="filter-group">
          <label class="filter-label">
            <svg viewBox="0 0 24 24" fill="currentColor" class="filter-icon">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
            </svg>
            题目类型
          </label>
          <select v-model="selectedType" class="filter-select">
            <option value="">全部类型</option>
            <option v-for="type in questionTypes" :key="type.value" :value="type.value">
              {{ type.text }}
            </option>
          </select>
        </div>
      </div>

      <div class="action-buttons">
        <button @click="startRandomPractice" class="btn-primary action-btn">
          <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon">
            <path d="M19.07 4.93l-1.41 1.41C19.1 7.79 20 9.79 20 12c0 4.42-3.58 8-8 8s-8-3.58-8-8c0-4.42 3.58-8 8-8 1.57 0 3.04.46 4.28 1.26l1.45-1.45C16.1 2.67 14.13 2 12 2 6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10c0-2.76-1.12-5.26-2.93-7.07z"/>
            <path d="M12.5 7H11v6l5.25 3.15.75-1.23-4.5-2.67z"/>
          </svg>
          随机练习
        </button>
        
        <button @click="showCreateDialog = true" class="btn-secondary action-btn" v-if="canManageQuestions">
          <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
          </svg>
          添加题目
        </button>
      </div>
    </div>

    <!-- 题目练习模式 -->
    <div v-if="practiceMode" class="practice-container">
      <div class="practice-header">
        <div class="practice-progress">
          <div class="progress-info">
            <span class="progress-text">第 {{ currentQuestionIndex + 1 }} 题 / 共 {{ practiceQuestions.length }} 题</span>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: `${((currentQuestionIndex + 1) / practiceQuestions.length) * 100}%` }"></div>
            </div>
          </div>
        </div>
        
        <button @click="exitPractice" class="exit-btn">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
          退出练习
        </button>
      </div>

      <div class="question-card" v-if="currentPracticeQuestion">
        <div class="question-header">
          <div class="question-type">{{ questionTypeText(currentPracticeQuestion.question_type) }}</div>
          <div class="question-difficulty">
            <span v-for="n in currentPracticeQuestion.difficulty" :key="n" class="star">⭐</span>
          </div>
        </div>
        
        <div class="question-content">
          <h3>{{ currentPracticeQuestion.content }}</h3>
        </div>

        <div v-if="hasCurrentOptions" class="question-options">
          <div v-for="(option, index) in currentPracticeQuestion.options" :key="index" 
               class="option-item" 
               :class="{ 
                 selected: userAnswer === option,
                 correct: showResult && option === currentPracticeQuestion.answer,
                 incorrect: showResult && userAnswer === option && option !== currentPracticeQuestion.answer
               }"
               @click="selectOption(option)">
            <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
            <div class="option-text">{{ option }}</div>
          </div>
        </div>

        <div v-else class="answer-input">
          <textarea 
            v-model="userAnswer" 
            placeholder="请输入你的答案..."
            class="answer-textarea"
            :disabled="showResult"
          ></textarea>
        </div>

        <div class="question-actions">
          <button v-if="!showResult" @click="submitAnswer" :disabled="!userAnswer" class="btn-primary">
            提交答案
          </button>
          
          <div v-if="showResult" class="result-section">
            <div class="result-indicator" :class="isCorrect ? 'correct' : 'incorrect'">
              <svg v-if="isCorrect" viewBox="0 0 24 24" fill="currentColor" class="result-icon">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor" class="result-icon">
                <path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"/>
              </svg>
              <span>{{ isCorrect ? '答对了！' : '答错了' }}</span>
            </div>
            
            <div class="correct-answer">
              <strong>正确答案：</strong>{{ currentPracticeQuestion.answer }}
            </div>
            
            <div v-if="currentPracticeQuestion.explanation" class="explanation">
              <strong>解析：</strong>{{ currentPracticeQuestion.explanation }}
            </div>
            
            <button @click="nextQuestion" class="btn-primary next-btn">
              {{ currentQuestionIndex < practiceQuestions.length - 1 ? '下一题' : '完成练习' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 题目列表模式 -->
    <div v-else class="questions-grid">
      <div v-for="question in filteredQuestions" :key="question.id" class="question-item">
        <div class="question-card-small">
          <div class="question-meta">
            <span class="question-type-badge" :class="question.question_type">
              {{ questionTypeText(question.question_type) }}
            </span>
            <div class="question-difficulty-stars">
              <span v-for="n in question.difficulty" :key="n" class="star">⭐</span>
            </div>
          </div>
          
          <div class="question-preview">
            <h4>{{ question.content.substring(0, 80) }}{{ question.content.length > 80 ? '...' : '' }}</h4>
          </div>
          
          <div class="question-actions-small">
            <button @click="practiceQuestion(question)" class="btn-primary practice-btn">
              <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon-small">
                <path d="M8 5v14l11-7z"/>
              </svg>
              开始练习
            </button>
            
            <button v-if="canManageQuestions" @click="editQuestion(question)" class="btn-secondary edit-btn">
              <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon-small">
                <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
              </svg>
              编辑
            </button>
            
            <button v-if="canManageQuestions" @click="deleteQuestionConfirm(question.id)" class="btn-danger delete-btn">
              <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon-small">
                <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
              </svg>
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 创建/编辑题目模态框 -->
    <div v-if="showCreateDialog || currentQuestion" class="modal-overlay" @click="cancelEdit">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h2 class="modal-title">{{ currentQuestion ? "编辑题目" : "新增题目" }}</h2>
          <button @click="cancelEdit" class="modal-close">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="submitQuestion" class="modal-form">
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">题型</label>
              <select v-model="questionForm.question_type" class="form-select">
                <option v-for="type in questionTypes" :key="type.value" :value="type.value">
                  {{ type.text }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">难度</label>
              <select v-model="questionForm.difficulty" class="form-select">
                <option value="1">⭐ 入门</option>
                <option value="2">⭐⭐ 基础</option>
                <option value="3">⭐⭐⭐ 中级</option>
                <option value="4">⭐⭐⭐⭐ 困难</option>
                <option value="5">⭐⭐⭐⭐⭐ 专家</option>
              </select>
            </div>
            
            <div class="form-group">
              <label class="form-label">分类</label>
              <select v-model="questionForm.category_id" class="form-select">
                <option value="">无分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">题目内容</label>
            <textarea v-model="questionForm.content" class="form-textarea" rows="4" placeholder="请输入题目内容..."></textarea>
          </div>
          
          <div v-if="hasOptions" class="form-group">
            <label class="form-label">选项</label>
            <div class="options-container">
              <div v-for="(option, index) in questionForm.options" :key="index" class="option-input-group">
                <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
                <input v-model="questionForm.options[index]" class="option-input" placeholder="请输入选项内容..." />
                <button type="button" @click="removeOption(index)" class="btn-danger remove-option" v-if="questionForm.options.length > 2">
                  <svg viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                  </svg>
                </button>
              </div>
              <button type="button" @click="addOption" class="btn-secondary add-option">
                <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon-small">
                  <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
                </svg>
                添加选项
              </button>
            </div>
          </div>
          
          <div class="form-group">
            <label class="form-label">标准答案</label>
            <textarea v-model="questionForm.answer" class="form-textarea" rows="2" placeholder="请输入标准答案..."></textarea>
          </div>
          
          <div class="form-group">
            <label class="form-label">解析 (可选)</label>
            <textarea v-model="questionForm.explanation" class="form-textarea" rows="3" placeholder="请输入解题解析..."></textarea>
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="cancelEdit" class="btn-secondary">取消</button>
            <button type="submit" class="btn-primary">{{ currentQuestion ? "更新" : "创建" }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import {
  createQuestion,
  getQuestion,
  updateQuestion,
  deleteQuestion,
  getQuestionsByCategory,
  getCategories,
} from "@/api/question";

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
    const questions = ref<Question[]>([]);
    const categories = ref<Category[]>([]);
    const selectedCategory = ref("");
    const selectedDifficulty = ref("");
    const selectedType = ref("");
    const showCreateDialog = ref(false);
    const currentQuestion = ref<Question | null>(null);
    
    // 练习模式相关状态
    const practiceMode = ref(false);
    const practiceQuestions = ref<Question[]>([]);
    const currentQuestionIndex = ref(0);
    const userAnswer = ref("");
    const showResult = ref(false);
    const isCorrect = ref(false);

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

    const canManageQuestions = computed(() => {
      // 这里可以根据用户权限判断是否可以管理题目
      return true;
    });

    const hasOptions = computed(() => {
      return ["single_choice", "multiple_choice"].includes(
        questionForm.value.question_type
      );
    });

    const hasCurrentOptions = computed(() => {
      if (!currentPracticeQuestion.value) return false;
      return ["single_choice", "multiple_choice"].includes(
        currentPracticeQuestion.value.question_type
      );
    });

    const currentPracticeQuestion = computed(() => {
      if (!practiceQuestions.value.length || currentQuestionIndex.value >= practiceQuestions.value.length) {
        return null;
      }
      return practiceQuestions.value[currentQuestionIndex.value];
    });

    const filteredQuestions = computed(() => {
      let filtered = questions.value;
      
      if (selectedCategory.value) {
        filtered = filtered.filter(q => q.category_id?.toString() === selectedCategory.value);
      }
      
      if (selectedDifficulty.value) {
        filtered = filtered.filter(q => q.difficulty.toString() === selectedDifficulty.value);
      }
      
      if (selectedType.value) {
        filtered = filtered.filter(q => q.question_type === selectedType.value);
      }
      
      return filtered;
    });

    const questionTypeText = (type: string) => {
      const found = questionTypes.find((t) => t.value === type);
      return found ? found.text : type;
    };

    const fetchQuestions = async () => {
      try {
        const response = await getQuestionsByCategory();
        questions.value = response.data;
      } catch (error) {
        console.error('Failed to fetch questions:', error);
        // 模拟数据用于演示
        questions.value = [
          {
            id: 1,
            question_type: "single_choice",
            content: "Vue.js 是什么？",
            options: ["一个JavaScript框架", "一个CSS框架", "一个HTML模板", "一个数据库"],
            answer: "一个JavaScript框架",
            explanation: "Vue.js是一个用于构建用户界面的渐进式JavaScript框架",
            difficulty: 2,
            category_id: 1
          },
          {
            id: 2,
            question_type: "multiple_choice",
            content: "以下哪些是Vue.js的特性？",
            options: ["响应式数据绑定", "组件系统", "虚拟DOM", "服务端渲染"],
            answer: "响应式数据绑定,组件系统,虚拟DOM",
            explanation: "Vue.js具有响应式数据绑定、组件系统和虚拟DOM等特性",
            difficulty: 3,
            category_id: 1
          }
        ];
      }
    };

    const fetchCategories = async () => {
      try {
        const response = await getCategories();
        categories.value = response.data;
      } catch (error) {
        console.error('Failed to fetch categories:', error);
        // 模拟数据用于演示
        categories.value = [
          { id: 1, name: "前端开发" },
          { id: 2, name: "后端开发" },
          { id: 3, name: "数据库" }
        ];
      }
    };

    const startRandomPractice = () => {
      const shuffled = [...filteredQuestions.value].sort(() => Math.random() - 0.5);
      practiceQuestions.value = shuffled.slice(0, Math.min(10, shuffled.length));
      practiceMode.value = true;
      currentQuestionIndex.value = 0;
      userAnswer.value = "";
      showResult.value = false;
    };

    const practiceQuestion = (question: Question) => {
      practiceQuestions.value = [question];
      practiceMode.value = true;
      currentQuestionIndex.value = 0;
      userAnswer.value = "";
      showResult.value = false;
    };

    const exitPractice = () => {
      practiceMode.value = false;
      practiceQuestions.value = [];
      currentQuestionIndex.value = 0;
      userAnswer.value = "";
      showResult.value = false;
    };

    const selectOption = (option: string) => {
      if (!showResult.value) {
        userAnswer.value = option;
      }
    };

    const submitAnswer = () => {
      if (!currentPracticeQuestion.value || !userAnswer.value) return;
      
      isCorrect.value = userAnswer.value.trim().toLowerCase() === 
                       currentPracticeQuestion.value.answer.trim().toLowerCase();
      showResult.value = true;
    };

    const nextQuestion = () => {
      if (currentQuestionIndex.value < practiceQuestions.value.length - 1) {
        currentQuestionIndex.value++;
        userAnswer.value = "";
        showResult.value = false;
      } else {
        exitPractice();
      }
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

    const deleteQuestionConfirm = async (id: number) => {
      if (confirm("确定删除此题目吗？此操作无法撤销。")) {
        try {
          await deleteQuestion(id);
          await fetchQuestions();
        } catch (error) {
          console.error('Failed to delete question:', error);
          alert('删除失败，请稍后重试');
        }
      }
    };

    const submitQuestion = async () => {
      try {
        const data = {
          question_type: questionForm.value.question_type,
          content: questionForm.value.content,
          answer: questionForm.value.answer,
          difficulty: questionForm.value.difficulty,
          category_id: questionForm.value.category_id,
          explanation: questionForm.value.explanation || undefined,
          options: hasOptions.value ? questionForm.value.options : undefined,
        };

        if (currentQuestion.value) {
          await updateQuestion(currentQuestion.value.id, data);
        } else {
          await createQuestion(data);
        }

        resetForm();
        await fetchQuestions();
      } catch (error) {
        console.error('Failed to submit question:', error);
        alert('保存失败，请稍后重试');
      }
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
      selectedDifficulty,
      selectedType,
      showCreateDialog,
      currentQuestion,
      questionTypes,
      questionForm,
      canManageQuestions,
      hasOptions,
      hasCurrentOptions,
      filteredQuestions,
      practiceMode,
      practiceQuestions,
      currentQuestionIndex,
      currentPracticeQuestion,
      userAnswer,
      showResult,
      isCorrect,
      questionTypeText,
      startRandomPractice,
      practiceQuestion,
      exitPractice,
      selectOption,
      submitAnswer,
      nextQuestion,
      addOption,
      removeOption,
      editQuestion,
      deleteQuestionConfirm,
      submitQuestion,
      cancelEdit,
    };
  },
});
</script>

<style scoped>
.question-bank {
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.header-content {
  flex: 1;
}

.page-title {
  display: flex;
  align-items: center;
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.title-icon {
  width: 32px;
  height: 32px;
  margin-right: var(--spacing-md);
  color: var(--primary-color);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin: 0;
}

.header-stats {
  display: flex;
  gap: var(--spacing-xl);
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
  line-height: 1;
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-top: var(--spacing-xs);
}

/* 筛选区域 */
.filter-section {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.filter-controls {
  display: flex;
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.filter-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  font-size: 0.875rem;
}

.filter-icon {
  width: 16px;
  height: 16px;
  margin-right: var(--spacing-xs);
  color: var(--text-secondary);
}

.filter-select {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: border-color 0.2s ease;
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary-color);
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* 练习模式 */
.practice-container {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
}

.practice-header {
  background: var(--gradient-primary);
  color: white;
  padding: var(--spacing-lg) var(--spacing-xl);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-info {
  flex: 1;
}

.progress-text {
  font-weight: 500;
  margin-bottom: var(--spacing-sm);
  display: block;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: white;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.exit-btn {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  cursor: pointer;
  transition: background 0.2s ease;
}

.exit-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.exit-btn svg {
  width: 16px;
  height: 16px;
}

.question-card {
  padding: var(--spacing-xxl);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
}

.question-type {
  background: var(--primary-color);
  color: white;
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
}

.question-difficulty {
  display: flex;
  gap: var(--spacing-xs);
}

.star {
  font-size: 1.2rem;
}

.question-content {
  margin-bottom: var(--spacing-xxl);
}

.question-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.5;
}

.question-options {
  margin-bottom: var(--spacing-xxl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.option-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-lg);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--bg-primary);
}

.option-item:hover {
  border-color: var(--primary-color);
  background: rgba(74, 144, 226, 0.05);
}

.option-item.selected {
  border-color: var(--primary-color);
  background: rgba(74, 144, 226, 0.1);
}

.option-item.correct {
  border-color: var(--success-color);
  background: rgba(39, 174, 96, 0.1);
}

.option-item.incorrect {
  border-color: var(--danger-color);
  background: rgba(231, 76, 60, 0.1);
}

.option-label {
  width: 32px;
  height: 32px;
  background: var(--bg-accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--text-primary);
  margin-right: var(--spacing-lg);
  flex-shrink: 0;
}

.option-item.selected .option-label {
  background: var(--primary-color);
  color: white;
}

.option-item.correct .option-label {
  background: var(--success-color);
  color: white;
}

.option-item.incorrect .option-label {
  background: var(--danger-color);
  color: white;
}

.option-text {
  flex: 1;
  font-size: 1.1rem;
  color: var(--text-primary);
}

.answer-input {
  margin-bottom: var(--spacing-xxl);
}

.answer-textarea {
  width: 100%;
  min-height: 120px;
  padding: var(--spacing-lg);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-lg);
  resize: vertical;
  font-family: inherit;
  font-size: 1rem;
  line-height: 1.5;
}

.answer-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.question-actions {
  display: flex;
  justify-content: center;
}

.result-section {
  width: 100%;
  text-align: center;
}

.result-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  font-size: 1.2rem;
  font-weight: 600;
}

.result-indicator.correct {
  background: rgba(39, 174, 96, 0.1);
  color: var(--success-color);
}

.result-indicator.incorrect {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
}

.result-icon {
  width: 24px;
  height: 24px;
}

.correct-answer {
  margin-bottom: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-accent);
  border-radius: var(--radius-md);
  color: var(--text-primary);
}

.explanation {
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: rgba(74, 144, 226, 0.05);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  text-align: left;
}

.next-btn {
  margin-top: var(--spacing-md);
}

/* 题目网格 */
.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: var(--spacing-lg);
}

.question-item {
  height: 100%;
}

.question-card-small {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
}

.question-card-small:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.question-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.question-type-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
  color: white;
}

.question-type-badge.single_choice {
  background: var(--primary-color);
}

.question-type-badge.multiple_choice {
  background: var(--secondary-color);
}

.question-type-badge.fill_blank {
  background: var(--success-color);
}

.question-type-badge.short_answer {
  background: var(--warning-color);
}

.question-type-badge.essay {
  background: var(--danger-color);
}

.question-difficulty-stars {
  display: flex;
  gap: 2px;
}

.question-preview {
  flex: 1;
  margin-bottom: var(--spacing-lg);
}

.question-preview h4 {
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--text-primary);
  line-height: 1.4;
  margin: 0;
}

.question-actions-small {
  display: flex;
  gap: var(--spacing-sm);
}

.practice-btn, .edit-btn, .delete-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.practice-btn {
  background: var(--gradient-primary);
  color: white;
}

.practice-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.edit-btn {
  background: var(--bg-primary);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
}

.edit-btn:hover {
  background: var(--primary-color);
  color: white;
}

.delete-btn {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
  border: 1px solid rgba(231, 76, 60, 0.3);
}

.delete-btn:hover {
  background: var(--danger-color);
  color: white;
}

.btn-icon-small {
  width: 14px;
  height: 14px;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: var(--spacing-md);
}

.modal-container {
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: var(--shadow-xl);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-xl);
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.modal-close:hover {
  background: var(--bg-accent);
  color: var(--text-primary);
}

.modal-close svg {
  width: 20px;
  height: 20px;
}

.modal-form {
  padding: var(--spacing-xl);
  max-height: calc(90vh - 120px);
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.form-group {
  margin-bottom: var(--spacing-lg);
}

.form-label {
  display: block;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.form-select, .form-textarea {
  width: 100%;
  padding: var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.2s ease;
  background: var(--bg-primary);
}

.form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: var(--primary-color);
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.option-input-group {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.option-label {
  width: 32px;
  height: 32px;
  background: var(--bg-accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: var(--text-primary);
  flex-shrink: 0;
}

.option-input {
  flex: 1;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  font-family: inherit;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.option-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.remove-option {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.remove-option:hover {
  background: var(--danger-color);
  color: white;
}

.remove-option svg {
  width: 16px;
  height: 16px;
}

.add-option {
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid var(--primary-color);
  background: transparent;
  color: var(--primary-color);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-option:hover {
  background: var(--primary-color);
  color: white;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .page-header {
    flex-direction: column;
    gap: var(--spacing-lg);
    text-align: center;
  }

  .filter-section {
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .filter-controls {
    justify-content: center;
  }
}

@media (max-width: 768px) {
  .questions-grid {
    grid-template-columns: 1fr;
  }

  .filter-controls {
    flex-direction: column;
    width: 100%;
  }

  .filter-group {
    min-width: auto;
  }

  .action-buttons {
    flex-direction: column;
    width: 100%;
  }

  .question-actions-small {
    flex-direction: column;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .modal-container {
    margin: var(--spacing-sm);
  }

  .option-input-group {
    flex-direction: column;
    align-items: stretch;
  }

  .option-label {
    align-self: flex-start;
  }
}
</style>
