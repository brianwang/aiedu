<template>
  <div class="ai-study">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">
          <svg viewBox="0 0 24 24" fill="currentColor" class="title-icon">
            <path
              d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"
            />
          </svg>
          AI智能学习
        </h1>
        <p class="page-subtitle">基于AI的个性化学习体验</p>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="ai-content">
      <!-- 学习计划卡片 -->
      <div class="study-plan-card">
        <div class="card-header">
          <h2>个性化学习计划</h2>
          <button
            @click="refreshStudyPlan"
            class="refresh-btn"
            :disabled="loading"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
              />
            </svg>
          </button>
        </div>

        <div v-if="loading" class="loading">
          <div class="spinner"></div>
          <p>正在生成学习计划...</p>
        </div>

        <div v-else-if="studyPlan" class="plan-content">
          <div class="plan-summary">
            <div class="summary-item">
              <div class="summary-number">
                {{ studyPlan.progress_summary?.total_questions || 0 }}
              </div>
              <div class="summary-label">总题目数</div>
            </div>
            <div class="summary-item">
              <div class="summary-number">
                {{ studyPlan.progress_summary?.accuracy || 0 }}%
              </div>
              <div class="summary-label">正确率</div>
            </div>
            <div class="summary-item">
              <div class="summary-number">
                {{ studyPlan.progress_summary?.total_study_time || 0 }}分钟
              </div>
              <div class="summary-label">学习时长</div>
            </div>
          </div>

          <div class="daily-goals">
            <h3>今日目标</h3>
            <div class="goals-grid">
              <div class="goal-item">
                <div class="goal-icon">📝</div>
                <div class="goal-content">
                  <div class="goal-number">
                    {{ studyPlan.daily_goal?.questions || 20 }}
                  </div>
                  <div class="goal-label">题目数量</div>
                </div>
              </div>
              <div class="goal-item">
                <div class="goal-icon">⏰</div>
                <div class="goal-content">
                  <div class="goal-number">
                    {{ studyPlan.daily_goal?.study_time || 60 }}
                  </div>
                  <div class="goal-label">学习时间(分钟)</div>
                </div>
              </div>
              <div class="goal-item">
                <div class="goal-icon">🎯</div>
                <div class="goal-content">
                  <div class="goal-number">
                    {{ studyPlan.daily_goal?.accuracy_target || 80 }}%
                  </div>
                  <div class="goal-label">目标正确率</div>
                </div>
              </div>
            </div>
          </div>

          <div class="recommendations">
            <h3>AI建议</h3>
            <div class="recommendation-list">
              <div
                v-if="studyPlan.recommendations?.focus_subjects?.length"
                class="recommendation-item"
              >
                <div class="rec-icon">🎯</div>
                <div class="rec-content">
                  <strong>重点关注学科：</strong>
                  {{ studyPlan.recommendations.focus_subjects.join("、") }}
                </div>
              </div>
              <div class="recommendation-item">
                <div class="rec-icon">📈</div>
                <div class="rec-content">
                  <strong>难度调整：</strong>
                  {{
                    getDifficultyText(
                      studyPlan.recommendations?.difficulty_adjustment
                    )
                  }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 智能推荐题目 -->
      <div class="recommended-questions">
        <div class="section-header">
          <h2>智能推荐题目</h2>
          <div class="filter-controls">
            <select v-model="selectedSubject" class="filter-select">
              <option value="">全学科</option>
              <option
                v-for="subject in subjects"
                :key="subject"
                :value="subject"
              >
                {{ subject }}
              </option>
            </select>
            <button
              @click="getRecommendedQuestions"
              class="btn-primary"
              :disabled="loading"
            >
              获取推荐
            </button>
          </div>
        </div>

        <div v-if="recommendedQuestions.length" class="questions-list">
          <div
            v-for="question in recommendedQuestions"
            :key="question.id"
            class="question-item"
          >
            <div class="question-header">
              <span class="question-type">{{
                getQuestionTypeText(question.question_type)
              }}</span>
              <div class="question-difficulty">
                <span v-for="n in question.difficulty" :key="n" class="star"
                  >⭐</span
                >
              </div>
            </div>
            <div class="question-content">{{ question.content }}</div>
            <div class="question-actions">
              <button @click="startPractice(question)" class="btn-secondary">
                开始练习
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="!loading" class="empty-state">
          <div class="empty-icon">🤖</div>
          <p>点击"获取推荐"开始AI智能推荐</p>
        </div>
      </div>

      <!-- 学习模式分析 -->
      <div class="learning-pattern">
        <div class="section-header">
          <h2>学习模式分析</h2>
          <button
            @click="analyzePattern"
            class="btn-secondary"
            :disabled="loading"
          >
            分析模式
          </button>
        </div>

        <div v-if="learningPattern" class="pattern-content">
          <div class="pattern-grid">
            <div class="pattern-card">
              <h3>学习效率</h3>
              <div class="pattern-value">
                {{ learningPattern.learning_efficiency || 0 }}
              </div>
              <div class="pattern-label">题目/分钟</div>
            </div>
            <div class="pattern-card">
              <h3>学习会话</h3>
              <div class="pattern-value">
                {{ learningPattern.total_study_sessions || 0 }}
              </div>
              <div class="pattern-label">总次数</div>
            </div>
            <div class="pattern-card">
              <h3>平均时长</h3>
              <div class="pattern-value">
                {{ learningPattern.average_session_duration || 0 }}
              </div>
              <div class="pattern-label">分钟/次</div>
            </div>
          </div>

          <div
            v-if="learningPattern.subject_preference"
            class="subject-preference"
          >
            <h3>学科偏好</h3>
            <div class="preference-list">
              <div
                v-for="(time, subject) in learningPattern.subject_preference"
                :key="subject"
                class="preference-item"
              >
                <div class="preference-subject">{{ subject }}</div>
                <div class="preference-time">{{ time }}分钟</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useApi } from "@/composables/useApi";

const api = useApi();
const loading = ref(false);
const studyPlan = ref(null);
const recommendedQuestions = ref([]);
const learningPattern = ref(null);
const selectedSubject = ref("");
const subjects = ["数学", "英语", "物理", "化学", "生物"];

const getDifficultyText = (difficulty: string) => {
  const texts = {
    increase: "建议增加难度",
    decrease: "建议降低难度",
    maintain: "保持当前难度",
  };
  return texts[difficulty] || "保持当前难度";
};

const getQuestionTypeText = (type: string) => {
  const types = {
    single_choice: "单选题",
    multiple_choice: "多选题",
    fill_blank: "填空题",
    short_answer: "简答题",
    essay: "论述题",
  };
  return types[type] || type;
};

const refreshStudyPlan = async () => {
  loading.value = true;
  try {
    const response = await api.get("/ai/study-plan");
    studyPlan.value = response.data;
  } catch (error) {
    console.error("获取学习计划失败:", error);
  } finally {
    loading.value = false;
  }
};

const getRecommendedQuestions = async () => {
  loading.value = true;
  try {
    const params = { count: 5 };
    if (selectedSubject.value) {
      params.subject = selectedSubject.value;
    }
    const response = await api.get("/ai/recommendations", { params });
    recommendedQuestions.value = response.data;
  } catch (error) {
    console.error("获取推荐题目失败:", error);
  } finally {
    loading.value = false;
  }
};

const analyzePattern = async () => {
  loading.value = true;
  try {
    const response = await api.get("/ai/learning-pattern");
    learningPattern.value = response.data;
  } catch (error) {
    console.error("分析学习模式失败:", error);
  } finally {
    loading.value = false;
  }
};

const startPractice = (question: any) => {
  // 跳转到练习页面
  console.log("开始练习:", question);
};

onMounted(() => {
  refreshStudyPlan();
});
</script>

<style scoped>
.ai-study {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
  text-align: center;
}

.page-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 10px;
}

.title-icon {
  width: 32px;
  height: 32px;
  color: var(--primary-color);
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
}

.ai-content {
  display: grid;
  gap: 30px;
}

.study-plan-card,
.recommended-questions,
.learning-pattern {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header,
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h2,
.section-header h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0;
}

.refresh-btn {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background-color 0.2s;
}

.refresh-btn:hover {
  background-color: var(--bg-hover);
}

.loading {
  text-align: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--bg-secondary);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.plan-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-item {
  text-align: center;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.summary-number {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 5px;
}

.summary-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.daily-goals {
  margin-bottom: 30px;
}

.daily-goals h3 {
  margin-bottom: 15px;
  color: var(--text-primary);
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.goal-icon {
  font-size: 1.5rem;
}

.goal-number {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--text-primary);
}

.goal-label {
  font-size: 0.9rem;
  color: var(--text-secondary);
}

.recommendations h3 {
  margin-bottom: 15px;
  color: var(--text-primary);
}

.recommendation-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.recommendation-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: var(--bg-secondary);
  border-radius: 6px;
}

.rec-icon {
  font-size: 1.2rem;
}

.filter-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: white;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.question-item {
  padding: 20px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-secondary);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.question-type {
  background: var(--primary-color);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.question-difficulty {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 0.8rem;
}

.question-content {
  margin-bottom: 15px;
  line-height: 1.6;
}

.question-actions {
  display: flex;
  justify-content: flex-end;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.pattern-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.pattern-card {
  text-align: center;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: 8px;
}

.pattern-card h3 {
  margin-bottom: 10px;
  color: var(--text-primary);
  font-size: 1rem;
}

.pattern-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 5px;
}

.pattern-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.subject-preference h3 {
  margin-bottom: 15px;
  color: var(--text-primary);
}

.preference-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.preference-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background: var(--bg-secondary);
  border-radius: 6px;
}

.preference-subject {
  font-weight: 500;
  color: var(--text-primary);
}

.preference-time {
  color: var(--text-secondary);
}

.btn-primary,
.btn-secondary {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-hover);
}

.btn-secondary {
  background: var(--secondary-color);
  color: white;
}

.btn-secondary:hover {
  background: var(--secondary-hover);
}

.btn-primary:disabled,
.btn-secondary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .ai-study {
    padding: 15px;
  }

  .plan-summary {
    grid-template-columns: 1fr;
  }

  .goals-grid {
    grid-template-columns: 1fr;
  }

  .pattern-grid {
    grid-template-columns: 1fr;
  }

  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
