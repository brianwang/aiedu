import axios from "axios";
import type { AxiosResponse } from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const login = async (credentials: {
  username: string;
  password: string;
}): Promise<AxiosResponse<{ access_token: string }>> => {
  return axios.post("/api/login", credentials, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

export const logout = async (): Promise<void> => {
  // Add logout logic if needed
};

export const refreshToken = async (): Promise<string> => {
  // Add token refresh logic if needed
  return "";
};

interface RegisterData {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
}

export const register = async (
  data: RegisterData
): Promise<
  AxiosResponse<{ message: string; user_id: number; email: string }>
> => {
  return axios.post("/api/register", data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};
