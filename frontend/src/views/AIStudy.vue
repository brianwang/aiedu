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

          <!-- 学习计划详情 -->
          <div class="plan-details">
            <div class="plan-section">
              <h3>📋 学习计划概览</h3>
              <div class="plan-info">
                <div class="info-item">
                  <span class="label">学习阶段：</span>
                  <span class="value">{{ studyPlan.study_level || '初级' }}</span>
                </div>
                <div class="info-item">
                  <span class="label">重点学科：</span>
                  <span class="value">{{ studyPlan.focus_subjects?.join(', ') || '暂无' }}</span>
                </div>
                <div class="info-item">
                  <span class="label">难度建议：</span>
                  <span class="value">{{ getDifficultyText(studyPlan.difficulty_adjustment) }}</span>
                </div>
              </div>
            </div>

            <div class="plan-section">
              <h3>🎯 今日目标</h3>
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

            <!-- 今日学习计划提醒 -->
            <div class="plan-section" v-if="todayTasks.length > 0">
              <h3>📅 今日学习提醒</h3>
              <div class="today-tasks">
                <div 
                  v-for="task in todayTasks" 
                  :key="task.id"
                  :class="['task-item', `status-${task.status}`]"
                >
                  <div class="task-info">
                    <div class="task-title">{{ task.title }}</div>
                    <div class="task-meta">
                      <span class="task-type">{{ getTaskTypeText(task.task_type) }}</span>
                      <span class="task-duration">{{ task.estimated_time }}分钟</span>
                      <span class="task-subject">{{ task.subject }}</span>
                    </div>
                  </div>
                  <div class="task-actions">
                    <button 
                      v-if="task.status === 'pending'"
                      @click="startTask(task.id)"
                      class="btn btn-sm btn-primary"
                    >
                      开始
                    </button>
                    <button 
                      v-if="task.status === 'in_progress'"
                      @click="completeTask(task.id)"
                      class="btn btn-sm btn-success"
                    >
                      完成
                    </button>
                    <span v-if="task.status === 'completed'" class="status-badge">
                      ✅ 已完成
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 学习建议 -->
            <div class="plan-section" v-if="studyPlan.study_suggestions">
              <h3>💡 学习建议</h3>
              <div class="suggestions-list">
                <div 
                  v-for="(suggestion, index) in studyPlan.study_suggestions" 
                  :key="index"
                  class="suggestion-item"
                >
                  <div class="suggestion-icon">💡</div>
                  <div class="suggestion-text">{{ suggestion }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习能力评估卡片 -->
      <div class="ability-assessment-card">
        <div class="card-header">
          <h2>学习能力评估</h2>
          <!-- 右上角按钮已移除 -->
        </div>

        <div v-if="loading && !abilityAssessment" class="loading">
          <div class="spinner"></div>
          <p>正在评估学习能力...</p>
        </div>

        <div v-else-if="abilityAssessment" class="assessment-content">
          <div class="assessment-summary">
            <div class="summary-item">
              <div class="summary-number">
                {{ abilityAssessment.overall_score || 0 }}
              </div>
              <div class="summary-label">综合能力</div>
            </div>
            <div class="summary-item">
              <div class="summary-number">
                {{ abilityAssessment.learning_level || '初级' }}
              </div>
              <div class="summary-label">学习水平</div>
            </div>
            <div class="summary-item">
              <div class="summary-number">
                {{ abilityAssessment.study_efficiency || 0 }}%
              </div>
              <div class="summary-label">学习效率</div>
            </div>
          </div>

          <div class="assessment-details">
            <div class="detail-section">
              <h3>📊 能力分析</h3>
              <div class="ability-breakdown">
                <div 
                  v-for="ability in abilityAssessment.ability_breakdown" 
                  :key="ability.name"
                  class="ability-item"
                >
                  <div class="ability-header">
                    <span class="ability-name">{{ ability.name }}</span>
                    <span class="ability-score">{{ ability.score }}分</span>
                  </div>
                  <div class="progress-bar">
                    <div class="progress-fill" :style="{ width: ability.score + '%' }"></div>
                  </div>
                  <div class="ability-description">{{ ability.description }}</div>
                </div>
              </div>
            </div>

            <div class="detail-section">
              <h3>🎯 改进建议</h3>
              <ul class="improvement-list">
                <li 
                  v-for="(suggestion, index) in abilityAssessment.improvement_suggestions" 
                  :key="index"
                  class="improvement-item"
                >
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div v-else class="no-assessment">
          <div class="empty-icon">📊</div>
          <h3>尚未进行学习能力评估</h3>
          <p>通过能力评估，我们可以为您制定更精准的学习计划</p>
          <button @click="assessAbility" class="btn btn-primary" :disabled="loading">
            <span v-if="loading">评估中...</span>
            <span v-else>开始能力评估</span>
          </button>
        </div>
      </div>

      <!-- 学习风格与模式分析卡片 -->
      <div class="learning-style-card">
        <div class="card-header">
          <h2>学习风格与模式分析</h2>
          <!-- 右上角按钮已移除 -->
        </div>

        <div v-if="loading && !learningStyle" class="loading">
          <div class="spinner"></div>
          <p>正在分析学习风格...</p>
        </div>

        <div v-else-if="learningStyle" class="style-content">
          <div class="style-summary">
            <div class="style-type">
              <div class="style-icon">{{ getStyleIcon(learningStyle.learning_style) }}</div>
              <div class="style-info">
                <h3>{{ learningStyle.learning_style }}</h3>
                <p>{{ learningStyle.style_description }}</p>
              </div>
            </div>
          </div>

          <div class="style-details">
            <div class="detail-section">
              <h3>🎨 学习偏好</h3>
              <div class="preferences-grid">
                <div 
                  v-for="preference in learningStyle.learning_preferences" 
                  :key="preference.name"
                  class="preference-item"
                >
                  <div class="preference-icon">{{ preference.icon }}</div>
                  <div class="preference-content">
                    <h4>{{ preference.name }}</h4>
                    <p>{{ preference.description }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="detail-section">
              <h3>📈 学习模式</h3>
              <div class="pattern-analysis">
                <div class="pattern-item">
                  <h4>学习时间分布</h4>
                  <div class="time-distribution">
                    <div 
                      v-for="(time, period) in learningStyle.time_distribution" 
                      :key="period"
                      class="time-item"
                    >
                      <span class="time-period">{{ period }}</span>
                      <span class="time-percentage">{{ time }}%</span>
                    </div>
                  </div>
                </div>
                <div class="pattern-item">
                  <h4>题目类型偏好</h4>
                  <div class="question-preferences">
                    <div 
                      v-for="(pref, type) in learningStyle.question_type_preference" 
                      :key="type"
                      class="question-item"
                    >
                      <span class="question-type">{{ getQuestionTypeText(type) }}</span>
                      <span class="question-percentage">{{ String(pref) }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="detail-section">
              <h3>💡 个性化建议</h3>
              <ul class="personalized-suggestions">
                <li 
                  v-for="(suggestion, index) in learningStyle.personalized_recommendations" 
                  :key="index"
                  class="suggestion-item"
                >
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div v-else class="no-style">
          <div class="empty-icon">🎨</div>
          <h3>尚未进行学习风格分析</h3>
          <p>了解您的学习风格，获得更个性化的学习建议</p>
          <button @click="analyzeStyle" class="btn btn-primary" :disabled="loading">
            <span v-if="loading">分析中...</span>
            <span v-else>开始风格分析</span>
          </button>
        </div>
      </div>

      <!-- 智能推荐题目 -->
      <div class="recommended-questions">
        <div class="card-header">
          <h2>智能推荐题目</h2>
          <button
            @click="fetchRecommendedQuestions"
            class="refresh-btn"
            :disabled="loading"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
              />
            </svg>
            刷新推荐
          </button>
        </div>

        <div v-if="loading && recommendedQuestions.length === 0" class="loading">
          <div class="spinner"></div>
          <p>正在为您推荐题目...</p>
        </div>

        <div v-else-if="recommendedQuestions.length > 0" class="questions-content">
          <div class="questions-grid">
            <div 
              v-for="question in recommendedQuestions.slice(0, 3)" 
              :key="String(question.id)"
              class="question-card"
            >
              <div class="question-header">
                <span class="question-type">{{ getQuestionTypeText(question.question_type) }}</span>
                <span class="question-difficulty">难度: {{ question.difficulty }}</span>
              </div>
              <div class="question-content">
                <p>{{ question.content }}</p>
              </div>
              <div class="question-footer">
                <span class="question-subject">{{ question.category || '综合' }}</span>
                <button @click="startPractice(question)" class="btn btn-sm btn-primary">
                  开始练习
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="no-questions">
          <div class="empty-icon">📝</div>
          <p>暂无推荐题目</p>
          <button @click="fetchRecommendedQuestions" class="btn btn-primary">
            <svg viewBox="0 0 24 24" fill="currentColor" class="btn-icon">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              <path d="M12 6l1.09 2.26L15.5 9l-2.41 2.35.57 3.32L12 13.77l-1.66.9.57-3.32L8.5 9l2.41-.74L12 6z"/>
            </svg>
            获取推荐
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  getStudyPlan, 
  assessLearningAbility, 
  analyzeLearningStyle, 
  getRecommendedQuestions,
  getLearningTasks,
  updateTaskStatus
} from '@/api/ai'

const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const loading = ref(false)
const studyPlan = ref<any>(null)
const abilityAssessment = ref<any>(null)
const learningStyle = ref<any>(null)
const recommendedQuestions = ref<any[]>([])
const todayTasks = ref<any[]>([])

// 计算属性
const subjects = computed(() => [
  '数学', '语文', '英语', '物理', '化学', '生物', '历史', '地理', '政治'
])

// 工具方法
const getDifficultyText = (difficulty: string) => {
  const difficultyMap: { [key: string]: string } = {
    increase: '适当提高',
    decrease: '适当降低',
    maintain: '保持当前'
  }
  return difficultyMap[difficulty] || '保持当前'
}

const getQuestionTypeText = (type: string) => {
  const typeMap: { [key: string]: string } = {
    single_choice: '单选题',
    multiple_choice: '多选题',
    fill_blank: '填空题',
    short_answer: '简答题',
    essay: '论述题'
  }
  return typeMap[type] || '未知类型'
}

const getTaskTypeText = (type: string) => {
  const typeMap: { [key: string]: string } = {
    practice: '练习',
    review: '复习',
    new_concept: '新概念'
  }
  return typeMap[type] || '未知类型'
}

const getStyleIcon = (style: string) => {
  const iconMap: { [key: string]: string } = {
    '视觉型': '👁️',
    '听觉型': '👂',
    '动觉型': '🏃',
    '阅读型': '📖',
    '混合型': '🔄'
  }
  return iconMap[style] || '🎨'
}

// API方法
const refreshStudyPlan = async () => {
  try {
    loading.value = true
    const response = await getStudyPlan()
    if (response.success) {
      studyPlan.value = response.data
      await loadTodayTasks()
    }
  } catch (error) {
    console.error('获取学习计划失败:', error)
  } finally {
    loading.value = false
  }
}

const assessAbility = async () => {
  try {
    loading.value = true
    // 模拟用户数据
    const assessmentData = {
      study_time: 120,
      questions_completed: 50,
      accuracy: 75,
      subjects: ['数学', '英语'],
      wrong_questions_distribution: {
        '数学': 8,
        '英语': 4
      }
    }
    const response = await assessLearningAbility(assessmentData)
    if (response.success) {
      abilityAssessment.value = response.data
    }
  } catch (error) {
    console.error('能力评估失败:', error)
  } finally {
    loading.value = false
  }
}

const analyzeStyle = async () => {
  try {
    loading.value = true
    // 模拟用户数据
    const styleData = {
      time_distribution: {
        '上午': 30,
        '下午': 40,
        '晚上': 30
      },
      question_type_preference: {
        'single_choice': 40,
        'multiple_choice': 30,
        'fill_blank': 20,
        'short_answer': 10
      },
      learning_mode: 'visual',
      review_frequency: 3,
      wrong_question_handling: 'immediate'
    }
    const response = await analyzeLearningStyle(styleData)
    if (response.success) {
      learningStyle.value = response.data
    }
  } catch (error) {
    console.error('学习风格分析失败:', error)
  } finally {
    loading.value = false
  }
}

const fetchRecommendedQuestions = async () => {
  try {
    loading.value = true
    const response = await getRecommendedQuestions()
    if (response.success) {
      recommendedQuestions.value = response.data.slice(0, 3) // 只取前3题
    }
  } catch (error) {
    console.error('获取推荐题目失败:', error)
  } finally {
    loading.value = false
  }
}

const loadTodayTasks = async () => {
  try {
    const response = await getLearningTasks()
    if (response.success) {
      todayTasks.value = response.data.filter((task: any) => {
        const today = new Date().toISOString().split('T')[0]
        return task.scheduled_date === today
      })
    }
  } catch (error) {
    console.error('加载今日任务失败:', error)
  }
}

const startTask = async (taskId: string) => {
  try {
    await updateTaskStatus(taskId, 'in_progress')
    await loadTodayTasks()
  } catch (error) {
    console.error('开始任务失败:', error)
  }
}

const completeTask = async (taskId: string) => {
  try {
    await updateTaskStatus(taskId, 'completed')
    await loadTodayTasks()
  } catch (error) {
    console.error('完成任务失败:', error)
  }
}

const startPractice = (question: any) => {
  // 跳转到练习页面
  router.push(`/question-bank?questionId=${String(question.id)}&mode=practice`)
}

// 生命周期
onMounted(async () => {
  await refreshStudyPlan()
  await fetchRecommendedQuestions()
})
</script>

<style scoped>
.ai-study {
  min-height: 100vh;
  background: #f5f6fa;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.title-icon {
  width: 40px;
  height: 40px;
  color: #ffd700;
}

.page-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
  color: #666;
}

.ai-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr;
  gap: 25px;
}

/* 卡片通用样式 */
.study-plan-card,
.ability-assessment-card,
.learning-style-card,
.recommended-questions {
  background: white;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.07);
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.study-plan-card:hover,
.ability-assessment-card:hover,
.learning-style-card:hover,
.recommended-questions:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.card-header {
  background: #fff;
  color: #333;
  padding: 20px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.refresh-btn,
.btn-secondary {
  background: #f5f6fa;
  border: 1px solid #e0e0e0;
  color: #333;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.refresh-btn:hover,
.btn-secondary:hover {
  background: #e9ecef;
  color: #222;
}

.refresh-btn svg {
  width: 16px;
  height: 16px;
}

/* 加载状态 */
.loading {
  padding: 40px;
  text-align: center;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 学习计划内容 */
.plan-content {
  padding: 25px;
}

.plan-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.summary-item {
  text-align: center;
  padding: 20px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border-radius: 15px;
  color: white;
}

.summary-number {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 5px;
}

.summary-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.plan-details {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.plan-section {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 20px;
}

.plan-section h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.2rem;
}

.plan-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #666;
}

.value {
  color: #333;
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.goal-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.goal-icon {
  font-size: 2rem;
}

.goal-content {
  flex: 1;
}

.goal-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
}

.goal-label {
  font-size: 0.9rem;
  color: #666;
}

/* 今日任务 */
.today-tasks {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #ddd;
  transition: all 0.3s ease;
}

.task-item.status-pending {
  border-left-color: #ffc107;
}

.task-item.status-in_progress {
  border-left-color: #17a2b8;
}

.task-item.status-completed {
  border-left-color: #28a745;
  opacity: 0.7;
}

.task-info {
  flex: 1;
}

.task-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.task-meta {
  display: flex;
  gap: 15px;
  font-size: 0.9rem;
  color: #666;
}

.task-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.status-badge {
  background: #28a745;
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.8rem;
}

/* 建议列表 */
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.suggestion-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.suggestion-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.suggestion-text {
  color: #333;
  line-height: 1.5;
}

/* 能力评估 */
.assessment-content {
  padding: 25px;
}

.assessment-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.assessment-details {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.detail-section {
  background: #f8f9fa;
  border-radius: 15px;
  padding: 20px;
}

.detail-section h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 1.2rem;
}

.ability-breakdown {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ability-item {
  background: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.ability-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.ability-name {
  font-weight: 600;
  color: #333;
}

.ability-score {
  font-weight: 700;
  color: #667eea;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.ability-description {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.improvement-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.improvement-item {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  color: #333;
  line-height: 1.5;
}

.improvement-item:last-child {
  border-bottom: none;
}

.improvement-item::before {
  content: "💡";
  margin-right: 10px;
}

/* 空状态 */
.no-assessment,
.no-style,
.no-questions {
  padding: 40px;
  text-align: center;
  color: #666;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.no-assessment h3,
.no-style h3 {
  margin: 0 0 10px 0;
  color: #333;
}

.no-assessment p,
.no-style p {
  margin: 0 0 20px 0;
  line-height: 1.5;
}

/* 学习风格 */
.style-content {
  padding: 25px;
}

.style-summary {
  margin-bottom: 30px;
}

.style-type {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  color: white;
}

.style-icon {
  font-size: 3rem;
}

.style-info h3 {
  margin: 0 0 10px 0;
  font-size: 1.5rem;
}

.style-info p {
  margin: 0;
  opacity: 0.9;
  line-height: 1.5;
}

.style-details {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.preferences-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
}

.preference-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.preference-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.preference-content h4 {
  margin: 0 0 8px 0;
  color: #333;
}

.preference-content p {
  margin: 0;
  color: #666;
  line-height: 1.4;
}

.pattern-analysis {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.pattern-item {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.pattern-item h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.time-distribution,
.question-preferences {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.time-item,
.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.time-item:last-child,
.question-item:last-child {
  border-bottom: none;
}

.time-period,
.question-type {
  color: #333;
  font-weight: 500;
}

.time-percentage,
.question-percentage {
  color: #667eea;
  font-weight: 600;
}

.personalized-suggestions {
  list-style: none;
  padding: 0;
  margin: 0;
}

.personalized-suggestions .suggestion-item {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  color: #333;
  line-height: 1.5;
}

.personalized-suggestions .suggestion-item:last-child {
  border-bottom: none;
}

.personalized-suggestions .suggestion-item::before {
  content: "💡";
  margin-right: 10px;
}

/* 推荐题目 */
.questions-content {
  padding: 25px;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 20px;
}

.question-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.question-card:hover {
  transform: translateY(-5px);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-type {
  background: #667eea;
  color: white;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.question-difficulty {
  color: #666;
  font-size: 0.9rem;
}

.question-content {
  margin-bottom: 15px;
}

.question-content p {
  margin: 0;
  color: #333;
  line-height: 1.6;
}

.question-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-subject {
  color: #666;
  font-size: 0.9rem;
}

/* 按钮样式 */
.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
}

.btn-outline {
  background: transparent;
  border: 2px solid #667eea;
  color: #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .ai-study {
    padding: 15px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .ai-content {
    gap: 20px;
  }
  
  .plan-summary,
  .assessment-summary {
    grid-template-columns: 1fr;
  }
  
  .goals-grid {
    grid-template-columns: 1fr;
  }
  
  .questions-grid {
    grid-template-columns: 1fr;
  }
  
  .preferences-grid {
    grid-template-columns: 1fr;
  }
  
  .pattern-analysis {
    grid-template-columns: 1fr;
  }
  
  .task-meta {
    flex-direction: column;
    gap: 5px;
  }
  
  .task-actions {
    flex-direction: column;
    gap: 5px;
  }
}
</style>
