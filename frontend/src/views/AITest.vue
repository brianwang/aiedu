<template>
  <div class="ai-test">
    <div class="test-header">
      <h1>AI功能测试页面</h1>
      <p>用于测试各种AI功能是否正常工作</p>
    </div>

    <div class="test-sections">
      <!-- 学习计划测试 -->
      <div class="test-section">
        <h2>学习计划测试</h2>
        <button @click="testStudyPlan" :disabled="loading" class="test-btn">
          测试学习计划
        </button>
        <div v-if="studyPlanResult" class="test-result">
          <h3>测试结果：</h3>
          <pre>{{ JSON.stringify(studyPlanResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- 能力评估测试 -->
      <div class="test-section">
        <h2>能力评估测试</h2>
        <button @click="testAbilityAssessment" :disabled="loading" class="test-btn">
          测试能力评估
        </button>
        <div v-if="abilityResult" class="test-result">
          <h3>测试结果：</h3>
          <pre>{{ JSON.stringify(abilityResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- 学习风格测试 -->
      <div class="test-section">
        <h2>学习风格测试</h2>
        <button @click="testLearningStyle" :disabled="loading" class="test-btn">
          测试学习风格
        </button>
        <div v-if="styleResult" class="test-result">
          <h3>测试结果：</h3>
          <pre>{{ JSON.stringify(styleResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- 题目推荐测试 -->
      <div class="test-section">
        <h2>题目推荐测试</h2>
        <button @click="testQuestionRecommendation" :disabled="loading" class="test-btn">
          测试题目推荐
        </button>
        <div v-if="recommendationResult" class="test-result">
          <h3>测试结果：</h3>
          <pre>{{ JSON.stringify(recommendationResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- 学习模式测试 -->
      <div class="test-section">
        <h2>学习模式测试</h2>
        <button @click="testLearningPattern" :disabled="loading" class="test-btn">
          测试学习模式
        </button>
        <div v-if="patternResult" class="test-result">
          <h3>测试结果：</h3>
          <pre>{{ JSON.stringify(patternResult, null, 2) }}</pre>
        </div>
      </div>

      <!-- 难度分析测试 -->
      <div class="test-section">
        <h2>难度分析测试</h2>
        <button @click="testDifficultyAnalysis" :disabled="loading" class="test-btn">
          测试难度分析
        </button>
        <div v-if="difficultyResult" class="test-result">
          <h3>测试结果：</h3>
          <pre>{{ JSON.stringify(difficultyResult, null, 2) }}</pre>
        </div>
      </div>
    </div>

    <!-- 错误信息显示 -->
    <div v-if="errorMessage" class="error-message">
      <h3>错误信息：</h3>
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useApi } from "@/composables/useApi";
import { 
  getStudyPlan, 
  getRecommendedQuestions, 
  getLearningPattern,
  getDifficultyAnalysis
} from "@/api/ai";

const api = useApi();
const loading = ref(false);
const errorMessage = ref("");

// 测试结果
const studyPlanResult = ref(null);
const abilityResult = ref(null);
const styleResult = ref(null);
const recommendationResult = ref(null);
const patternResult = ref(null);
const difficultyResult = ref(null);

const clearError = () => {
  errorMessage.value = "";
};

const testStudyPlan = async () => {
  loading.value = true;
  clearError();
  try {
    const response = await getStudyPlan();
    studyPlanResult.value = response.data;
    console.log("学习计划测试成功:", response.data);
  } catch (error: any) {
    errorMessage.value = `学习计划测试失败: ${error.message}`;
    console.error("学习计划测试失败:", error);
  } finally {
    loading.value = false;
  }
};

const testAbilityAssessment = async () => {
  loading.value = true;
  clearError();
  try {
    const response = await api.get("/ai/user-ability-assessment");
    abilityResult.value = response.data;
    console.log("能力评估测试成功:", response.data);
  } catch (error: any) {
    errorMessage.value = `能力评估测试失败: ${error.message}`;
    console.error("能力评估测试失败:", error);
  } finally {
    loading.value = false;
  }
};

const testLearningStyle = async () => {
  loading.value = true;
  clearError();
  try {
    const response = await api.get("/ai/user-learning-style");
    styleResult.value = response.data;
    console.log("学习风格测试成功:", response.data);
  } catch (error: any) {
    errorMessage.value = `学习风格测试失败: ${error.message}`;
    console.error("学习风格测试失败:", error);
  } finally {
    loading.value = false;
  }
};

const testQuestionRecommendation = async () => {
  loading.value = true;
  clearError();
  try {
    const response = await getRecommendedQuestions("数学", 3);
    recommendationResult.value = response.data;
    console.log("题目推荐测试成功:", response.data);
  } catch (error: any) {
    errorMessage.value = `题目推荐测试失败: ${error.message}`;
    console.error("题目推荐测试失败:", error);
  } finally {
    loading.value = false;
  }
};

const testLearningPattern = async () => {
  loading.value = true;
  clearError();
  try {
    const response = await getLearningPattern();
    patternResult.value = response.data;
    console.log("学习模式测试成功:", response.data);
  } catch (error: any) {
    errorMessage.value = `学习模式测试失败: ${error.message}`;
    console.error("学习模式测试失败:", error);
  } finally {
    loading.value = false;
  }
};

const testDifficultyAnalysis = async () => {
  loading.value = true;
  clearError();
  try {
    const response = await getDifficultyAnalysis();
    difficultyResult.value = response.data;
    console.log("难度分析测试成功:", response.data);
  } catch (error: any) {
    errorMessage.value = `难度分析测试失败: ${error.message}`;
    console.error("难度分析测试失败:", error);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.ai-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.test-header {
  text-align: center;
  margin-bottom: 40px;
}

.test-header h1 {
  color: var(--text-primary);
  margin-bottom: 10px;
}

.test-header p {
  color: var(--text-secondary);
}

.test-sections {
  display: grid;
  gap: 30px;
}

.test-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.test-section h2 {
  color: var(--text-primary);
  margin-bottom: 20px;
}

.test-btn {
  padding: 12px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.test-btn:hover {
  background: var(--primary-hover);
}

.test-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.test-result {
  margin-top: 20px;
  padding: 15px;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.test-result h3 {
  color: var(--text-primary);
  margin-bottom: 10px;
}

.test-result pre {
  background: white;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.9rem;
  line-height: 1.4;
  color: var(--text-primary);
}

.error-message {
  margin-top: 30px;
  padding: 20px;
  background: #fee;
  border: 1px solid #fcc;
  border-radius: 8px;
  color: #c33;
}

.error-message h3 {
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  .ai-test {
    padding: 15px;
  }
  
  .test-section {
    padding: 20px;
  }
  
  .test-result pre {
    font-size: 0.8rem;
  }
}
</style> 