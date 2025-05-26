import axios from "axios";
import type { AxiosResponse } from "axios";

interface Question {
  id: number;
  question_type: string;
  content: string;
  options?: string[];
  answer: string;
  explanation?: string;
  difficulty: number;
  category_id?: number;
}

interface QuestionCategory {
  id: number;
  name: string;
  parent_id?: number;
}

interface ExamPaper {
  id: number;
  title: string;
  description?: string;
  total_score: number;
  time_limit?: number;
}

export const createQuestion = async (
  question: Omit<Question, "id">
): Promise<AxiosResponse<Question>> => {
  return axios.post("/api/questions", question);
};

export const getQuestion = async (
  questionId: number
): Promise<AxiosResponse<Question>> => {
  return axios.get(`/api/questions/${questionId}`);
};

export const updateQuestion = async (
  questionId: number,
  question: Partial<Question>
): Promise<AxiosResponse<Question>> => {
  return axios.put(`/api/questions/${questionId}`, question);
};

export const deleteQuestion = async (
  questionId: number
): Promise<AxiosResponse> => {
  return axios.delete(`/api/questions/${questionId}`);
};

export const getQuestionsByCategory = async (
  categoryId?: number,
  skip = 0,
  limit = 100
): Promise<AxiosResponse<Question[]>> => {
  const url = categoryId
    ? `/api/questions/category/${categoryId}`
    : "/api/questions";
  return axios.get(url, {
    params: { skip, limit },
  });
};

export const getCategories = async (): Promise<
  AxiosResponse<QuestionCategory[]>
> => {
  return axios.get("/api/questions/categories");
};

export const createCategory = async (
  category: Omit<QuestionCategory, "id">
): Promise<AxiosResponse<QuestionCategory>> => {
  return axios.post("/api/questions/categories", category);
};

export const createExamPaper = async (
  exam: Omit<ExamPaper, "id">
): Promise<AxiosResponse<ExamPaper>> => {
  return axios.post("/api/questions/exams", exam);
};

export const addQuestionToExam = async (
  examId: number,
  questionId: number,
  score = 10,
  sequence?: number
): Promise<AxiosResponse> => {
  return axios.post(`/api/questions/exams/${examId}/questions`, {
    questionId,
    score,
    sequence,
  });
};
