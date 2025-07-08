import axios from "axios";
import type { AxiosResponse } from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/";

// 题目推荐接口
export interface RecommendedQuestion {
  id: number;
  content: string;
  question_type: string;
  options?: string[];
  difficulty: number;
  category?: string;
}

export interface QuestionRecommendationResponse {
  success: boolean;
  data: RecommendedQuestion[];
  message: string;
}

export const getRecommendedQuestions = async (
  subject?: string,
  count: number = 10
): Promise<AxiosResponse<QuestionRecommendationResponse>> => {
  const params = new URLSearchParams();
  if (subject) params.append("subject", subject);
  params.append("count", count.toString());

  return axios.get(`/api/v1/ai/recommendations?${params.toString()}`, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 学习计划接口
export interface DailyGoal {
  questions: number;
  study_time: number;
  accuracy_target: number;
}

export interface WeeklyGoals {
  total_questions: number;
  total_study_time: number;
  review_wrong_questions: number;
}

export interface StudySchedule {
  daily_study_time: number;
  sessions_per_day: number;
  break_time: number;
}

export interface Recommendations {
  focus_subjects: string[];
  difficulty_adjustment: string;
  study_schedule: StudySchedule;
}

export interface ProgressSummary {
  total_study_time: number;
  total_questions: number;
  accuracy: number;
  wrong_questions_count: number;
}

export interface StudyPlan {
  user_id: number;
  study_level: string;
  daily_goal: DailyGoal;
  weekly_goals: WeeklyGoals;
  recommendations: Recommendations;
  progress_summary: ProgressSummary;
}

export interface StudyPlanResponse {
  success: boolean;
  data: StudyPlan;
  message: string;
}

export const getStudyPlan = async (): Promise<AxiosResponse<StudyPlanResponse>> => {
  return axios.get("/api/v1/ai/study-plan", {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 学习模式分析接口
export interface LearningPattern {
  time_distribution: Record<string, number>;
  subject_preference: Record<string, number>;
  learning_efficiency: number;
  total_study_sessions: number;
  average_session_duration: number;
  message?: string;
}

export interface LearningPatternResponse {
  success: boolean;
  data: LearningPattern;
  message: string;
}

export const getLearningPattern = async (): Promise<AxiosResponse<LearningPatternResponse>> => {
  return axios.get("/api/v1/ai/learning-pattern", {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 难度分析接口
export interface DifficultyAnalysis {
  accuracy: number;
  total_questions: number;
  wrong_questions_count: number;
  suggestion: string;
  recommended_difficulty: string;
}

export interface DifficultyAnalysisResponse {
  success: boolean;
  data: DifficultyAnalysis;
  message: string;
}

export const getDifficultyAnalysis = async (): Promise<AxiosResponse<DifficultyAnalysisResponse>> => {
  return axios.get("/api/v1/ai/difficulty-analysis", {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// AI生成题目接口（教师/管理员）
export interface GenerateQuestionRequest {
  subject: string;
  difficulty: number;
  count: number;
}

export interface GeneratedQuestion {
  content: string;
  question_type: string;
  options: string[];
  answer: string;
  explanation: string;
  difficulty: number;
}

export interface GenerateQuestionsResponse {
  success: boolean;
  data: GeneratedQuestion[];
  message: string;
}

export const generateQuestions = async (
  data: GenerateQuestionRequest
): Promise<AxiosResponse<GenerateQuestionsResponse>> => {
  const params = new URLSearchParams();
  params.append("subject", data.subject);
  params.append("difficulty", data.difficulty.toString());
  params.append("count", data.count.toString());

  return axios.post(`/api/v1/ai/generate-questions?${params.toString()}`, null, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 智能评分接口
export interface SmartGradingRequest {
  question_content: string;
  standard_answer: string;
  student_answer: string;
  question_type: string;
  max_score: number;
}

export interface GradingResult {
  score: number;
  correctness: number;
  logic_completeness: number;
  expression_standard: number;
  creativity: number;
  overall_evaluation: string;
  suggestions: string[];
}

export interface SmartGradingResponse {
  success: boolean;
  data: GradingResult;
  message: string;
}

export const smartGrading = async (
  data: SmartGradingRequest
): Promise<AxiosResponse<SmartGradingResponse>> => {
  return axios.post("/api/v1/ai/smart-grading", data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 学习能力评估接口
export interface AbilityAssessmentRequest {
  study_time: number;
  questions_completed: number;
  accuracy: number;
  subjects: string[];
  wrong_questions_distribution: Record<string, number>;
}

export interface AbilityAssessment {
  knowledge_mastery: number;
  problem_solving: number;
  concentration: number;
  knowledge_transfer: number;
  learning_efficiency: number;
  overall_level: string;
  improvement_suggestions: string[];
}

export interface AbilityAssessmentResponse {
  success: boolean;
  data: AbilityAssessment;
  message: string;
}

export const assessLearningAbility = async (
  data: AbilityAssessmentRequest
): Promise<AxiosResponse<AbilityAssessmentResponse>> => {
  return axios.post("/api/v1/ai/ability-assessment", data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 学习风格分析接口
export interface LearningStyleRequest {
  time_distribution: Record<string, number>;
  question_type_preference: Record<string, number>;
  learning_mode: string;
  review_frequency: number;
  wrong_question_handling: string;
}

export interface LearningStyle {
  style_type: string;
  characteristics: string[];
  learning_suggestions: string[];
  study_methods: string[];
}

export interface LearningStyleResponse {
  success: boolean;
  data: LearningStyle;
  message: string;
}

export const analyzeLearningStyle = async (
  data: LearningStyleRequest
): Promise<AxiosResponse<LearningStyleResponse>> => {
  return axios.post("/api/v1/ai/learning-style", data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 学习动机激励接口
export interface MotivationRequest {
  learning_status: string;
  learning_difficulties: string[];
  learning_goals: string[];
  learning_achievements: string[];
  personal_characteristics: string[];
}

export interface MotivationPlan {
  achievement_recognition: string[];
  goal_setting: string[];
  challenge_incentives: string[];
  emotional_support: string[];
  encouragement_message: string;
}

export interface MotivationResponse {
  success: boolean;
  data: MotivationPlan;
  message: string;
}

export const getMotivationPlan = async (
  data: MotivationRequest
): Promise<AxiosResponse<MotivationResponse>> => {
  return axios.post("/api/v1/ai/motivation", data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

// 智能组卷
export const generateExam = async (formData: FormData) => {
  return await axios.post('/ai/generate-exam', formData)
}

// 题目推荐
export const recommendQuestions = async (params: { subject?: string; count: number }) => {
  return await axios.get('/ai/recommend-questions', { params })
}

// 创建学习计划
export const createStudyPlan = async (data: { subject: string; goal: string; duration: number }) => {
  return await axios.post('/ai/create-study-plan', data)
}

// 分析学习模式
export const analyzeLearningPattern = async () => {
  return await axios.get('/ai/analyze-learning-pattern')
}

// 学习分析报告
export const generateLearningReport = async () => {
  return await axios.get('/ai/learning-report')
}

// 错题分析讲解
export const analyzeWrongQuestion = async (formData: FormData) => {
  return await axios.post('/ai/analyze-wrong-question', formData)
}

// 学习激励
export const generateLearningMotivation = async () => {
  return await axios.get('/ai/learning-motivation')
}

// 学习风格识别
export const identifyLearningStyle = async () => {
  return await axios.get('/ai/learning-style')
}

// 导出所有AI API方法
export const aiApi = {
  generateExam,
  recommendQuestions,
  createStudyPlan,
  analyzeLearningPattern,
  generateLearningReport,
  analyzeWrongQuestion,
  generateLearningMotivation,
  identifyLearningStyle
} 