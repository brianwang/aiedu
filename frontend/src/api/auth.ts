import axios from "axios";
import type { AxiosResponse } from "axios";

const API_URL = import.meta.env.VITE_API_URL || "/";

interface LoginResponse {
  access_token: string;
  token_type: string;
}

export const login = async (
  username: string,
  password: string
): Promise<string> => {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const response: AxiosResponse<LoginResponse> = await axios.post(
    `/api/token`,
    formData,
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );

  return response.data.access_token;
};

export const logout = async (): Promise<void> => {
  // Add logout logic if needed
};

export const refreshToken = async (): Promise<string> => {
  // Add token refresh logic if needed
  return "";
};
