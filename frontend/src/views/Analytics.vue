<template>
  <div class="analytics-page">
    <div class="page-header">
      <h1>学习数据分析</h1>
      <p>深入了解你的学习表现和进步趋势</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>{{ achievementStats.total_study_time || 0 }}</h3>
          <p>总学习时间(分钟)</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <h3>{{ achievementStats.total_questions || 0 }}</h3>
          <p>答题总数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-content">
          <h3>{{ achievementStats.avg_accuracy || 0 }}%</h3>
          <p>平均正确率</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🏆</div>
        <div class="stat-content">
          <h3>{{ achievementStats.learning_level || '新手' }}</h3>
          <p>学习等级</p>
        </div>
      </div>
    </div>

    <!-- 图表区域 -->
    <div class="charts-container">
      <!-- 学习趋势图 -->
      <div class="chart-card">
        <h3>学习趋势</h3>
        <div class="chart-controls">
          <button 
            v-for="period in [7, 30, 90]" 
            :key="period"
            :class="['period-btn', { active: selectedPeriod === period }]"
            @click="selectedPeriod = period; loadStudyTrends()"
          >
            {{ period }}天
          </button>
        </div>
        <div class="chart-placeholder">
          <div class="trend-chart">
            <div 
              v-for="(trend, index) in studyTrends" 
              :key="index"
              class="trend-bar"
              :style="{ height: `${(trend.total_time / maxTime) * 100}%` }"
              :title="`${trend.date}: ${trend.total_time}分钟`"
            ></div>
          </div>
          <p class="chart-note">学习时间趋势 (最近{{ selectedPeriod }}天)</p>
        </div>
      </div>

      <!-- 学科表现 -->
      <div class="chart-card">
        <h3>学科表现</h3>
        <div class="subject-performance">
          <div 
            v-for="subject in subjectPerformance" 
            :key="subject.subject"
            class="subject-item"
          >
            <div class="subject-info">
              <span class="subject-name">{{ subject.subject }}</span>
              <span class="subject-accuracy">{{ subject.avg_accuracy }}%</span>
            </div>
            <div class="accuracy-bar">
              <div 
                class="accuracy-fill"
                :style="{ width: `${subject.avg_accuracy}%` }"
              ></div>
            </div>
            <div class="subject-stats">
              <span>{{ subject.question_count }}题</span>
              <span>{{ subject.total_time }}分钟</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习模式 -->
      <div class="chart-card">
        <h3>学习模式分析</h3>
        <div class="learning-patterns">
          <div class="pattern-section">
            <h4>每日学习时间分布</h4>
            <div class="hourly-chart">
              <div 
                v-for="hour in 24" 
                :key="hour"
                class="hour-bar"
                :style="{ height: `${getHourlyHeight(hour)}%` }"
                :title="`${hour}:00 - ${hour}:59`"
              ></div>
            </div>
          </div>
          
          <div class="pattern-section">
            <h4>每周学习分布</h4>
            <div class="weekly-chart">
              <div 
                v-for="day in weeklyDistribution" 
                :key="day.day_of_week"
                class="day-bar"
                :style="{ height: `${(day.total_time / maxWeeklyTime) * 100}%` }"
                :title="`${day.day_name}: ${day.total_time}分钟`"
              >
                <span class="day-label">{{ day.day_name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 难度分析 -->
      <div class="chart-card">
        <h3>难度分布</h3>
        <div class="difficulty-analysis">
          <div 
            v-for="diff in difficultyAnalysis" 
            :key="diff.difficulty"
            class="difficulty-item"
          >
            <div class="difficulty-info">
              <span class="difficulty-level">{{ getDifficultyLabel(diff.difficulty) }}</span>
              <span class="difficulty-accuracy">{{ diff.avg_accuracy }}%</span>
            </div>
            <div class="difficulty-bar">
              <div 
                class="difficulty-fill"
                :style="{ width: `${(diff.question_count / maxQuestionCount) * 100}%` }"
              ></div>
            </div>
            <span class="question-count">{{ diff.question_count }}题</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <p>正在加载数据...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useApi } from '@/composables/useApi'

const api = useApi()

// 响应式数据
const loading = ref(false)
const selectedPeriod = ref(30)
const studyTrends = ref([])
const subjectPerformance = ref([])
const difficultyAnalysis = ref([])
const learningPatterns = ref({})
const achievementStats = ref({})

// 计算属性
const maxTime = computed(() => {
  if (studyTrends.value.length === 0) return 1
  return Math.max(...studyTrends.value.map(t => t.total_time))
})

const maxWeeklyTime = computed(() => {
  if (!learningPatterns.value.weekly_distribution) return 1
  return Math.max(...learningPatterns.value.weekly_distribution.map(d => d.total_time))
})

const maxQuestionCount = computed(() => {
  if (difficultyAnalysis.value.length === 0) return 1
  return Math.max(...difficultyAnalysis.value.map(d => d.question_count))
})

const weeklyDistribution = computed(() => {
  return learningPatterns.value.weekly_distribution || []
})

// 方法
const loadStudyTrends = async () => {
  try {
    loading.value = true
    const response = await api.get(`/analytics/study-trends?days=${selectedPeriod.value}`)
    if (response.success) {
      studyTrends.value = response.data.trends
    }
  } catch (error) {
    console.error('加载学习趋势失败:', error)
  } finally {
    loading.value = false
  }
}

const loadSubjectPerformance = async () => {
  try {
    const response = await api.get('/analytics/subject-performance')
    if (response.success) {
      subjectPerformance.value = response.data
    }
  } catch (error) {
    console.error('加载学科表现失败:', error)
  }
}

const loadDifficultyAnalysis = async () => {
  try {
    const response = await api.get('/analytics/difficulty-analysis')
    if (response.success) {
      difficultyAnalysis.value = response.data
    }
  } catch (error) {
    console.error('加载难度分析失败:', error)
  }
}

const loadLearningPatterns = async () => {
  try {
    const response = await api.get('/analytics/learning-patterns')
    if (response.success) {
      learningPatterns.value = response.data
    }
  } catch (error) {
    console.error('加载学习模式失败:', error)
  }
}

const loadAchievementStats = async () => {
  try {
    const response = await api.get('/analytics/achievement-stats')
    if (response.success) {
      achievementStats.value = response.data
    }
  } catch (error) {
    console.error('加载成就统计失败:', error)
  }
}

const getHourlyHeight = (hour) => {
  if (!learningPatterns.value.hourly_distribution) return 0
  const hourData = learningPatterns.value.hourly_distribution.find(h => h.hour === hour)
  if (!hourData) return 0
  
  const maxHourlyTime = Math.max(...learningPatterns.value.hourly_distribution.map(h => h.total_time))
  return maxHourlyTime > 0 ? (hourData.total_time / maxHourlyTime) * 100 : 0
}

const getDifficultyLabel = (difficulty) => {
  const labels = {
    1: '基础',
    2: '简单', 
    3: '中等',
    4: '困难',
    5: '专家'
  }
  return labels[difficulty] || `难度${difficulty}`
}

const loadAllData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadStudyTrends(),
      loadSubjectPerformance(),
      loadDifficultyAnalysis(),
      loadLearningPatterns(),
      loadAchievementStats()
    ])
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadAllData()
})
</script>

<style scoped>
.analytics-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-header p {
  color: #6c757d;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.stat-content h3 {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0 0 5px 0;
}

.stat-content p {
  color: #6c757d;
  margin: 0;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 20px;
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
  font-size: 1.3rem;
}

.chart-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.period-btn {
  padding: 8px 16px;
  border: 1px solid #dee2e6;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.period-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.chart-placeholder {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.trend-chart {
  display: flex;
  align-items: end;
  gap: 2px;
  height: 200px;
  margin-bottom: 10px;
}

.trend-bar {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px 2px 0 0;
  min-height: 4px;
  transition: all 0.3s;
}

.trend-bar:hover {
  opacity: 0.8;
}

.chart-note {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0;
}

.subject-performance {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.subject-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.subject-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.subject-name {
  font-weight: 500;
  color: #2c3e50;
}

.subject-accuracy {
  font-weight: bold;
  color: #667eea;
}

.accuracy-bar {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.accuracy-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.subject-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: #6c757d;
}

.learning-patterns {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.pattern-section h4 {
  margin: 0 0 15px 0;
  color: #2c3e50;
}

.hourly-chart {
  display: flex;
  align-items: end;
  gap: 1px;
  height: 150px;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
}

.hour-bar {
  flex: 1;
  background: #667eea;
  border-radius: 2px 2px 0 0;
  min-height: 2px;
  transition: all 0.3s;
}

.hour-bar:hover {
  background: #764ba2;
}

.weekly-chart {
  display: flex;
  align-items: end;
  gap: 8px;
  height: 150px;
  background: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
}

.day-bar {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px 4px 0 0;
  min-height: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  padding-bottom: 5px;
  transition: all 0.3s;
}

.day-bar:hover {
  opacity: 0.8;
}

.day-label {
  font-size: 0.7rem;
  color: white;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

.difficulty-analysis {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.difficulty-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.difficulty-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.difficulty-level {
  font-weight: 500;
  color: #2c3e50;
}

.difficulty-accuracy {
  font-weight: bold;
  color: #667eea;
}

.difficulty-bar {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.difficulty-fill {
  height: 100%;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  transition: width 0.3s;
}

.question-count {
  font-size: 0.8rem;
  color: #6c757d;
  text-align: right;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .analytics-page {
    padding: 10px;
  }
  
  .charts-container {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .trend-chart,
  .hourly-chart,
  .weekly-chart {
    height: 120px;
  }
}
</style> 