import axios from "axios";
import type { AxiosResponse } from "axios";

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
