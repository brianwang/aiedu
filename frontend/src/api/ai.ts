import { apiClient } from "./index";

export interface QuestionGenerationRequest {
  subject: string;
  difficulty: number;
  count: number;
  question_types?: string[];
}

export interface SmartGradingRequest {
  question_content: string;
  standard_answer: string;
  student_answer: string;
  question_type: string;
  max_score: number;
  student_level?: string;
}

export interface RealTimeQARequest {
  question: string;
  context?: string;
  user_level?: string;
}

export interface TextToSpeechRequest {
  text: string;
  voice?: string;
}

export interface AIStatus {
  ai_available: boolean;
  clients_count: number;
  cache_enabled: boolean;
  cache_size: number;
}

export interface LearningReport {
  total_study_time: number;
  total_questions: number;
  accuracy: number;
  suggestions: string;
}

export interface LearningStyle {
  style_type: string;
  characteristics: string[];
  learning_suggestions: string[];
  study_methods: string[];
}

export interface LearningMotivation {
  encouragement_message: string;
  learning_tips: string[];
}

export interface GradingResult {
  score: number;
  accuracy_score: number;
  logic_score: number;
  expression_score: number;
  creativity_score: number;
  overall_accuracy: number;
  detailed_feedback: {
    strengths: string[];
    weaknesses: string[];
    specific_errors: string[];
    improvement_suggestions: string[];
  };
  learning_insights: {
    knowledge_gaps: string[];
    skill_development: string[];
    next_steps: string[];
  };
  encouragement: string;
  difficulty_adjustment: string;
}

export interface QAResult {
  answer: string;
  explanation: string;
  knowledge_points: string[];
  learning_tips: string[];
  related_topics: string[];
  difficulty_level: string;
}

export interface SpeechToTextResult {
  text: string;
  confidence: number;
  language: string;
  duration?: number;
  error?: string;
}

export interface TextToSpeechResult {
  audio_data: string;
  text: string;
  voice: string;
}

// AI功能API
export const aiApi = {
  // 获取AI服务状态
  getStatus(): Promise<AIStatus> {
    return apiClient.get("/api/v1/ai/ai-status");
  },

  // 生成题目
  generateQuestions(request: QuestionGenerationRequest): Promise<any[]> {
    return apiClient.post("/api/v1/ai/generate-questions", request);
  },

  // 智能评分
  smartGrading(request: SmartGradingRequest): Promise<GradingResult> {
    return apiClient.post("/api/v1/ai/smart-grading", request);
  },

  // 实时问答
  realTimeQA(request: RealTimeQARequest): Promise<QAResult> {
    return apiClient.post("/api/v1/ai/real-time-qa", request);
  },

  // 语音转文字
  speechToText(
    audioFile: File,
    language: string = "zh-CN"
  ): Promise<SpeechToTextResult> {
    const formData = new FormData();
    formData.append("audio_file", audioFile);
    formData.append("language", language);
    return apiClient.post("/api/v1/ai/speech-to-text", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },

  // 文字转语音
  textToSpeech(request: TextToSpeechRequest): Promise<TextToSpeechResult> {
    return apiClient.post("/api/v1/ai/text-to-speech", request);
  },

  // 获取推荐题目
  getRecommendations(subject?: string, count: number = 10): Promise<any[]> {
    const params = new URLSearchParams();
    if (subject) params.append("subject", subject);
    params.append("count", count.toString());
    return apiClient.get(`/api/v1/ai/recommendations?${params.toString()}`);
  },

  // 生成学习报告
  generateLearningReport(): Promise<LearningReport> {
    return apiClient.get("/api/v1/ai/learning-report");
  },

  // 分析学习风格
  analyzeLearningStyle(): Promise<LearningStyle> {
    return apiClient.get("/api/v1/ai/learning-style");
  },

  // 获取学习激励
  getLearningMotivation(): Promise<LearningMotivation> {
    return apiClient.get("/api/v1/ai/learning-motivation");
  },

  // 错题分析
  analyzeWrongQuestion(
    questionContent: string,
    userAnswer: string,
    correctAnswer: string,
    subject: string
  ): Promise<any> {
    return apiClient.post("/api/v1/ai/analyze-wrong-question", {
      question_content: questionContent,
      user_answer: userAnswer,
      correct_answer: correctAnswer,
      subject: subject,
    });
  },
};

export default aiApi;

// 兼容性导出：推荐题目
export function getRecommendedQuestions(subject?: string, count: number = 10) {
  return aiApi.getRecommendations(subject, count);
}
