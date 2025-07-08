<template>
  <div class="learning-plan">
    <div class="plan-container">
      <!-- 页面头部 -->
      <div class="plan-header">
        <h1>我的学习计划</h1>
        <div class="header-actions">
          <button @click="refreshPlans" class="btn btn-outline" :disabled="loading">
            {{ loading ? '加载中...' : '刷新' }}
          </button>
          <button @click="showProfileWizard" class="btn btn-primary">
            重新生成计划
          </button>
        </div>
      </div>

      <!-- 学习统计概览 -->
      <div class="statistics-overview" v-if="statistics">
        <div class="stat-card">
          <div class="stat-icon">📚</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.total_study_time }}分钟</div>
            <div class="stat-label">总学习时间</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">✅</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.completion_rate * 100 }}%</div>
            <div class="stat-label">完成率</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🔥</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.current_streak }}天</div>
            <div class="stat-label">连续学习</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏆</div>
          <div class="stat-content">
            <div class="stat-value">{{ statistics.total_achievements }}</div>
            <div class="stat-label">获得成就</div>
          </div>
        </div>
      </div>

      <!-- 学习日历 -->
      <div class="calendar-section">
        <LearningCalendar />
      </div>

      <!-- 成就系统 -->
      <div class="achievement-section">
        <AchievementSystem />
      </div>

      <!-- 计划类型切换 -->
      <div class="plan-tabs">
        <button 
          v-for="planType in planTypes" 
          :key="planType.value"
          @click="activePlanType = planType.value"
          :class="['tab-btn', { active: activePlanType === planType.value }]"
        >
          {{ planType.label }}
        </button>
      </div>

      <!-- 计划内容 -->
      <div class="plan-content">
        <!-- 短期计划 -->
        <div v-if="activePlanType === 'short_term' && shortTermPlan" class="plan-section">
          <div class="plan-info">
            <h2>{{ shortTermPlan.title }}</h2>
            <p class="plan-description">{{ shortTermPlan.description }}</p>
            <div class="plan-meta">
              <span class="meta-item">
                <i class="icon">📅</i>
                {{ formatDate(shortTermPlan.start_date) }} - {{ formatDate(shortTermPlan.end_date) }}
              </span>
              <span class="meta-item">
                <i class="icon">🎯</i>
                完成率: {{ getPlanCompletionRate(shortTermPlan.id) }}%
              </span>
            </div>
          </div>

          <!-- 任务列表 -->
          <div class="tasks-section">
            <h3>学习任务</h3>
            <div class="tasks-list">
              <div 
                v-for="task in getPlanTasks(shortTermPlan.id)" 
                :key="task.id"
                :class="['task-item', `status-${task.status}`]"
              >
                <div class="task-header">
                  <div class="task-title">
                    <span class="task-type-icon">{{ getTaskTypeIcon(task.task_type) }}</span>
                    {{ task.title }}
                  </div>
                  <div class="task-actions">
                    <span class="task-duration">{{ task.estimated_time }}分钟</span>
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
                    <span v-if="task.status === 'completed'" class="status-badge completed">
                      ✅ 已完成
                    </span>
                  </div>
                </div>
                <div class="task-description">{{ task.description }}</div>
                <div class="task-meta">
                  <span class="difficulty">难度: {{ '⭐'.repeat(task.difficulty) }}</span>
                  <span v-if="task.due_date" class="due-date">
                    截止: {{ formatDate(task.due_date) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 中期计划 -->
        <div v-if="activePlanType === 'medium_term' && mediumTermPlan" class="plan-section">
          <div class="plan-info">
            <h2>{{ mediumTermPlan.title }}</h2>
            <p class="plan-description">{{ mediumTermPlan.description }}</p>
            <div class="plan-meta">
              <span class="meta-item">
                <i class="icon">📅</i>
                {{ formatDate(mediumTermPlan.start_date) }} - {{ formatDate(mediumTermPlan.end_date) }}
              </span>
              <span class="meta-item">
                <i class="icon">🎯</i>
                完成率: {{ getPlanCompletionRate(mediumTermPlan.id) }}%
              </span>
            </div>
          </div>

          <!-- 里程碑展示 -->
          <div class="milestones-section">
            <h3>学习里程碑</h3>
            <div class="milestones-list">
              <div class="milestone-item">
                <div class="milestone-icon">🎯</div>
                <div class="milestone-content">
                  <h4>掌握核心概念</h4>
                  <p>完成基础理论学习，建立知识框架</p>
                  <div class="milestone-progress">
                    <div class="progress-bar">
                      <div class="progress-fill" :style="{ width: '60%' }"></div>
                    </div>
                    <span>60%</span>
                  </div>
                </div>
              </div>
              <div class="milestone-item">
                <div class="milestone-icon">💻</div>
                <div class="milestone-content">
                  <h4>实践项目开发</h4>
                  <p>完成2-3个实际项目，巩固技能应用</p>
                  <div class="milestone-progress">
                    <div class="progress-bar">
                      <div class="progress-fill" :style="{ width: '30%' }"></div>
                    </div>
                    <span>30%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 长期计划 -->
        <div v-if="activePlanType === 'long_term' && longTermPlan" class="plan-section">
          <div class="plan-info">
            <h2>{{ longTermPlan.title }}</h2>
            <p class="plan-description">{{ longTermPlan.description }}</p>
            <div class="plan-meta">
              <span class="meta-item">
                <i class="icon">📅</i>
                {{ formatDate(longTermPlan.start_date) }} - {{ formatDate(longTermPlan.end_date) }}
              </span>
              <span class="meta-item">
                <i class="icon">🎯</i>
                完成率: {{ getPlanCompletionRate(longTermPlan.id) }}%
              </span>
            </div>
          </div>

          <!-- 职业发展路径 -->
          <div class="career-path-section">
            <h3>职业发展路径</h3>
            <div class="career-timeline">
              <div class="timeline-item">
                <div class="timeline-point current"></div>
                <div class="timeline-content">
                  <h4>当前阶段</h4>
                  <p>学习基础技能，建立知识体系</p>
                </div>
              </div>
              <div class="timeline-item">
                <div class="timeline-point"></div>
                <div class="timeline-content">
                  <h4>技能提升</h4>
                  <p>深入专业领域，提升实战能力</p>
                </div>
              </div>
              <div class="timeline-item">
                <div class="timeline-point"></div>
                <div class="timeline-content">
                  <h4>专业发展</h4>
                  <p>成为领域专家，具备独立解决问题的能力</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>加载中...</p>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && !hasPlans" class="empty-state">
          <div class="empty-icon">📚</div>
          <h3>还没有学习计划</h3>
          <p>开始创建你的个性化学习计划吧！</p>
          <button @click="showProfileWizard" class="btn btn-primary">
            创建学习计划
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useApi } from '@/composables/useApi'
import LearningCalendar from '@/components/LearningCalendar.vue'
import AchievementSystem from '@/components/AchievementSystem.vue'

const router = useRouter()
const authStore = useAuthStore()
const api = useApi()

// 响应式数据
const loading = ref(false)
const plans = ref([])
const tasks = ref([])
const statistics = ref(null)
const activePlanType = ref('short_term')

// 计划类型配置
const planTypes = [
  { label: '短期计划', value: 'short_term' },
  { label: '中期计划', value: 'medium_term' },
  { label: '长期计划', value: 'long_term' }
]

// 计算属性
const shortTermPlan = computed(() => 
  plans.value.find(plan => plan.plan_type === 'short_term')
)

const mediumTermPlan = computed(() => 
  plans.value.find(plan => plan.plan_type === 'medium_term')
)

const longTermPlan = computed(() => 
  plans.value.find(plan => plan.plan_type === 'long_term')
)

const hasPlans = computed(() => plans.value.length > 0)

// 方法
const loadPlans = async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  loading.value = true
  try {
    // 加载学习计划
    const plansResponse = await api.get('/learning/plans')
    plans.value = plansResponse

    // 加载学习统计
    const statsResponse = await api.get('/learning/statistics')
    statistics.value = statsResponse

    // 加载任务（如果有计划）
    if (plans.value.length > 0) {
      for (const plan of plans.value) {
        const tasksResponse = await api.get(`/learning/plans/${plan.id}/tasks`)
        tasks.value.push(...tasksResponse)
      }
    }
  } catch (error) {
    console.error('加载学习计划失败:', error)
  } finally {
    loading.value = false
  }
}

const refreshPlans = () => {
  loadPlans()
}

const showProfileWizard = () => {
  router.push('/profile-wizard')
}

const getPlanTasks = (planId) => {
  return tasks.value.filter(task => task.plan_id === planId)
}

const getPlanCompletionRate = (planId) => {
  const planTasks = getPlanTasks(planId)
  if (planTasks.length === 0) return 0
  
  const completedTasks = planTasks.filter(task => task.status === 'completed')
  return Math.round((completedTasks.length / planTasks.length) * 100)
}

const startTask = async (taskId) => {
  try {
    await api.put(`/learning/tasks/${taskId}/status`, { status: 'in_progress' })
    await loadPlans() // 重新加载数据
  } catch (error) {
    console.error('开始任务失败:', error)
  }
}

const completeTask = async (taskId) => {
  try {
    await api.put(`/learning/tasks/${taskId}/status`, { status: 'completed' })
    await loadPlans() // 重新加载数据
  } catch (error) {
    console.error('完成任务失败:', error)
  }
}

const getTaskTypeIcon = (taskType) => {
  const iconMap = {
    'study': '📖',
    'practice': '💻',
    'review': '🔄',
    'assessment': '📝'
  }
  return iconMap[taskType] || '📋'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadPlans()
})
</script>

<style scoped>
.learning-plan {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 20px;
}

.plan-container {
  max-width: 1200px;
  margin: 0 auto;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.plan-header h1 {
  color: #2c3e50;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.statistics-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.calendar-section {
  margin-bottom: 30px;
}

.achievement-section {
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
  margin-right: 15px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
}

.plan-tabs {
  display: flex;
  background: white;
  border-radius: 12px;
  padding: 5px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.tab-btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.tab-btn.active {
  background: #007bff;
  color: white;
}

.plan-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.plan-section {
  display: none;
}

.plan-section:first-child {
  display: block;
}

.plan-info h2 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.plan-description {
  color: #6c757d;
  margin-bottom: 20px;
}

.plan-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.meta-item {
  display: flex;
  align-items: center;
  color: #6c757d;
}

.icon {
  margin-right: 5px;
}

.tasks-section h3,
.milestones-section h3,
.career-path-section h3 {
  color: #2c3e50;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e9ecef;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.task-item {
  padding: 20px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  transition: all 0.3s;
}

.task-item:hover {
  border-color: #007bff;
  box-shadow: 0 2px 8px rgba(0, 123, 255, 0.1);
}

.task-item.status-completed {
  border-color: #28a745;
  background: #f8fff9;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.task-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  color: #2c3e50;
}

.task-type-icon {
  margin-right: 8px;
  font-size: 1.2rem;
}

.task-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.task-duration {
  color: #6c757d;
  font-size: 0.9rem;
}

.task-description {
  color: #6c757d;
  margin-bottom: 10px;
}

.task-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
}

.difficulty {
  color: #ffc107;
}

.due-date {
  color: #dc3545;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.completed {
  background: #d4edda;
  color: #155724;
}

.milestones-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.milestone-item {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.milestone-icon {
  font-size: 2rem;
  margin-right: 15px;
}

.milestone-content h4 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.milestone-content p {
  color: #6c757d;
  margin-bottom: 15px;
}

.milestone-progress {
  display: flex;
  align-items: center;
  gap: 10px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #007bff;
  transition: width 0.3s;
}

.career-timeline {
  position: relative;
  padding-left: 30px;
}

.timeline-item {
  position: relative;
  margin-bottom: 30px;
}

.timeline-point {
  position: absolute;
  left: -35px;
  top: 5px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #e9ecef;
  border: 3px solid white;
}

.timeline-point.current {
  background: #007bff;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: -29px;
  top: 17px;
  width: 2px;
  height: 30px;
  background: #e9ecef;
}

.timeline-content h4 {
  color: #2c3e50;
  margin-bottom: 5px;
}

.timeline-content p {
  color: #6c757d;
}

.loading-state,
.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e9ecef;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.empty-state p {
  color: #6c757d;
  margin-bottom: 20px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #1e7e34;
}

.btn-outline {
  background: transparent;
  color: #007bff;
  border: 2px solid #007bff;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .plan-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .statistics-overview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .plan-tabs {
    flex-direction: column;
  }
  
  .task-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style> 