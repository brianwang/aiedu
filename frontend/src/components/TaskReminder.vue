<template>
  <div class="task-reminder">
    <!-- 提醒设置 -->
    <div class="reminder-settings" v-if="showSettings">
      <h3>⏰ 提醒设置</h3>
      <div class="settings-form">
        <div class="form-group">
          <label>每日提醒时间：</label>
          <input 
            type="time" 
            v-model="reminderTime" 
            class="form-control"
            @change="updateReminderTime"
          />
        </div>
        <div class="form-group">
          <label>提醒频率：</label>
          <select v-model="reminderFrequency" class="form-control" @change="updateReminderFrequency">
            <option value="daily">每日</option>
            <option value="weekdays">工作日</option>
            <option value="custom">自定义</option>
          </select>
        </div>
        <div class="form-group">
          <label>
            <input 
              type="checkbox" 
              v-model="enableNotifications" 
              @change="toggleNotifications"
            />
            启用浏览器通知
          </label>
        </div>
      </div>
    </div>

    <!-- 今日提醒 -->
    <div v-if="todayReminders.length > 0" class="today-reminders">
      <h3>📅 今日提醒</h3>
      <div class="reminder-list">
        <div 
          v-for="reminder in todayReminders" 
          :key="reminder.id"
          :class="['reminder-item', { 'urgent': reminder.isUrgent }]"
        >
          <div class="reminder-icon">
            {{ getReminderIcon(reminder.type) }}
          </div>
          <div class="reminder-content">
            <div class="reminder-title">{{ reminder.title }}</div>
            <div class="reminder-time">{{ formatTime(reminder.scheduled_time) }}</div>
            <div class="reminder-description">{{ reminder.description }}</div>
          </div>
          <div class="reminder-actions">
            <button 
              @click="dismissReminder(reminder.id)"
              class="btn btn-sm btn-outline"
            >
              忽略
            </button>
            <button 
              @click="handleReminder(reminder)"
              class="btn btn-sm btn-primary"
            >
              处理
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 即将到来的提醒 -->
    <div v-if="upcomingReminders.length > 0" class="upcoming-reminders">
      <h3>⏳ 即将到来</h3>
      <div class="reminder-list">
        <div 
          v-for="reminder in upcomingReminders" 
          :key="reminder.id"
          class="reminder-item"
        >
          <div class="reminder-icon">
            {{ getReminderIcon(reminder.type) }}
          </div>
          <div class="reminder-content">
            <div class="reminder-title">{{ reminder.title }}</div>
            <div class="reminder-time">{{ formatTime(reminder.scheduled_time) }}</div>
            <div class="reminder-description">{{ reminder.description }}</div>
          </div>
          <div class="reminder-actions">
            <button 
              @click="editReminder(reminder.id)"
              class="btn btn-sm btn-outline"
            >
              编辑
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="todayReminders.length === 0 && upcomingReminders.length === 0" class="empty-state">
      <div class="empty-icon">⏰</div>
      <p>暂无学习提醒</p>
      <button @click="createReminder" class="btn btn-primary">创建提醒</button>
    </div>

    <!-- 创建提醒对话框 -->
    <div v-if="showCreateDialog" class="modal-overlay" @click="closeCreateDialog">
      <div class="modal-content" @click.stop>
        <h3>创建学习提醒</h3>
        <form @submit.prevent="submitReminder">
          <div class="form-group">
            <label>提醒标题：</label>
            <input 
              type="text" 
              v-model="newReminder.title" 
              class="form-control" 
              required
              placeholder="例如：数学练习"
            />
          </div>
          <div class="form-group">
            <label>提醒描述：</label>
            <textarea 
              v-model="newReminder.description" 
              class="form-control"
              placeholder="提醒的具体内容..."
            ></textarea>
          </div>
          <div class="form-group">
            <label>提醒时间：</label>
            <input 
              type="datetime-local" 
              v-model="newReminder.scheduled_time" 
              class="form-control" 
              required
            />
          </div>
          <div class="form-group">
            <label>提醒类型：</label>
            <select v-model="newReminder.type" class="form-control">
              <option value="task">任务提醒</option>
              <option value="break">休息提醒</option>
              <option value="review">复习提醒</option>
              <option value="custom">自定义</option>
            </select>
          </div>
          <div class="form-actions">
            <button type="button" @click="closeCreateDialog" class="btn btn-outline">取消</button>
            <button type="submit" class="btn btn-primary">创建</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useApi } from '@/composables/useApi'

const api = useApi()

// 响应式数据
const reminders = ref([])
const showSettings = ref(false)
const showCreateDialog = ref(false)
const reminderTime = ref('09:00')
const reminderFrequency = ref('daily')
const enableNotifications = ref(true)

const newReminder = ref({
  title: '',
  description: '',
  scheduled_time: '',
  type: 'task'
})

// 计算属性
const todayReminders = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return reminders.value.filter(reminder => {
    const reminderDate = new Date(reminder.scheduled_time).toISOString().split('T')[0]
    return reminderDate === today && !reminder.dismissed
  })
})

const upcomingReminders = computed(() => {
  const now = new Date()
  const today = now.toISOString().split('T')[0]
  return reminders.value.filter(reminder => {
    const reminderDate = new Date(reminder.scheduled_time).toISOString().split('T')[0]
    return reminderDate > today && !reminder.dismissed
  }).slice(0, 5) // 只显示最近5个
})

// 方法
const loadReminders = async () => {
  try {
    const response = await api.get('/api/v1/learning/reminders')
    reminders.value = response || []
  } catch (error) {
    console.error('加载提醒失败:', error)
    // 使用示例数据
    reminders.value = createSampleReminders()
  }
}

const createSampleReminders = () => {
  const now = new Date()
  const today = new Date(now)
  const tomorrow = new Date(now)
  tomorrow.setDate(tomorrow.getDate() + 1)
  
  return [
    {
      id: 1,
      title: '数学练习时间',
      description: '完成今日数学练习题',
      type: 'task',
      scheduled_time: new Date(today.setHours(14, 0, 0, 0)).toISOString(),
      dismissed: false,
      isUrgent: true
    },
    {
      id: 2,
      title: '休息提醒',
      description: '学习45分钟了，该休息一下',
      type: 'break',
      scheduled_time: new Date(today.setHours(15, 30, 0, 0)).toISOString(),
      dismissed: false,
      isUrgent: false
    },
    {
      id: 3,
      title: '英语复习',
      description: '复习昨天的英语语法',
      type: 'review',
      scheduled_time: new Date(tomorrow.setHours(10, 0, 0, 0)).toISOString(),
      dismissed: false,
      isUrgent: false
    }
  ]
}

const getReminderIcon = (type) => {
  const icons = {
    'task': '📝',
    'break': '☕',
    'review': '🔄',
    'custom': '⏰'
  }
  return icons[type] || '⏰'
}

const formatTime = (timeString) => {
  const date = new Date(timeString)
  return date.toLocaleString('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const dismissReminder = async (reminderId) => {
  try {
    const reminder = reminders.value.find(r => r.id === reminderId)
    if (reminder) {
      reminder.dismissed = true
    }
    
    // 调用API更新提醒状态
    try {
      await api.put(`/api/v1/learning/reminders/${reminderId}`, { dismissed: true })
    } catch (error) {
      console.warn('更新提醒状态失败:', error)
    }
  } catch (error) {
    console.error('忽略提醒失败:', error)
  }
}

const handleReminder = (reminder) => {
  // 根据提醒类型执行相应操作
  switch (reminder.type) {
    case 'task':
      // 跳转到任务页面
      console.log('处理任务提醒:', reminder)
      break
    case 'break':
      // 显示休息提示
      alert('该休息了！建议休息5-10分钟。')
      break
    case 'review':
      // 跳转到复习页面
      console.log('处理复习提醒:', reminder)
      break
    default:
      console.log('处理自定义提醒:', reminder)
  }
  
  // 标记为已处理
  dismissReminder(reminder.id)
}

const editReminder = (reminderId) => {
  const reminder = reminders.value.find(r => r.id === reminderId)
  if (reminder) {
    newReminder.value = { ...reminder }
    showCreateDialog.value = true
  }
}

const createReminder = () => {
  newReminder.value = {
    title: '',
    description: '',
    scheduled_time: '',
    type: 'task'
  }
  showCreateDialog.value = true
}

const closeCreateDialog = () => {
  showCreateDialog.value = false
}

const submitReminder = async () => {
  try {
    const response = await api.post('/api/v1/learning/reminders', newReminder.value)
    reminders.value.push(response)
    closeCreateDialog()
  } catch (error) {
    console.error('创建提醒失败:', error)
    alert('创建提醒失败，请重试')
  }
}

const updateReminderTime = async () => {
  try {
    await api.put('/api/v1/learning/reminder-settings', { reminder_time: reminderTime.value })
  } catch (error) {
    console.error('更新提醒时间失败:', error)
  }
}

const updateReminderFrequency = async () => {
  try {
    await api.put('/api/v1/learning/reminder-settings', { reminder_frequency: reminderFrequency.value })
  } catch (error) {
    console.error('更新提醒频率失败:', error)
  }
}

const toggleNotifications = async () => {
  if (enableNotifications.value) {
    // 请求浏览器通知权限
    if ('Notification' in window) {
      const permission = await Notification.requestPermission()
      if (permission !== 'granted') {
        enableNotifications.value = false
        alert('需要通知权限才能启用提醒功能')
      }
    }
  }
  
  try {
    await api.put('/api/v1/learning/reminder-settings', { enable_notifications: enableNotifications.value })
  } catch (error) {
    console.error('更新通知设置失败:', error)
  }
}

// 检查提醒
const checkReminders = () => {
  const now = new Date()
  const currentTime = now.getTime()
  
  reminders.value.forEach(reminder => {
    if (!reminder.dismissed && !reminder.notified) {
      const reminderTime = new Date(reminder.scheduled_time).getTime()
      const timeDiff = reminderTime - currentTime
      
      // 如果提醒时间到了（允许5分钟误差）
      if (timeDiff <= 0 && timeDiff > -300000) {
        reminder.notified = true
        
        // 显示浏览器通知
        if (enableNotifications.value && 'Notification' in window && Notification.permission === 'granted') {
          new Notification(reminder.title, {
            body: reminder.description,
            icon: '/favicon.ico'
          })
        }
        
        // 显示页面提醒
        showPageNotification(reminder)
      }
    }
  })
}

const showPageNotification = (reminder) => {
  // 创建页面通知元素
  const notification = document.createElement('div')
  notification.className = 'page-notification'
  notification.innerHTML = `
    <div class="notification-content">
      <h4>${reminder.title}</h4>
      <p>${reminder.description}</p>
      <div class="notification-actions">
        <button onclick="this.parentElement.parentElement.parentElement.remove()">忽略</button>
        <button onclick="handleReminderNotification(${reminder.id})">处理</button>
      </div>
    </div>
  `
  
  document.body.appendChild(notification)
  
  // 5秒后自动移除
  setTimeout(() => {
    if (notification.parentElement) {
      notification.remove()
    }
  }, 5000)
}

// 全局函数，用于处理通知按钮点击
window.handleReminderNotification = (reminderId) => {
  const reminder = reminders.value.find(r => r.id === reminderId)
  if (reminder) {
    handleReminder(reminder)
  }
}

// 定时检查提醒
let reminderInterval

onMounted(() => {
  loadReminders()
  
  // 每分钟检查一次提醒
  reminderInterval = setInterval(checkReminders, 60000)
  
  // 立即检查一次
  checkReminders()
})

onUnmounted(() => {
  if (reminderInterval) {
    clearInterval(reminderInterval)
  }
})
</script>

<style scoped>
.task-reminder {
  padding: 20px;
}

.reminder-settings {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.settings-form {
  display: grid;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-group label {
  font-weight: 500;
  color: var(--text-primary);
}

.form-control {
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 14px;
}

.today-reminders,
.upcoming-reminders {
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.reminder-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.reminder-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-secondary);
  transition: all 0.3s ease;
}

.reminder-item.urgent {
  border-color: var(--warning-color);
  background: rgba(255, 193, 7, 0.1);
}

.reminder-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-color);
  color: white;
  border-radius: 50%;
}

.reminder-content {
  flex: 1;
}

.reminder-title {
  font-weight: bold;
  color: var(--text-primary);
  margin-bottom: 5px;
}

.reminder-time {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 5px;
}

.reminder-description {
  font-size: 14px;
  color: var(--text-secondary);
}

.reminder-actions {
  display: flex;
  gap: 8px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

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
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

/* 页面通知样式 */
.page-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1001;
  max-width: 300px;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.notification-content h4 {
  margin: 0 0 10px 0;
  color: var(--text-primary);
}

.notification-content p {
  margin: 0 0 15px 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.notification-actions {
  display: flex;
  gap: 8px;
}

.notification-actions button {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.notification-actions button:first-child {
  background: var(--border-color);
  color: var(--text-primary);
}

.notification-actions button:last-child {
  background: var(--primary-color);
  color: white;
}

@media (max-width: 768px) {
  .reminder-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .reminder-actions {
    width: 100%;
    justify-content: flex-end;
  }
  
  .modal-content {
    width: 95%;
    margin: 20px;
  }
}
</style> 