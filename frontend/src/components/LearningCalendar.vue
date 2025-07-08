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
    const response = await api.get('/api/v1/learning/plans')
    const allTasks = []
    
    for (const plan of response) {
      const tasksResponse = await api.get(`/api/v1/learning/plans/${plan.id}/tasks`)
      allTasks.push(...tasksResponse)
    }
    
    tasks.value = allTasks
  } catch (error) {
    console.error('加载任务失败:', error)
  }
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
  // 这里可以添加日期选择逻辑，比如显示该日期的任务详情
}

const startTask = async (taskId) => {
  try {
    await api.put(`/api/v1/learning/tasks/${taskId}/status`, { status: 'in_progress' })
    await loadTasks()
  } catch (error) {
    console.error('开始任务失败:', error)
  }
}

const completeTask = async (taskId) => {
  try {
    await api.put(`/api/v1/learning/tasks/${taskId}/status`, { status: 'completed' })
    await loadTasks()
  } catch (error) {
    console.error('完成任务失败:', error)
  }
}

const createTask = () => {
  // 跳转到创建任务页面或打开创建任务弹窗
  console.log('创建新任务')
}

const getTaskTypeText = (taskType) => {
  const typeMap = {
    'study': '学习',
    'practice': '练习',
    'review': '复习',
    'assessment': '测试'
  }
  return typeMap[taskType] || taskType
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
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-header h3 {
  color: #2c3e50;
  margin: 0;
}

.calendar-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.current-month {
  font-weight: 600;
  color: #2c3e50;
  min-width: 100px;
  text-align: center;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  color: #6c757d;
  transition: all 0.3s;
}

.btn-icon:hover {
  background: #f8f9fa;
  color: #007bff;
}

.btn-icon svg {
  width: 20px;
  height: 20px;
}

.calendar-grid {
  margin-bottom: 20px;
}

.calendar-weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  margin-bottom: 5px;
}

.weekday {
  text-align: center;
  padding: 10px;
  font-weight: 600;
  color: #6c757d;
  background: #f8f9fa;
  border-radius: 6px;
}

.calendar-days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
}

.calendar-day {
  aspect-ratio: 1;
  padding: 5px;
  border: 1px solid #e9ecef;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.calendar-day:hover {
  background: #f8f9fa;
  border-color: #007bff;
}

.calendar-day.other-month {
  color: #adb5bd;
  background: #f8f9fa;
}

.calendar-day.today {
  background: #e3f2fd;
  border-color: #2196f3;
  font-weight: bold;
}

.calendar-day.has-task {
  background: #fff3cd;
  border-color: #ffc107;
}

.calendar-day.task-completed {
  background: #d4edda;
  border-color: #28a745;
}

.day-number {
  font-size: 14px;
  font-weight: 500;
}

.task-indicator {
  position: absolute;
  bottom: 2px;
  right: 2px;
}

.task-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  font-size: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.task-dot.pending {
  background: #ffc107;
}

.task-dot.completed {
  background: #28a745;
}

.today-reminder {
  border-top: 1px solid #e9ecef;
  padding-top: 20px;
}

.today-reminder h4 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.task-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.task-item.status-completed {
  border-left-color: #28a745;
  background: #f8fff9;
}

.task-info {
  flex: 1;
}

.task-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 4px;
}

.task-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #6c757d;
}

.task-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-sm {
  padding: 4px 8px;
  font-size: 11px;
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
  border: 1px solid #007bff;
}

.btn-outline:hover {
  background: #007bff;
  color: white;
}

.status-badge {
  font-size: 11px;
  color: #28a745;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #6c757d;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.empty-state p {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .calendar-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .calendar-day {
    padding: 2px;
  }
  
  .day-number {
    font-size: 12px;
  }
  
  .task-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style> 