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
  return axios.post("/api/v1/login", credentials, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

export const logout = async (): Promise<void> => {
  try {
    const token = localStorage.getItem("token");
    if (token) {
      await axios.post("/api/v1/logout", {}, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });
    }
  } catch (error) {
    console.error("Logout API call failed:", error);
  } finally {
    // Always clear local storage regardless of API call success
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }
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
  return axios.post("/api/v1/register", data, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};
