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
    const response = await api.get('/learning/achievements')
    achievements.value = response
  } catch (error) {
    console.error('加载成就失败:', error)
    // 如果API不存在，使用模拟数据
    achievements.value = getMockAchievements()
  }
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
      earned_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 2,
      achievement_type: 'daily_streak',
      title: '学习达人',
      description: '连续学习7天',
      points: 100,
      earned: false
    },
    {
      id: 3,
      achievement_type: 'daily_streak',
      title: '学习大师',
      description: '连续学习30天',
      points: 500,
      earned: false
    },
    {
      id: 4,
      achievement_type: 'milestone',
      title: '第一个任务',
      description: '完成第一个学习任务',
      points: 25,
      earned: true,
      earned_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 5,
      achievement_type: 'milestone',
      title: '任务达人',
      description: '完成10个学习任务',
      points: 150,
      earned: false
    },
    {
      id: 6,
      achievement_type: 'milestone',
      title: '计划完成者',
      description: '完成一个完整的学习计划',
      points: 300,
      earned: false
    },
    {
      id: 7,
      achievement_type: 'skill_mastery',
      title: '技能入门',
      description: '掌握一个技能的基础知识',
      points: 200,
      earned: true,
      earned_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString()
    },
    {
      id: 8,
      achievement_type: 'skill_mastery',
      title: '技能专家',
      description: '达到高级技能水平',
      points: 1000,
      earned: false
    }
  ]
}

const getAchievementIcon = (type) => {
  const iconMap = {
    'daily_streak': '🔥',
    'milestone': '🎯',
    'skill_mastery': '💎'
  }
  return iconMap[type] || '🏆'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadAchievements()
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