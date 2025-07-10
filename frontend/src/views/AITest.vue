<template>
  <div class="ai-test-container">
    <div class="header">
      <h1>AI智能测试系统</h1>
      <p>基于DeepSeek大模型的智能教育功能</p>
    </div>

    <div class="tabs">
      <button 
        :class="['tab-btn', { active: activeTab === 'generate' }]"
        @click="activeTab = 'generate'"
      >
        智能组卷
      </button>
      <button 
        :class="['tab-btn', { active: activeTab === 'recommend' }]"
        @click="activeTab = 'recommend'"
      >
        题目推荐
      </button>
      <button 
        :class="['tab-btn', { active: activeTab === 'plan' }]"
        @click="activeTab = 'plan'"
      >
        学习计划
      </button>
      <button 
        :class="['tab-btn', { active: activeTab === 'analysis' }]"
        @click="activeTab = 'analysis'"
      >
        学习分析
      </button>
    </div>

    <!-- 智能组卷 -->
    <div v-if="activeTab === 'generate'" class="tab-content">
      <div class="exam-generator">
        <h2>AI智能组卷</h2>
        <div class="form-group">
          <label>学科：</label>
          <select v-model="examForm.subject" class="form-control">
            <option value="数学">数学</option>
            <option value="语文">语文</option>
            <option value="英语">英语</option>
            <option value="物理">物理</option>
            <option value="化学">化学</option>
            <option value="生物">生物</option>
            <option value="历史">历史</option>
            <option value="地理">地理</option>
            <option value="政治">政治</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>难度等级：</label>
          <div class="difficulty-selector">
            <button 
              v-for="level in 5" 
              :key="level"
              :class="['difficulty-btn', { active: examForm.difficulty === level }]"
              @click="examForm.difficulty = level"
            >
              {{ level }}星
            </button>
          </div>
        </div>
        
        <div class="form-group">
          <label>试卷类型：</label>
          <select v-model="examForm.examType" class="form-control">
            <option value="comprehensive">综合测试</option>
            <option value="unit">单元测试</option>
            <option value="midterm">期中考试</option>
            <option value="final">期末考试</option>
            <option value="practice">练习卷</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>题目分布：</label>
          <div class="question-distribution">
            <div v-for="(count, type) in examForm.questionDistribution" :key="type" class="distribution-item">
              <label>{{ getQuestionTypeName(type) }}：</label>
              <input 
                type="number" 
                v-model.number="examForm.questionDistribution[type]" 
                min="0" 
                max="20"
                class="form-control small"
              />
            </div>
          </div>
        </div>
        
        <button @click="generateExam" :disabled="generating" class="btn btn-primary">
          {{ generating ? '生成中...' : '生成试卷' }}
        </button>
      </div>
      
      <!-- 生成的试卷 -->
      <div v-if="generatedExam" class="generated-exam">
        <h3>{{ generatedExam.exam_info.title }}</h3>
        <div class="exam-info">
          <p><strong>学科：</strong>{{ generatedExam.exam_info.subject }}</p>
          <p><strong>难度：</strong>{{ generatedExam.exam_info.difficulty }}星</p>
          <p><strong>总分：</strong>{{ generatedExam.exam_info.total_score }}分</p>
          <p><strong>时长：</strong>{{ generatedExam.exam_info.duration }}分钟</p>
          <p><strong>题目数：</strong>{{ generatedExam.exam_info.total_questions }}道</p>
        </div>
        
        <div class="questions-section">
          <h4>题目列表</h4>
          <div v-for="(question, index) in generatedExam.questions" :key="index" class="question-item">
            <div class="question-header">
              <span class="question-number">{{ index + 1 }}.</span>
              <span class="question-type">{{ getQuestionTypeName(question.question_type) }}</span>
              <span class="question-score">({{ question.score }}分)</span>
            </div>
            <div class="question-content">{{ question.content }}</div>
            <div v-if="question.options" class="question-options">
              <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option">
                {{ String.fromCharCode(65 + optIndex) }}. {{ option }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="exam-actions">
          <button @click="downloadExam" class="btn btn-secondary">下载试卷</button>
          <button @click="showAnswers = !showAnswers" class="btn btn-info">
            {{ showAnswers ? '隐藏答案' : '查看答案' }}
          </button>
        </div>
        
        <!-- 答案页 -->
        <div v-if="showAnswers" class="answers-section">
          <h4>{{ generatedExam.answer_sheet.title }}</h4>
          <div v-for="answer in generatedExam.answer_sheet.answers" :key="answer.question_id" class="answer-item">
            <span class="answer-number">{{ answer.question_id }}.</span>
            <span class="answer-content">{{ answer.answer }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 题目推荐 -->
    <div v-if="activeTab === 'recommend'" class="tab-content">
      <div class="question-recommendation">
        <h2>AI题目推荐</h2>
        <div class="form-group">
          <label>学科：</label>
          <select v-model="recommendForm.subject" class="form-control">
            <option value="">全部学科</option>
            <option value="数学">数学</option>
            <option value="语文">语文</option>
            <option value="英语">英语</option>
            <option value="物理">物理</option>
            <option value="化学">化学</option>
            <option value="生物">生物</option>
            <option value="历史">历史</option>
            <option value="地理">地理</option>
            <option value="政治">政治</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>推荐数量：</label>
          <input type="number" v-model.number="recommendForm.count" min="1" max="20" class="form-control" />
        </div>
        
        <button @click="recommendQuestions" :disabled="recommending" class="btn btn-primary">
          {{ recommending ? '推荐中...' : '获取推荐' }}
        </button>
      </div>
      
      <div v-if="recommendedQuestions.length > 0" class="recommended-questions">
        <h3>推荐题目</h3>
        <div v-for="(question, index) in recommendedQuestions" :key="index" class="question-card">
          <div class="question-header">
            <span class="question-subject">{{ question.subject }}</span>
            <span class="question-difficulty">难度: {{ question.difficulty }}</span>
          </div>
          <div class="question-content">{{ question.content }}</div>
          <div class="question-footer">
            <span class="question-type">{{ getQuestionTypeName(question.question_type) }}</span>
            <button @click="practiceQuestion(question)" class="btn btn-sm btn-primary">练习</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习计划 -->
    <div v-if="activeTab === 'plan'" class="tab-content">
      <div class="learning-plan">
        <h2>AI学习计划</h2>
        <div class="form-group">
          <label>目标学科：</label>
          <select v-model="planForm.subject" class="form-control">
            <option value="数学">数学</option>
            <option value="语文">语文</option>
            <option value="英语">英语</option>
            <option value="物理">物理</option>
            <option value="化学">化学</option>
            <option value="生物">生物</option>
            <option value="历史">历史</option>
            <option value="地理">地理</option>
            <option value="政治">政治</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>学习目标：</label>
          <textarea v-model="planForm.goal" placeholder="描述你的学习目标..." class="form-control"></textarea>
        </div>
        
        <div class="form-group">
          <label>学习时长（天）：</label>
          <input type="number" v-model.number="planForm.duration" min="1" max="365" class="form-control" />
        </div>
        
        <button @click="createLearningPlan" :disabled="creatingPlan" class="btn btn-primary">
          {{ creatingPlan ? '生成中...' : '生成学习计划' }}
        </button>
      </div>
      
      <div v-if="learningPlan" class="generated-plan">
        <h3>个性化学习计划</h3>
        <div class="plan-info">
          <p><strong>学科：</strong>{{ learningPlan.subject }}</p>
          <p><strong>目标：</strong>{{ learningPlan.goal }}</p>
          <p><strong>时长：</strong>{{ learningPlan.duration }}天</p>
        </div>
        
        <div class="plan-stages">
          <h4>学习阶段</h4>
          <div v-for="(stage, index) in learningPlan.stages" :key="index" class="stage-item">
            <div class="stage-header">
              <span class="stage-number">第{{ index + 1 }}阶段</span>
              <span class="stage-duration">{{ stage.duration }}天</span>
            </div>
            <div class="stage-content">
              <h5>{{ stage.title }}</h5>
              <p>{{ stage.description }}</p>
              <ul class="stage-tasks">
                <li v-for="task in stage.tasks" :key="task">{{ task }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习分析 -->
    <div v-if="activeTab === 'analysis'" class="tab-content">
      <div class="learning-analysis">
        <h2>AI学习分析</h2>
        <button @click="analyzeLearning" :disabled="analyzing" class="btn btn-primary">
          {{ analyzing ? '分析中...' : '开始分析' }}
        </button>
      </div>
      
      <div v-if="learningAnalysis" class="analysis-results">
        <h3>学习分析报告</h3>
        <div class="analysis-section">
          <h4>学习概况</h4>
          <div class="analysis-grid">
            <div class="analysis-item">
              <span class="label">总学习时长</span>
              <span class="value">{{ learningAnalysis.total_study_time }}小时</span>
            </div>
            <div class="analysis-item">
              <span class="label">完成题目数</span>
              <span class="value">{{ learningAnalysis.total_questions }}</span>
            </div>
            <div class="analysis-item">
              <span class="label">平均正确率</span>
              <span class="value">{{ learningAnalysis.accuracy_rate }}%</span>
            </div>
            <div class="analysis-item">
              <span class="label">学习效率</span>
              <span class="value">{{ learningAnalysis.efficiency_score }}</span>
            </div>
          </div>
        </div>
        
        <div class="analysis-section">
          <h4>学科表现</h4>
          <div v-for="subject in learningAnalysis.subject_performance" :key="subject.name" class="subject-performance">
            <div class="subject-header">
              <span class="subject-name">{{ subject.name }}</span>
              <span class="subject-score">{{ subject.score }}分</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: subject.score + '%' }"></div>
            </div>
          </div>
        </div>
        
        <div class="analysis-section">
          <h4>学习建议</h4>
          <ul class="suggestions">
            <li v-for="suggestion in learningAnalysis.suggestions" :key="suggestion">{{ suggestion }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { aiApi } from '@/api/ai'

const authStore = useAuthStore()

// 标签页状态
const activeTab = ref('generate')

// 智能组卷
const examForm = reactive({
  subject: '数学',
  difficulty: 3,
  examType: 'comprehensive',
  questionDistribution: {
    single_choice: 10,
    multiple_choice: 5,
    fill_blank: 5,
    short_answer: 3,
    essay: 2
  }
})

const generating = ref(false)
const generatedExam = ref(null)
const showAnswers = ref(false)

// 题目推荐
const recommendForm = reactive({
  subject: '',
  count: 10
})

const recommending = ref(false)
const recommendedQuestions = ref([])

// 学习计划
const planForm = reactive({
  subject: '数学',
  goal: '',
  duration: 30
})

const creatingPlan = ref(false)
const learningPlan = ref(null)

// 学习分析
const analyzing = ref(false)
const learningAnalysis = ref(null)

// 生成试卷
const generateExam = async () => {
  if (!authStore.isAuthenticated) {
    alert('只有教师可以生成试卷')
    return
  }
  
  generating.value = true
  try {
    const formData = new FormData()
    formData.append('subject', examForm.subject)
    formData.append('difficulty', examForm.difficulty.toString())
    formData.append('exam_type', examForm.examType)
    formData.append('question_distribution', JSON.stringify(examForm.questionDistribution))
    
    const response = await aiApi.generateExam(formData)
    generatedExam.value = response.data
    showAnswers.value = false
  } catch (error) {
    console.error('生成试卷失败:', error)
    alert('生成试卷失败')
  } finally {
    generating.value = false
  }
}

// 推荐题目
const recommendQuestions = async () => {
  recommending.value = true
  try {
    const response = await aiApi.recommendQuestions({
      subject: recommendForm.subject || undefined,
      count: recommendForm.count
    })
    recommendedQuestions.value = response.data
  } catch (error) {
    console.error('推荐题目失败:', error)
    alert('推荐题目失败')
  } finally {
    recommending.value = false
  }
}

// 创建学习计划
const createLearningPlan = async () => {
  creatingPlan.value = true
  try {
    const response = await aiApi.createStudyPlan({
      subject: planForm.subject,
      goal: planForm.goal,
      duration: planForm.duration
    })
    learningPlan.value = response.data
  } catch (error) {
    console.error('创建学习计划失败:', error)
    alert('创建学习计划失败')
  } finally {
    creatingPlan.value = false
  }
}

// 分析学习
const analyzeLearning = async () => {
  analyzing.value = true
  try {
    const response = await aiApi.analyzeLearningPattern()
    learningAnalysis.value = response.data
  } catch (error) {
    console.error('学习分析失败:', error)
    alert('学习分析失败')
  } finally {
    analyzing.value = false
  }
}

// 练习题目
const practiceQuestion = (question: any) => {
  // 跳转到题目练习页面
  console.log('练习题目:', question)
}

// 下载试卷
const downloadExam = () => {
  if (!generatedExam.value) return
  
  const examData = {
    title: generatedExam.value.exam_info.title,
    questions: generatedExam.value.questions,
    answers: generatedExam.value.answer_sheet.answers
  }
  
  const blob = new Blob([JSON.stringify(examData, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${examData.title}.json`
  a.click()
  URL.revokeObjectURL(url)
}

// 获取题目类型名称
const getQuestionTypeName = (type: string) => {
  const typeNames: Record<string, string> = {
    single_choice: '单选题',
    multiple_choice: '多选题',
    fill_blank: '填空题',
    short_answer: '简答题',
    essay: '论述题'
  }
  return typeNames[type] || type
}
</script>

<style scoped>
.ai-test-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.header p {
  color: #7f8c8d;
  font-size: 16px;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 2px solid #ecf0f1;
  padding-bottom: 10px;
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: #ecf0f1;
  color: #7f8c8d;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.tab-btn.active {
  background: #3498db;
  color: white;
}

.tab-btn:hover {
  background: #2980b9;
  color: white;
}

.tab-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 12px;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: #3498db;
}

.form-control.small {
  width: 80px;
}

.difficulty-selector {
  display: flex;
  gap: 10px;
}

.difficulty-btn {
  padding: 8px 16px;
  border: 2px solid #ecf0f1;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.difficulty-btn.active {
  border-color: #3498db;
  background: #3498db;
  color: white;
}

.question-distribution {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.distribution-item label {
  margin-bottom: 0;
  min-width: 80px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  margin-right: 10px;
}

.btn-primary {
  background: #3498db;
  color: white;
}

.btn-primary:hover {
  background: #2980b9;
}

.btn-secondary {
  background: #95a5a6;
  color: white;
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.generated-exam {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.exam-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.questions-section {
  margin: 20px 0;
}

.question-item {
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.question-number {
  font-weight: bold;
  color: #3498db;
}

.question-type {
  background: #ecf0f1;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.question-score {
  color: #e74c3c;
  font-weight: bold;
}

.question-content {
  margin-bottom: 10px;
  line-height: 1.6;
}

.question-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option {
  padding: 8px 12px;
  background: #f8f9fa;
  border-radius: 4px;
}

.exam-actions {
  margin: 20px 0;
  padding: 15px;
  background: white;
  border-radius: 8px;
}

.answers-section {
  margin-top: 20px;
  padding: 20px;
  background: #e8f5e8;
  border-radius: 8px;
}

.answer-item {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}

.answer-number {
  font-weight: bold;
  color: #27ae60;
}

.question-recommendation,
.learning-plan,
.learning-analysis {
  margin-bottom: 30px;
}

.recommended-questions {
  margin-top: 30px;
}

.question-card {
  margin-bottom: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.question-card .question-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.question-subject {
  background: #3498db;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.question-difficulty {
  color: #e74c3c;
  font-weight: bold;
}

.question-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.generated-plan {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.plan-info {
  margin-bottom: 20px;
}

.stage-item {
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  border-left: 4px solid #27ae60;
}

.stage-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.stage-number {
  font-weight: bold;
  color: #27ae60;
}

.stage-duration {
  color: #7f8c8d;
}

.stage-tasks {
  margin-top: 10px;
  padding-left: 20px;
}

.analysis-results {
  margin-top: 30px;
}

.analysis-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.analysis-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background: white;
  border-radius: 8px;
}

.analysis-item .label {
  font-weight: 600;
  color: #2c3e50;
}

.analysis-item .value {
  font-size: 18px;
  font-weight: bold;
  color: #3498db;
}

.subject-performance {
  margin-bottom: 15px;
}

.subject-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.subject-name {
  font-weight: 600;
}

.subject-score {
  color: #3498db;
  font-weight: bold;
}

.progress-bar {
  height: 8px;
  background: #ecf0f1;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #3498db;
  transition: width 0.3s;
}

.suggestions {
  padding-left: 20px;
}

.suggestions li {
  margin-bottom: 8px;
  line-height: 1.6;
}
</style> 