<template>
  <div class="achievement-system">
    <div class="achievement-header">
      <h3>学习成就</h3>
      <div class="achievement-stats">
        <span class="stat-item">
          <span class="stat-number">{{ totalAchievements }}</span>
          <span class="stat-label">总成就</span>
        </span>
        <span class="stat-item">
          <span class="stat-number">{{ totalPoints }}</span>
          <span class="stat-label">总点数</span>
        </span>
      </div>
    </div>

    <!-- 成就分类 -->
    <div class="achievement-categories">
      <button 
        v-for="category in categories" 
        :key="category.value"
        @click="activeCategory = category.value"
        :class="['category-btn', { active: activeCategory === category.value }]"
      >
        {{ category.label }}
      </button>
    </div>

    <!-- 成就列表 -->
    <div class="achievements-grid">
      <div 
        v-for="achievement in filteredAchievements" 
        :key="achievement.id"
        :class="['achievement-card', { earned: achievement.earned }]"
      >
        <div class="achievement-icon">
          <div class="icon-wrapper">
            {{ getAchievementIcon(achievement.achievement_type) }}
          </div>
          <div v-if="achievement.earned" class="earned-badge">✓</div>
        </div>
        <div class="achievement-content">
          <h4 class="achievement-title">{{ achievement.title }}</h4>
          <p class="achievement-description">{{ achievement.description }}</p>
          <div class="achievement-meta">
            <span class="points">+{{ achievement.points }} 点数</span>
            <span v-if="achievement.earned" class="earned-date">
              {{ formatDate(achievement.earned_at) }}
            </span>
            <div v-if="achievement.reward_type" class="reward-info">
              {{ getRewardInfo(achievement)?.icon }} {{ getRewardInfo(achievement)?.label }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredAchievements.length === 0" class="empty-state">
      <div class="empty-icon">🏆</div>
      <p>还没有成就</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useApi } from '@/composables/useApi'

const api = useApi()

// 响应式数据
const achievements = ref([])
const activeCategory = ref('all')

// 成就分类
const categories = [
  { label: '全部', value: 'all' },
  { label: '连续学习', value: 'daily_streak' },
  { label: '里程碑', value: 'milestone' },
  { label: '技能掌握', value: 'skill_mastery' }
]

// 计算属性
const filteredAchievements = computed(() => {
  if (activeCategory.value === 'all') {
    return achievements.value
  }
  return achievements.value.filter(achievement => 
    achievement.achievement_type === activeCategory.value
  )
})

const totalAchievements = computed(() => achievements.value.length)

const totalPoints = computed(() => 
  achievements.value.reduce((sum, achievement) => sum + achievement.points, 0)
)

// 方法
const loadAchievements = async () => {
  try {
    const response = await api.get('/api/v1/learning/achievements')
    if (response && Array.isArray(response)) {
      achievements.value = response
    } else {
      // 如果API不存在或返回格式不正确，使用模拟数据
      achievements.value = getMockAchievements()
    }
  } catch (error) {
    console.error('加载成就失败:', error)
    // 使用模拟数据作为降级方案
    achievements.value = getMockAchievements()
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

const getMockAchievements = () => {
  return [
    {
      id: 1,
      achievement_type: 'daily_streak',
      title: '学习新手',
      description: '连续学习3天',
      points: 50,
      earned: true,
      earned_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
      reward_type: 'experience',
      reward_value: 100
    },
    {
      id: 2,
      achievement_type: 'daily_streak',
      title: '学习达人',
      description: '连续学习7天',
      points: 100,
      earned: false,
      reward_type: 'badge',
      reward_value: 'gold_streak'
    },
    {
      id: 3,
      achievement_type: 'daily_streak',
      title: '学习大师',
      description: '连续学习30天',
      points: 500,
      earned: false,
      reward_type: 'title',
      reward_value: '学习大师'
    },
    {
      id: 4,
      achievement_type: 'milestone',
      title: '第一个任务',
      description: '完成第一个学习任务',
      points: 25,
      earned: true,
      earned_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
      reward_type: 'experience',
      reward_value: 50
    },
    {
      id: 5,
      achievement_type: 'milestone',
      title: '任务达人',
      description: '完成10个学习任务',
      points: 150,
      earned: false,
      reward_type: 'badge',
      reward_value: 'task_master'
    },
    {
      id: 6,
      achievement_type: 'milestone',
      title: '计划完成者',
      description: '完成一个完整的学习计划',
      points: 300,
      earned: false,
      reward_type: 'title',
      reward_value: '计划完成者'
    },
    {
      id: 7,
      achievement_type: 'skill_mastery',
      title: '技能入门',
      description: '掌握一个技能的基础知识',
      points: 200,
      earned: true,
      earned_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
      reward_type: 'experience',
      reward_value: 200
    },
    {
      id: 8,
      achievement_type: 'skill_mastery',
      title: '技能专家',
      description: '达到高级技能水平',
      points: 1000,
      earned: false,
      reward_type: 'title',
      reward_value: '技能专家'
    },
    {
      id: 9,
      achievement_type: 'accuracy',
      title: '精准射手',
      description: '连续10题全部正确',
      points: 75,
      earned: false,
      reward_type: 'badge',
      reward_value: 'accuracy_master'
    },
    {
      id: 10,
      achievement_type: 'speed',
      title: '速度之王',
      description: '在5分钟内完成10道题目',
      points: 120,
      earned: false,
      reward_type: 'badge',
      reward_value: 'speed_king'
    }
  ]
}

const getAchievementIcon = (type) => {
  const iconMap = {
    'daily_streak': '🔥',
    'milestone': '🎯',
    'skill_mastery': '💎',
    'accuracy': '🎯',
    'speed': '⚡'
  }
  return iconMap[type] || '🏆'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 成就解锁检查
const checkAchievementUnlock = async () => {
  try {
    // 获取用户学习数据
    const statsResponse = await api.get('/api/v1/learning/statistics')
    if (statsResponse) {
      const stats = statsResponse
      
      // 检查各种成就条件
      const newAchievements = []
      
      // 检查连续学习成就
      if (stats.current_streak >= 3 && !hasAchievement('daily_streak', '学习新手')) {
        newAchievements.push(await unlockAchievement('daily_streak', '学习新手'))
      }
      if (stats.current_streak >= 7 && !hasAchievement('daily_streak', '学习达人')) {
        newAchievements.push(await unlockAchievement('daily_streak', '学习达人'))
      }
      
      // 检查任务完成成就
      if (stats.total_tasks_completed >= 1 && !hasAchievement('milestone', '第一个任务')) {
        newAchievements.push(await unlockAchievement('milestone', '第一个任务'))
      }
      if (stats.total_tasks_completed >= 10 && !hasAchievement('milestone', '任务达人')) {
        newAchievements.push(await unlockAchievement('milestone', '任务达人'))
      }
      
      // 检查正确率成就
      if (stats.accuracy_rate >= 90 && !hasAchievement('accuracy', '精准射手')) {
        newAchievements.push(await unlockAchievement('accuracy', '精准射手'))
      }
      
      // 显示新解锁的成就
      if (newAchievements.length > 0) {
        showAchievementUnlock(newAchievements)
      }
    }
  } catch (error) {
    console.error('检查成就解锁失败:', error)
  }
}

const hasAchievement = (type, title) => {
  return achievements.value.some(achievement => 
    achievement.achievement_type === type && 
    achievement.title === title && 
    achievement.earned
  )
}

const unlockAchievement = async (type, title) => {
  try {
    // 创建成就记录
    const achievementData = {
      achievement_type: type,
      title: title,
      earned: true,
      earned_at: new Date().toISOString()
    }
    
    const response = await api.post('/api/v1/learning/achievements', achievementData)
    
    // 更新本地成就列表
    const existingIndex = achievements.value.findIndex(a => 
      a.achievement_type === type && a.title === title
    )
    
    if (existingIndex >= 0) {
      achievements.value[existingIndex] = response
    } else {
      achievements.value.push(response)
    }
    
    return response
  } catch (error) {
    console.error('解锁成就失败:', error)
    return null
  }
}

const showAchievementUnlock = (newAchievements) => {
  // 创建成就解锁通知
  newAchievements.forEach(achievement => {
    if (achievement) {
      const notification = document.createElement('div')
      notification.className = 'achievement-notification'
      notification.innerHTML = `
        <div class="achievement-unlock">
          <div class="unlock-icon">🏆</div>
          <div class="unlock-content">
            <h4>🎉 解锁新成就！</h4>
            <p class="achievement-title">${achievement.title}</p>
            <p class="achievement-desc">${achievement.description}</p>
            <p class="achievement-reward">+${achievement.points} 点数</p>
          </div>
          <button onclick="this.parentElement.parentElement.remove()" class="close-btn">×</button>
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
  })
}

// 获取奖励信息
const getRewardInfo = (achievement) => {
  if (!achievement.reward_type) return null
  
  const rewardInfo = {
    experience: { icon: '⭐', label: '经验值' },
    badge: { icon: '🏅', label: '徽章' },
    title: { icon: '👑', label: '称号' }
  }
  
  return rewardInfo[achievement.reward_type] || null
}

// 生命周期
onMounted(() => {
  loadAchievements()
  
  // 检查成就解锁
  setTimeout(() => {
    checkAchievementUnlock()
  }, 2000)
})
</script>

<style scoped>
.achievement-system {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.achievement-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.achievement-header h3 {
  color: #2c3e50;
  margin: 0;
}

.achievement-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: bold;
  color: #007bff;
}

.stat-label {
  font-size: 0.8rem;
  color: #6c757d;
}

.achievement-categories {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.category-btn {
  padding: 8px 16px;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.category-btn:hover {
  border-color: #007bff;
  color: #007bff;
}

.category-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.achievement-card {
  display: flex;
  padding: 20px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  transition: all 0.3s;
  position: relative;
  background: #f8f9fa;
}

.achievement-card:hover {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.1);
}

.achievement-card.earned {
  border-color: #28a745;
  background: #f8fff9;
}

.achievement-icon {
  position: relative;
  margin-right: 15px;
}

.icon-wrapper {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #e9ecef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  transition: all 0.3s;
}

.achievement-card.earned .icon-wrapper {
  background: #28a745;
  color: white;
}

.earned-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  width: 20px;
  height: 20px;
  background: #28a745;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.achievement-content {
  flex: 1;
}

.achievement-title {
  color: #2c3e50;
  margin: 0 0 8px 0;
  font-size: 1.1rem;
}

.achievement-description {
  color: #6c757d;
  margin: 0 0 12px 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.achievement-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
}

.points {
  color: #007bff;
  font-weight: 600;
}

.earned-date {
  color: #28a745;
}

.reward-info {
  color: #007bff;
  font-weight: 600;
  margin-left: 10px;
}

/* 成就解锁通知样式 */
.achievement-notification {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1002;
  animation: slideInAchievement 0.5s ease;
}

.achievement-unlock {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 15px;
  max-width: 350px;
}

.unlock-icon {
  font-size: 32px;
  animation: bounce 1s infinite;
}

.unlock-content h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
}

.achievement-title {
  margin: 0 0 5px 0;
  font-weight: bold;
  font-size: 14px;
}

.achievement-desc {
  margin: 0 0 8px 0;
  font-size: 12px;
  opacity: 0.9;
}

.achievement-reward {
  margin: 0;
  font-weight: bold;
  color: #ffd700;
  font-size: 14px;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.close-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

@keyframes slideInAchievement {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
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
  margin: 0;
}

@media (max-width: 768px) {
  .achievement-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .achievement-stats {
    justify-content: center;
  }
  
  .achievements-grid {
    grid-template-columns: 1fr;
  }
  
  .achievement-card {
    flex-direction: column;
    text-align: center;
  }
  
  .achievement-icon {
    margin-right: 0;
    margin-bottom: 15px;
  }
}
</style> 