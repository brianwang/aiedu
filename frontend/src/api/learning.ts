import { useApi } from '@/composables/useApi'

const api = useApi()

// 学习计划相关API
export const learningApi = {
  // 获取用户画像
  getProfile: () => api.get('/api/v1/learning/profile'),
  
  // 创建用户画像
  createProfile: (data: any) => api.post('/api/v1/learning/profile', data),
  
  // 更新用户画像
  updateProfile: (data: any) => api.put('/api/v1/learning/profile', data),
  
  // 获取学习目标
  getGoals: () => api.get('/api/v1/learning/goals'),
  
  // 创建学习目标
  createGoal: (data: any) => api.post('/api/v1/learning/goals', data),
  
  // 更新学习目标
  updateGoal: (id: number, data: any) => api.put(`/api/v1/learning/goals/${id}`, data),
  
  // 删除学习目标
  deleteGoal: (id: number) => api.del(`/api/v1/learning/goals/${id}`),
  
  // 获取学习计划
  getPlans: () => api.get('/api/v1/learning/plans'),
  
  // 获取单个学习计划
  getPlan: (id: number) => api.get(`/api/v1/learning/plans/${id}`),
  
  // 生成学习计划
  generatePlan: (data: any) => api.post('/api/v1/learning/generate-plan', data),
  
  // 更新学习计划
  updatePlan: (id: number, data: any) => api.put(`/api/v1/learning/plans/${id}`, data),
  
  // 删除学习计划
  deletePlan: (id: number) => api.del(`/api/v1/learning/plans/${id}`),
  
  // 获取计划任务
  getPlanTasks: (planId: number) => api.get(`/api/v1/learning/plans/${planId}/tasks`),
  
  // 创建任务
  createTask: (data: any) => api.post('/api/v1/learning/tasks', data),
  
  // 更新任务状态
  updateTaskStatus: (taskId: number, status: string) => 
    api.put(`/api/v1/learning/tasks/${taskId}/status`, { status }),
  
  // 完成任务
  completeTask: (taskId: number) => api.put(`/api/v1/learning/tasks/${taskId}/complete`, {}),
  
  // 获取学习统计
  getStatistics: () => api.get('/api/v1/learning/statistics'),
  
  // 获取成就
  getAchievements: () => api.get('/api/v1/learning/achievements'),
  
  // 获取用户成就
  getUserAchievements: () => api.get('/api/v1/learning/user-achievements'),
  
  // 解锁成就
  unlockAchievement: (achievementId: number) => 
    api.post(`/api/v1/learning/achievements/${achievementId}/unlock`, {}),
  
  // 获取学习日历
  getCalendar: (year: number, month: number) => 
    api.get(`/api/v1/learning/calendar/${year}/${month}`),
  
  // 获取今日任务
  getTodayTasks: () => api.get('/api/v1/learning/today-tasks'),
  
  // 记录学习时间
  recordStudyTime: (data: any) => api.post('/api/v1/learning/study-time', data),
  
  // 获取学习报告
  getStudyReport: (period: string) => api.get(`/api/v1/learning/report/${period}`)
}

export default learningApi 