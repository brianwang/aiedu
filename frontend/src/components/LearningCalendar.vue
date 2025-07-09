<template>
  <div class="learning-calendar">
    <div class="calendar-header">
      <h3>学习日历</h3>
      <div class="calendar-controls">
        <button @click="previousMonth" class="btn-icon">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
          </svg>
        </button>
        <span class="current-month">{{ currentMonthYear }}</span>
        <button @click="nextMonth" class="btn-icon">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/>
          </svg>
        </button>
      </div>
    </div>

    <div class="calendar-grid">
      <!-- 星期标题 -->
      <div class="calendar-weekdays">
        <div v-for="day in weekdays" :key="day" class="weekday">{{ day }}</div>
      </div>

      <!-- 日历日期 -->
      <div class="calendar-days">
        <div 
          v-for="day in calendarDays" 
          :key="day.date"
          :class="[
            'calendar-day',
            { 
              'other-month': !day.isCurrentMonth,
              'today': day.isToday,
              'has-task': day.hasTask,
              'task-completed': day.taskCompleted
            }
          ]"
          @click="selectDate(day)"
        >
          <span class="day-number">{{ day.dayNumber }}</span>
          <div v-if="day.hasTask" class="task-indicator">
            <div v-if="day.taskCompleted" class="task-dot completed">✓</div>
            <div v-else class="task-dot pending">●</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 今日提醒 -->
    <div v-if="todayTasks.length > 0" class="today-reminder">
      <h4>今日学习任务</h4>
      <div class="task-list">
        <div 
          v-for="task in todayTasks" 
          :key="task.id"
          :class="['task-item', `status-${task.status}`]"
        >
          <div class="task-info">
            <div class="task-title">{{ task.title }}</div>
            <div class="task-meta">
              <span class="task-time">{{ task.estimated_time }}分钟</span>
              <span class="task-type">{{ getTaskTypeText(task.task_type) }}</span>
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

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">📅</div>
      <p>今天没有学习任务</p>
      <button @click="createTask" class="btn btn-outline">添加任务</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const api = useApi()

// 响应式数据
const currentDate = ref(new Date())
const tasks = ref([])
const selectedDate = ref(null)

// 星期标题
const weekdays = ['日', '一', '二', '三', '四', '五', '六']

// 计算属性
const currentMonthYear = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth() + 1
  return `${year}年${month}月`
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const startDate = new Date(firstDay)
  startDate.setDate(startDate.getDate() - firstDay.getDay())
  
  const days = []
  const today = new Date()
  
  for (let i = 0; i < 42; i++) {
    const date = new Date(startDate)
    date.setDate(startDate.getDate() + i)
    
    const dayNumber = date.getDate()
    const isCurrentMonth = date.getMonth() === month
    const isToday = date.toDateString() === today.toDateString()
    
    // 检查该日期是否有任务
    const dateString = date.toISOString().split('T')[0]
    const dayTasks = tasks.value.filter(task => {
      if (!task.due_date) return false
      return task.due_date === dateString
    })
    
    const hasTask = dayTasks.length > 0
    const taskCompleted = hasTask && dayTasks.every(task => task.status === 'completed')
    
    days.push({
      date: dateString,
      dayNumber,
      isCurrentMonth,
      isToday,
      hasTask,
      taskCompleted,
      tasks: dayTasks
    })
  }
  
  return days
})

const todayTasks = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return tasks.value.filter(task => task.due_date === today)
})

// 方法
const loadTasks = async () => {
  try {
    // 首先尝试从AI学习计划获取任务
    const aiResponse = await api.get('/api/v1/ai/study-plan')
    if (aiResponse.data && aiResponse.data.tasks) {
      tasks.value = aiResponse.data.tasks.map(task => ({
        ...task,
        due_date: task.due_date || new Date().toISOString().split('T')[0],
        status: task.status || 'pending'
      }))
    }
    
    // 然后从学习计划API获取任务
    try {
      const plansResponse = await api.get('/api/v1/learning/plans')
      if (plansResponse && Array.isArray(plansResponse)) {
        const allTasks = []
        
        for (const plan of plansResponse) {
          try {
            const tasksResponse = await api.get(`/api/v1/learning/plans/${plan.id}/tasks`)
            if (Array.isArray(tasksResponse)) {
              allTasks.push(...tasksResponse)
            }
          } catch (error) {
            console.warn(`获取计划 ${plan.id} 的任务失败:`, error)
          }
        }
        
        // 合并任务，避免重复
        const existingTaskIds = new Set(tasks.value.map(t => t.id))
        const newTasks = allTasks.filter(task => !existingTaskIds.has(task.id))
        tasks.value.push(...newTasks)
      }
    } catch (error) {
      console.warn('获取学习计划任务失败:', error)
    }
  } catch (error) {
    console.error('加载任务失败:', error)
    tasks.value = []
  }
}

const createSampleTasks = () => {
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  return [
    {
      id: 1,
      title: '数学基础练习',
      description: '完成10道基础数学题目',
      task_type: 'practice',
      subject: '数学',
      estimated_time: 30,
      due_date: today.toISOString().split('T')[0],
      status: 'pending'
    },
    {
      id: 2,
      title: '英语语法复习',
      description: '复习过去时态语法规则',
      task_type: 'review',
      subject: '英语',
      estimated_time: 45,
      due_date: today.toISOString().split('T')[0],
      status: 'in_progress'
    },
    {
      id: 3,
      title: '物理概念学习',
      description: '学习牛顿运动定律',
      task_type: 'new_concept',
      subject: '物理',
      estimated_time: 60,
      due_date: tomorrow.toISOString().split('T')[0],
      status: 'pending'
    }
  ]
}

const previousMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() - 1,
    1
  )
}

const nextMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() + 1,
    1
  )
}

const selectDate = (day) => {
  selectedDate.value = day
  // 可以在这里显示选中日期的任务详情
  console.log('选中日期:', day.date, '任务:', day.tasks)
}

const startTask = async (taskId) => {
  try {
    // 更新本地状态
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.status = 'in_progress'
    }
    
    // 调用API更新任务状态
    try {
      const response = await api.put(`/api/v1/learning/tasks/${taskId}/status`, { 
        status: 'in_progress',
        started_at: new Date().toISOString()
      })
      
      // 如果API调用成功，使用返回的数据更新本地状态
      if (response && response.status === 'in_progress') {
        const taskIndex = tasks.value.findIndex(t => t.id === taskId)
        if (taskIndex >= 0) {
          tasks.value[taskIndex] = { ...tasks.value[taskIndex], ...response }
        }
      }
      
      console.log('任务状态已同步到数据库:', response)
    } catch (error) {
      console.error('更新任务状态失败:', error)
      // 如果API调用失败，恢复本地状态
      if (task) {
        task.status = 'pending'
      }
      alert('更新任务状态失败，请重试')
    }
  } catch (error) {
    console.error('开始任务失败:', error)
  }
}

const completeTask = async (taskId) => {
  try {
    // 更新本地状态
    const task = tasks.value.find(t => t.id === taskId)
    if (task) {
      task.status = 'completed'
    }
    
    // 调用API更新任务状态
    try {
      const response = await api.put(`/api/v1/learning/tasks/${taskId}/status`, { 
        status: 'completed',
        completed_at: new Date().toISOString()
      })
      
      // 如果API调用成功，使用返回的数据更新本地状态
      if (response && response.status === 'completed') {
        const taskIndex = tasks.value.findIndex(t => t.id === taskId)
        if (taskIndex >= 0) {
          tasks.value[taskIndex] = { ...tasks.value[taskIndex], ...response }
        }
      }
      
      // 记录学习进度
      try {
        await api.post('/api/v1/learning/progress', {
          task_id: taskId,
          study_time: task.estimated_time || 30,
          questions_answered: 1,
          correct_answers: 1,
          completed_at: new Date().toISOString()
        })
        console.log('学习进度已记录')
      } catch (progressError) {
        console.warn('记录学习进度失败:', progressError)
      }
      
      // 检查是否解锁新成就
      try {
        await checkAchievementUnlock()
      } catch (achievementError) {
        console.warn('检查成就解锁失败:', achievementError)
      }
      
      console.log('任务完成状态已同步到数据库:', response)
    } catch (error) {
      console.error('更新任务状态失败:', error)
      // 如果API调用失败，恢复本地状态
      if (task) {
        task.status = 'in_progress'
      }
      alert('更新任务状态失败，请重试')
    }
  } catch (error) {
    console.error('完成任务失败:', error)
  }
}

// 检查成就解锁
const checkAchievementUnlock = async () => {
  try {
    // 获取用户学习统计
    const statsResponse = await api.get('/api/v1/learning/statistics')
    if (statsResponse) {
      // 这里可以添加成就解锁逻辑
      console.log('检查成就解锁:', statsResponse)
    }
  } catch (error) {
    console.error('检查成就解锁失败:', error)
  }
}

const createTask = () => {
  // 跳转到创建任务页面或打开创建任务对话框
  console.log('创建新任务')
}

const getTaskTypeText = (type) => {
  const types = {
    'practice': '练习',
    'review': '复习',
    'new_concept': '新概念',
    'assessment': '评估'
  }
  return types[type] || type
}

// 生命周期
onMounted(() => {
  loadTasks()
})
</script>

<style scoped>
.learning-calendar {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.calendar-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
}

.calendar-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-icon {
  background: #f8f9fa;
  border: none;
  color: #6c757d;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  background-color: #e9ecef;
  color: #495057;
}

.btn-icon svg {
  width: 18px;
  height: 18px;
}

.current-month {
  font-weight: 500;
  color: #2c3e50;
  font-size: 1rem;
  min-width: 80px;
  text-align: center;
}

.calendar-grid {
  margin-bottom: 16px;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
  margin-bottom: 8px;
}

.weekday {
  text-align: center;
  font-size: 0.85rem;
  font-weight: 500;
  color: #6c757d;
  padding: 8px 0;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.calendar-day {
  aspect-ratio: 1;
  min-height: 36px;
  font-size: 0.9rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  padding: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border: 1px solid transparent;
}

.calendar-day:hover {
  background-color: #e9ecef;
  border-color: #dee2e6;
}

.calendar-day.other-month {
  color: #adb5bd;
  background: #f8f9fa;
}

.calendar-day.today {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: bold;
  border-color: #667eea;
}

.calendar-day.has-task {
  background-color: #e3f2fd;
  border: 1px solid #bbdefb;
}

.calendar-day.task-completed {
  background-color: #e8f5e8;
  border: 1px solid #c8e6c9;
}

.day-number {
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 2px;
}

.task-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
}

.task-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  font-size: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-dot.pending {
  background-color: #ffc107;
}

.task-dot.completed {
  background-color: #28a745;
  color: white;
}

.today-reminder {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-top: 12px;
}

.today-reminder h4 {
  margin: 0 0 12px 0;
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 600;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: white;
  border-radius: 8px;
  border-left: 3px solid #667eea;
  font-size: 0.9rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.task-item:hover {
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.task-item.status-completed {
  border-left-color: #28a745;
  opacity: 0.8;
}

.task-item.status-in_progress {
  border-left-color: #ffc107;
}

.task-info {
  flex: 1;
}

.task-title {
  font-size: 0.95rem;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 4px;
}

.task-meta {
  display: flex;
  gap: 8px;
  font-size: 0.8rem;
  color: #6c757d;
}

.task-time {
  color: #667eea;
  font-weight: 500;
}

.task-type {
  background: #667eea;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.task-actions {
  display: flex;
  gap: 6px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-success:hover {
  background: #218838;
  transform: translateY(-1px);
}

.btn-outline {
  background: none;
  border: 1px solid #dee2e6;
  color: #6c757d;
}

.btn-outline:hover {
  background: #f8f9fa;
  border-color: #adb5bd;
}

.status-badge {
  font-size: 0.8rem;
  color: #28a745;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #6c757d;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.empty-state p {
  margin: 0 0 12px 0;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .learning-calendar {
    padding: 12px;
  }
  
  .calendar-header h3 {
    font-size: 1.1rem;
  }
  
  .current-month {
    font-size: 0.9rem;
    min-width: 70px;
  }
  
  .calendar-day {
    min-height: 32px;
    font-size: 0.85rem;
  }
  
  .day-number {
    font-size: 0.85rem;
  }
  
  .task-item {
    padding: 10px;
    font-size: 0.85rem;
  }
  
  .task-title {
    font-size: 0.9rem;
  }
}
</style> 