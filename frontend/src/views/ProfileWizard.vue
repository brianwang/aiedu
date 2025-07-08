<template>
  <div class="profile-wizard">
    <div class="wizard-container">
      <!-- 进度指示器 -->
      <div class="progress-bar">
        <div class="progress-step" 
             v-for="(step, index) in steps" 
             :key="index"
             :class="{ active: currentStep === index, completed: currentStep > index }">
          <div class="step-number">{{ index + 1 }}</div>
          <div class="step-title">{{ step.title }}</div>
        </div>
      </div>

      <!-- 步骤内容 -->
      <div class="step-content">
        <!-- 步骤1: 基础信息 -->
        <div v-if="currentStep === 0" class="step-panel">
          <h2>让我们了解一下你的基本信息</h2>
          <div class="form-group">
            <label>你的年龄</label>
            <input 
              v-model="profile.age" 
              type="number" 
              min="1" 
              max="120" 
              placeholder="请输入你的年龄"
              class="form-input"
            >
          </div>
          <div class="form-group">
            <label>每日可投入的学习时间（分钟）</label>
            <select v-model="profile.daily_study_time" class="form-select">
              <option value="">请选择</option>
              <option value="15">15分钟</option>
              <option value="30">30分钟</option>
              <option value="45">45分钟</option>
              <option value="60">1小时</option>
              <option value="90">1.5小时</option>
              <option value="120">2小时</option>
              <option value="180">3小时以上</option>
            </select>
          </div>
          <div class="form-group">
            <label>每周学习天数</label>
            <select v-model="profile.weekly_study_days" class="form-select">
              <option value="">请选择</option>
              <option value="1">1天</option>
              <option value="2">2天</option>
              <option value="3">3天</option>
              <option value="4">4天</option>
              <option value="5">5天</option>
              <option value="6">6天</option>
              <option value="7">7天</option>
            </select>
          </div>
        </div>

        <!-- 步骤2: 学习目标 -->
        <div v-if="currentStep === 1" class="step-panel">
          <h2>你想要学习什么？</h2>
          <div class="form-group">
            <label>学习科目</label>
            <input 
              v-model="currentGoal.subject" 
              type="text" 
              placeholder="例如：Python编程、数学、英语等"
              class="form-input"
            >
          </div>
          <div class="form-group">
            <label>技能领域</label>
            <input 
              v-model="currentGoal.skill_area" 
              type="text" 
              placeholder="例如：Web开发、数据分析、口语等"
              class="form-input"
            >
          </div>
          <div class="form-group">
            <label>目标水平</label>
            <select v-model="currentGoal.target_level" class="form-select">
              <option value="">请选择</option>
              <option value="beginner">初学者</option>
              <option value="intermediate">中级</option>
              <option value="advanced">高级</option>
              <option value="expert">专家级</option>
            </select>
          </div>
          <div class="form-group">
            <label>希望达到目标的时间（月）</label>
            <input 
              v-model="currentGoal.target_timeframe" 
              type="number" 
              min="1" 
              max="60" 
              placeholder="例如：6个月"
              class="form-input"
            >
          </div>
          <div class="form-group">
            <label>优先级</label>
            <select v-model="currentGoal.priority" class="form-select">
              <option value="1">低优先级</option>
              <option value="2">较低优先级</option>
              <option value="3">中等优先级</option>
              <option value="4">较高优先级</option>
              <option value="5">高优先级</option>
            </select>
          </div>
          <button @click="addGoal" class="btn btn-secondary">添加学习目标</button>
          
          <!-- 已添加的目标列表 -->
          <div v-if="goals.length > 0" class="goals-list">
            <h3>已添加的学习目标</h3>
            <div v-for="(goal, index) in goals" :key="index" class="goal-item">
              <div class="goal-info">
                <strong>{{ goal.subject }}</strong> - {{ goal.skill_area }}
                <br>
                <small>目标：{{ getLevelText(goal.target_level) }} | 时间：{{ goal.target_timeframe }}个月 | 优先级：{{ goal.priority }}</small>
              </div>
              <button @click="removeGoal(index)" class="btn-remove">删除</button>
            </div>
          </div>
        </div>

        <!-- 步骤3: 学习偏好 -->
        <div v-if="currentStep === 2" class="step-panel">
          <h2>你的学习偏好是什么？</h2>
          <div class="form-group">
            <label>学习风格</label>
            <div class="radio-group">
              <label class="radio-item">
                <input type="radio" v-model="profile.learning_style" value="visual">
                <span class="radio-text">
                  <strong>视觉型</strong>
                  <small>喜欢通过图表、视频、图片学习</small>
                </span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="profile.learning_style" value="auditory">
                <span class="radio-text">
                  <strong>听觉型</strong>
                  <small>喜欢通过听讲、讨论、音频学习</small>
                </span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="profile.learning_style" value="kinesthetic">
                <span class="radio-text">
                  <strong>动手型</strong>
                  <small>喜欢通过实践、操作、体验学习</small>
                </span>
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>难度偏好</label>
            <div class="radio-group">
              <label class="radio-item">
                <input type="radio" v-model="profile.difficulty_preference" value="comfortable">
                <span class="radio-text">
                  <strong>舒适区</strong>
                  <small>喜欢循序渐进，稳步提升</small>
                </span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="profile.difficulty_preference" value="progressive">
                <span class="radio-text">
                  <strong>渐进式</strong>
                  <small>喜欢适度挑战，逐步提高</small>
                </span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="profile.difficulty_preference" value="challenging">
                <span class="radio-text">
                  <strong>挑战性</strong>
                  <small>喜欢高难度挑战，快速突破</small>
                </span>
              </label>
            </div>
          </div>
          <div class="form-group">
            <label>学习环境偏好</label>
            <div class="radio-group">
              <label class="radio-item">
                <input type="radio" v-model="profile.learning_environment" value="online">
                <span class="radio-text">
                  <strong>在线学习</strong>
                  <small>喜欢通过网络课程、视频学习</small>
                </span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="profile.learning_environment" value="offline">
                <span class="radio-text">
                  <strong>线下学习</strong>
                  <small>喜欢实体书籍、面对面教学</small>
                </span>
              </label>
              <label class="radio-item">
                <input type="radio" v-model="profile.learning_environment" value="hybrid">
                <span class="radio-text">
                  <strong>混合学习</strong>
                  <small>喜欢线上线下结合的学习方式</small>
                </span>
              </label>
            </div>
          </div>
        </div>

        <!-- 步骤4: 确认信息 -->
        <div v-if="currentStep === 3" class="step-panel">
          <h2>确认你的学习画像</h2>
          <div class="profile-summary">
            <div class="summary-section">
              <h3>基本信息</h3>
              <p><strong>年龄：</strong>{{ profile.age }}岁</p>
              <p><strong>每日学习时间：</strong>{{ profile.daily_study_time }}分钟</p>
              <p><strong>每周学习天数：</strong>{{ profile.weekly_study_days }}天</p>
            </div>
            <div class="summary-section">
              <h3>学习偏好</h3>
              <p><strong>学习风格：</strong>{{ getStyleText(profile.learning_style) }}</p>
              <p><strong>难度偏好：</strong>{{ getDifficultyText(profile.difficulty_preference) }}</p>
              <p><strong>学习环境：</strong>{{ getEnvironmentText(profile.learning_environment) }}</p>
            </div>
            <div class="summary-section">
              <h3>学习目标 ({{ goals.length }}个)</h3>
              <div v-for="(goal, index) in goals" :key="index" class="goal-summary">
                <strong>{{ goal.subject }}</strong> - {{ goal.skill_area }}
                <br>
                <small>目标：{{ getLevelText(goal.target_level) }} | 时间：{{ goal.target_timeframe }}个月</small>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 导航按钮 -->
      <div class="step-navigation">
        <button 
          v-if="currentStep > 0" 
          @click="prevStep" 
          class="btn btn-outline"
        >
          上一步
        </button>
        <button 
          v-if="currentStep < steps.length - 1" 
          @click="nextStep" 
          class="btn btn-primary"
          :disabled="!canProceed"
        >
          下一步
        </button>
        <button 
          v-if="currentStep === steps.length - 1" 
          @click="submitProfile" 
          class="btn btn-success"
          :disabled="loading"
        >
          {{ loading ? '生成中...' : '生成学习计划' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useApi } from '@/composables/useApi'

const router = useRouter()
const authStore = useAuthStore()
const api = useApi()

// 步骤配置
const steps = [
  { title: '基本信息' },
  { title: '学习目标' },
  { title: '学习偏好' },
  { title: '确认信息' }
]

const currentStep = ref(0)
const loading = ref(false)

// 用户画像数据
const profile = reactive({
  age: '',
  daily_study_time: '',
  weekly_study_days: '',
  learning_style: '',
  difficulty_preference: '',
  learning_environment: ''
})

// 学习目标数据
const goals = ref([])
const currentGoal = reactive({
  subject: '',
  skill_area: '',
  target_level: '',
  target_timeframe: '',
  priority: 3
})

// 计算是否可以进入下一步
const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return profile.age && profile.daily_study_time && profile.weekly_study_days
    case 1:
      return goals.value.length > 0
    case 2:
      return profile.learning_style && profile.difficulty_preference && profile.learning_environment
    default:
      return true
  }
})

// 导航方法
const nextStep = () => {
  if (canProceed.value && currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 学习目标管理
const addGoal = () => {
  if (currentGoal.subject && currentGoal.target_level && currentGoal.target_timeframe) {
    goals.value.push({
      ...currentGoal,
      id: Date.now() // 临时ID
    })
    
    // 重置当前目标
    Object.assign(currentGoal, {
      subject: '',
      skill_area: '',
      target_level: '',
      target_timeframe: '',
      priority: 3
    })
  }
}

const removeGoal = (index) => {
  goals.value.splice(index, 1)
}

// 文本转换方法
const getLevelText = (level) => {
  const levelMap = {
    'beginner': '初学者',
    'intermediate': '中级',
    'advanced': '高级',
    'expert': '专家级'
  }
  return levelMap[level] || level
}

const getStyleText = (style) => {
  const styleMap = {
    'visual': '视觉型',
    'auditory': '听觉型',
    'kinesthetic': '动手型'
  }
  return styleMap[style] || style
}

const getDifficultyText = (difficulty) => {
  const difficultyMap = {
    'comfortable': '舒适区',
    'progressive': '渐进式',
    'challenging': '挑战性'
  }
  return difficultyMap[difficulty] || difficulty
}

const getEnvironmentText = (environment) => {
  const environmentMap = {
    'online': '在线学习',
    'offline': '线下学习',
    'hybrid': '混合学习'
  }
  return environmentMap[environment] || environment
}

// 提交用户画像和学习目标
const submitProfile = async () => {
  if (!authStore.isAuthenticated) {
    alert('请先登录')
    return
  }

  loading.value = true
  
  try {
    // 1. 创建用户画像
    const profileResponse = await api.post('/learning/profile', {
      age: parseInt(profile.age),
      daily_study_time: parseInt(profile.daily_study_time),
      weekly_study_days: parseInt(profile.weekly_study_days),
      learning_style: profile.learning_style,
      difficulty_preference: profile.difficulty_preference,
      learning_environment: profile.learning_environment
    })

    // 2. 创建学习目标
    for (const goal of goals.value) {
      await api.post('/learning/goals', {
        subject: goal.subject,
        skill_area: goal.skill_area,
        target_level: goal.target_level,
        target_timeframe: parseInt(goal.target_timeframe),
        priority: parseInt(goal.priority)
      })
    }

    // 3. 生成AI学习计划
    const planResponse = await api.post('/learning/generate-plan', {
      user_id: authStore.user.id
    })

    // 4. 跳转到学习计划页面
    router.push({
      name: 'LearningPlan',
      params: { planId: planResponse.short_term_plan.id }
    })

  } catch (error) {
    console.error('提交失败:', error)
    alert('提交失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-wizard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.wizard-container {
  max-width: 800px;
  margin: 0 auto;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.progress-bar {
  display: flex;
  background: #f8f9fa;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
}

.progress-step {
  flex: 1;
  text-align: center;
  position: relative;
}

.progress-step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 20px;
  right: -50%;
  width: 100%;
  height: 2px;
  background: #e9ecef;
  z-index: 1;
}

.progress-step.completed:not(:last-child)::after {
  background: #28a745;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e9ecef;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 10px;
  font-weight: bold;
  position: relative;
  z-index: 2;
}

.progress-step.active .step-number {
  background: #007bff;
  color: white;
}

.progress-step.completed .step-number {
  background: #28a745;
  color: white;
}

.step-title {
  font-size: 14px;
  color: #6c757d;
  font-weight: 500;
}

.progress-step.active .step-title {
  color: #007bff;
}

.progress-step.completed .step-title {
  color: #28a745;
}

.step-content {
  padding: 40px;
  min-height: 400px;
}

.step-panel h2 {
  color: #2c3e50;
  margin-bottom: 30px;
  text-align: center;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.form-input,
.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: #007bff;
}

.radio-group {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.radio-item {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.radio-item:hover {
  border-color: #007bff;
  background: #f8f9ff;
}

.radio-item input[type="radio"] {
  margin-right: 12px;
  margin-top: 2px;
}

.radio-text {
  flex: 1;
}

.radio-text strong {
  display: block;
  color: #2c3e50;
  margin-bottom: 4px;
}

.radio-text small {
  color: #6c757d;
  font-size: 14px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  margin: 5px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #0056b3;
}

.btn-primary:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #545b62;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover:not(:disabled) {
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

.btn-remove {
  background: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.goals-list {
  margin-top: 20px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.goal-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  margin-bottom: 10px;
  background: white;
  border-radius: 6px;
  border-left: 4px solid #007bff;
}

.goal-info {
  flex: 1;
}

.goal-info small {
  color: #6c757d;
}

.profile-summary {
  display: grid;
  gap: 30px;
}

.summary-section {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.summary-section h3 {
  color: #2c3e50;
  margin-bottom: 15px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 8px;
}

.goal-summary {
  padding: 10px;
  margin-bottom: 10px;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #28a745;
}

.step-navigation {
  display: flex;
  justify-content: space-between;
  padding: 20px 40px;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

@media (max-width: 768px) {
  .wizard-container {
    margin: 10px;
    border-radius: 15px;
  }
  
  .step-content {
    padding: 20px;
  }
  
  .progress-bar {
    flex-direction: column;
    gap: 10px;
  }
  
  .progress-step:not(:last-child)::after {
    display: none;
  }
}
</style> 