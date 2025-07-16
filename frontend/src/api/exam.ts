import axios from "axios";
import type { AxiosResponse } from "axios";
import { useApi } from "@/composables/useApi";

interface ExamResult {
  examId: string;
  studentId: string;
  answers: (string | null)[];
  score: number;
  totalScore: number;
}

export const submitExamResult = async (
  result: ExamResult
): Promise<AxiosResponse> => {
  return axios.post("/api/v1/exam/results", result);
};

export const getExam = async (examId: string): Promise<AxiosResponse> => {
  return axios.get(`/api/v1/exam/${examId}`);
};

export async function generateExam(params: {
  subject: string;
  difficulty: number;
  exam_type?: string;
  question_distribution?: Record<string, number>;
  skill?: string;
  tags?: string[];
}) {
  const api = useApi();
  return api.post("/api/v1/exam/generate", params);
}
