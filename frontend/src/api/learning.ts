import { useApi } from '@/composables/useApi'

const api = useApi()

// 学习计划相关API
export const learningApi = {
  // 获取用户画像
  getProfile: () => api.get('/learning/profile'),
  
  // 创建用户画像
  createProfile: (data: any) => api.post('/learning/profile', data),
  
  // 更新用户画像
  updateProfile: (data: any) => api.put('/learning/profile', data),
  
  // 获取学习目标
  getGoals: () => api.get('/learning/goals'),
  
  // 创建学习目标
  createGoal: (data: any) => api.post('/learning/goals', data),
  
  // 更新学习目标
  updateGoal: (id: number, data: any) => api.put(`/learning/goals/${id}`, data),
  
  // 删除学习目标
  deleteGoal: (id: number) => api.del(`/learning/goals/${id}`),
  
  // 获取学习计划
  getPlans: () => api.get('/learning/plans'),
  
  // 获取单个学习计划
  getPlan: (id: number) => api.get(`/learning/plans/${id}`),
  
  // 生成学习计划
  generatePlan: (data: any) => api.post('/learning/generate-plan', data),
  
  // 更新学习计划
  updatePlan: (id: number, data: any) => api.put(`/learning/plans/${id}`, data),
  
  // 删除学习计划
  deletePlan: (id: number) => api.del(`/learning/plans/${id}`),
  
  // 获取计划任务
  getPlanTasks: (planId: number) => api.get(`/learning/plans/${planId}/tasks`),
  
  // 创建任务
  createTask: (data: any) => api.post('/learning/tasks', data),
  
  // 更新任务状态
  updateTaskStatus: (taskId: number, status: string) => 
    api.put(`/learning/tasks/${taskId}/status`, { status }),
  
  // 完成任务
  completeTask: (taskId: number) => api.put(`/learning/tasks/${taskId}/complete`, {}),
  
  // 获取学习统计
  getStatistics: () => api.get('/learning/statistics'),
  
  // 获取成就
  getAchievements: () => api.get('/learning/achievements'),
  
  // 获取用户成就
  getUserAchievements: () => api.get('/learning/user-achievements'),
  
  // 解锁成就
  unlockAchievement: (achievementId: number) => 
    api.post(`/learning/achievements/${achievementId}/unlock`, {}),
  
  // 获取学习日历
  getCalendar: (year: number, month: number) => 
    api.get(`/learning/calendar/${year}/${month}`),
  
  // 获取今日任务
  getTodayTasks: () => api.get('/learning/today-tasks'),
  
  // 记录学习时间
  recordStudyTime: (data: any) => api.post('/learning/study-time', data),
  
  // 获取学习报告
  getStudyReport: (period: string) => api.get(`/learning/report/${period}`)
}

export default learningApi 