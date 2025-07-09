<script setup lang="ts">
import { ref, onMounted } from "vue";

const stats = ref({
  totalQuestions: 1250,
  completedExams: 15,
  studyHours: 48,
  accuracy: 85,
});

const recentActivity = ref([
  {
    id: 1,
    type: "exam",
    title: "数学基础测试",
    score: 88,
    date: "2024-01-15",
    status: "completed",
  },
  {
    id: 2,
    type: "practice",
    title: "英语语法练习",
    score: 92,
    date: "2024-01-14",
    status: "completed",
  },
  {
    id: 3,
    type: "exam",
    title: "物理力学测试",
    score: null,
    date: "2024-01-16",
    status: "pending",
  },
]);

const quickActions = [
  {
    title: "开始答题",
    desc: "从题库中选择练习",
    icon: "practice",
    route: "/question-bank",
    color: "primary",
  },
  {
    title: "学习计划",
    desc: "个性化学习计划",
    icon: "plan",
    route: "/member-center",
    color: "success",
  },
  {
    title: "AI学习",
    desc: "智能学习助手",
    icon: "ai",
    route: "/ai",
    color: "secondary",
  },
  {
    title: "模拟考试",
    desc: "参加模拟考试测试",
    icon: "exam",
    route: "/exam",
    color: "warning",
  },
];

const featuredSubjects = [
  {
    name: "数学",
    questions: 320,
    icon: "📊",
    difficulty: "medium",
    progress: 65,
  },
  {
    name: "英语",
    questions: 280,
    icon: "🔤",
    difficulty: "easy",
    progress: 78,
  },
  {
    name: "物理",
    questions: 245,
    icon: "⚛️",
    difficulty: "hard",
    progress: 42,
  },
  {
    name: "化学",
    questions: 195,
    icon: "🧪",
    difficulty: "medium",
    progress: 58,
  },
  {
    name: "生物",
    questions: 210,
    icon: "🧬",
    difficulty: "easy",
    progress: 73,
  },
];

onMounted(() => {
  // 这里可以添加获取用户数据的API调用
});
</script>

<template>
  <div class="home-dashboard">
    <!-- 欢迎横幅 -->
    <section class="welcome-banner">
      <div class="welcome-content">
        <h1 class="welcome-title">
          <span class="greeting">欢迎回来！</span>
          <span class="subtitle">继续你的学习之旅</span>
        </h1>
        <p class="welcome-desc">通过智能化的学习平台，提升你的知识水平</p>
      </div>
      <div class="welcome-visual">
        <div class="floating-elements">
          <div class="element element-1">📚</div>
          <div class="element element-2">✨</div>
          <div class="element element-3">🎯</div>
        </div>
      </div>
    </section>

    <!-- 统计卡片 -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon primary">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"
              />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">
              {{ stats.totalQuestions.toLocaleString() }}
            </div>
            <div class="stat-label">练习题目</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon secondary">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"
              />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.completedExams }}</div>
            <div class="stat-label">完成考试</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon success">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"
              />
              <path d="M12.5 7H11v6l5.25 3.15.75-1.23-4.5-2.67z" />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.studyHours }}h</div>
            <div class="stat-label">学习时长</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon warning">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
              />
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.accuracy }}%</div>
            <div class="stat-label">正确率</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 快速操作 -->
    <section class="quick-actions-section">
      <h2 class="section-title">快速开始</h2>
      <div class="quick-actions-grid">
        <router-link
          v-for="action in quickActions"
          :key="action.title"
          :to="action.route"
          class="quick-action-card"
          :class="action.color"
        >
          <div class="action-icon">
            <svg
              v-if="action.icon === 'practice'"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"
              />
            </svg>
            <svg
              v-else-if="action.icon === 'exam'"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"
              />
            </svg>
            <svg
              v-else-if="action.icon === 'progress'"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"
              />
            </svg>
            <svg
              v-else-if="action.icon === 'plan'"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"
              />
            </svg>
            <svg
              v-else-if="action.icon === 'ai'"
              viewBox="0 0 24 24"
              fill="currentColor"
            >
              <path
                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"
              />
            </svg>
          </div>
          <div class="action-content">
            <h3 class="action-title">{{ action.title }}</h3>
            <p class="action-desc">{{ action.desc }}</p>
          </div>
          <div class="action-arrow">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"
              />
            </svg>
          </div>
        </router-link>
      </div>
    </section>

    <div class="main-content-grid">
      <!-- 学科概览 -->
      <section class="subjects-section">
        <h2 class="section-title">学科进度</h2>
        <div class="subjects-list">
          <div
            v-for="subject in featuredSubjects"
            :key="subject.name"
            class="subject-card"
          >
            <div class="subject-header">
              <div class="subject-icon">{{ subject.icon }}</div>
              <div class="subject-info">
                <h3 class="subject-name">{{ subject.name }}</h3>
                <p class="subject-questions">{{ subject.questions }} 道题目</p>
              </div>
              <div class="subject-difficulty" :class="subject.difficulty">
                {{
                  subject.difficulty === "easy"
                    ? "简单"
                    : subject.difficulty === "medium"
                    ? "中等"
                    : "困难"
                }}
              </div>
            </div>
            <div class="subject-progress">
              <div class="progress-bar">
                <div
                  class="progress-fill"
                  :style="{ width: `${subject.progress}%` }"
                ></div>
              </div>
              <span class="progress-text">{{ subject.progress }}%</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 最近活动 -->
      <section class="activity-section">
        <h2 class="section-title">最近活动</h2>
        <div class="activity-list">
          <div
            v-for="activity in recentActivity"
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-icon" :class="activity.type">
              <svg
                v-if="activity.type === 'exam'"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path
                  d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6z"
                />
              </svg>
              <svg v-else viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"
                />
              </svg>
            </div>
            <div class="activity-content">
              <h4 class="activity-title">{{ activity.title }}</h4>
              <p class="activity-date">{{ activity.date }}</p>
            </div>
            <div class="activity-result">
              <span v-if="activity.status === 'completed'" class="score"
                >{{ activity.score }}分</span
              >
              <span v-else class="status pending">待完成</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.home-dashboard {
  min-height: 100vh;
  padding-bottom: var(--spacing-xxl);
}

/* 欢迎横幅 */
.welcome-banner {
  background: var(--gradient-primary);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xxl);
  margin-bottom: var(--spacing-xxl);
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: white;
  position: relative;
  overflow: hidden;
}

.welcome-content {
  flex: 1;
  z-index: 2;
}

.welcome-title {
  margin-bottom: var(--spacing-lg);
}

.greeting {
  display: block;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
}

.subtitle {
  display: block;
  font-size: 1.25rem;
  font-weight: 400;
  opacity: 0.9;
}

.welcome-desc {
  font-size: 1.1rem;
  opacity: 0.8;
  margin: 0;
}

.welcome-visual {
  position: relative;
  width: 200px;
  height: 150px;
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
}

.element {
  position: absolute;
  font-size: 2rem;
  animation: float 3s ease-in-out infinite;
}

.element-1 {
  top: 20%;
  left: 20%;
  animation-delay: 0s;
}

.element-2 {
  top: 50%;
  right: 20%;
  animation-delay: 1s;
}

.element-3 {
  bottom: 20%;
  left: 50%;
  animation-delay: 2s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 统计卡片 */
.stats-section {
  margin-bottom: var(--spacing-xxl);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
}

.stat-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  display: flex;
  align-items: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-lg);
}

.stat-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.stat-icon.primary {
  background: var(--gradient-primary);
}
.stat-icon.secondary {
  background: var(--gradient-secondary);
}
.stat-icon.success {
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
}
.stat-icon.warning {
  background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: var(--spacing-xs);
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* 快速操作 */
.quick-actions-section {
  margin-bottom: var(--spacing-xxl);
}

.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
}

.quick-action-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.quick-action-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--primary-color);
  transition: all 0.2s ease;
}

.quick-action-card.secondary::before {
  background: var(--secondary-color);
}
.quick-action-card.success::before {
  background: var(--success-color);
}
.quick-action-card.warning::before {
  background: var(--warning-color);
}

.quick-action-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.action-icon {
  width: 50px;
  height: 50px;
  border-radius: var(--radius-lg);
  background: rgba(74, 144, 226, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-lg);
  flex-shrink: 0;
}

.action-icon svg {
  width: 24px;
  height: 24px;
  color: var(--primary-color);
}

.secondary .action-icon {
  background: rgba(243, 156, 18, 0.1);
}

.secondary .action-icon svg {
  color: var(--secondary-color);
}

.success .action-icon {
  background: rgba(39, 174, 96, 0.1);
}

.success .action-icon svg {
  color: var(--success-color);
}

.warning .action-icon {
  background: rgba(241, 196, 15, 0.1);
}

.warning .action-icon svg {
  color: var(--warning-color);
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.action-desc {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0;
}

.action-arrow {
  margin-left: var(--spacing-md);
  color: var(--text-light);
}

.action-arrow svg {
  width: 20px;
  height: 20px;
}

/* 主要内容网格 */
.main-content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: var(--spacing-xxl);
}

/* 学科卡片 */
.subjects-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.subject-card {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.subject-header {
  display: flex;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.subject-icon {
  font-size: 2rem;
  margin-right: var(--spacing-md);
}

.subject-info {
  flex: 1;
}

.subject-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.subject-questions {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0;
}

.subject-difficulty {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 500;
}

.subject-difficulty.easy {
  background: rgba(39, 174, 96, 0.1);
  color: var(--success-color);
}

.subject-difficulty.medium {
  background: rgba(243, 156, 18, 0.1);
  color: var(--secondary-color);
}

.subject-difficulty.hard {
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
}

.subject-progress {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: var(--bg-accent);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  min-width: 40px;
}

/* 活动列表 */
.activity-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.activity-item {
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-md);
  flex-shrink: 0;
}

.activity-icon.exam {
  background: rgba(74, 144, 226, 0.1);
  color: var(--primary-color);
}

.activity-icon.practice {
  background: rgba(243, 156, 18, 0.1);
  color: var(--secondary-color);
}

.activity-icon svg {
  width: 20px;
  height: 20px;
}

.activity-content {
  flex: 1;
}

.activity-title {
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.activity-date {
  color: var(--text-secondary);
  font-size: 0.8rem;
  margin: 0;
}

.activity-result {
  text-align: right;
}

.score {
  font-weight: 600;
  color: var(--success-color);
}

.status.pending {
  color: var(--warning-color);
  font-size: 0.875rem;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .main-content-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
  }
}

@media (max-width: 768px) {
  .welcome-banner {
    flex-direction: column;
    text-align: center;
    padding: var(--spacing-xl);
  }

  .welcome-visual {
    margin-top: var(--spacing-lg);
  }

  .greeting {
    font-size: 2rem;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }

  .quick-actions-grid {
    grid-template-columns: 1fr;
  }

  .quick-action-card {
    padding: var(--spacing-lg);
  }
}
</style>
