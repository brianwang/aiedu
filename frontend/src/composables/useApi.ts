import { ref } from "vue";
import axios, { AxiosError } from "axios";
import { useAuthStore } from "@/stores/auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8111",
  withCredentials: true,
});

// 请求拦截器：自动添加认证token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    const token = authStore.token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器：处理401错误
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      authStore.clearToken();
      // 可以在这里添加重定向到登录页的逻辑
    }
    return Promise.reject(error);
  }
);

interface ApiError {
  message: string;
  response?: {
    data?: {
      message?: string;
    };
  };
}

export function useApi() {
  const error = ref<string | null>(null);
  const loading = ref(false);

  const get = async <T>(url: string): Promise<T> => {
    try {
      loading.value = true;
      const response = await api.get<T>(url);
      return response.data;
    } catch (err) {
      const axiosError = err as AxiosError<{ message?: string }>;
      error.value = axiosError.response?.data?.message || axiosError.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const post = async <T>(url: string, data: any): Promise<T> => {
    try {
      loading.value = true;
      const response = await api.post<T>(url, data);
      return response.data;
    } catch (err) {
      const axiosError = err as AxiosError<{ message?: string }>;
      error.value = axiosError.response?.data?.message || axiosError.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const put = async <T>(url: string, data: any): Promise<T> => {
    try {
      loading.value = true;
      const response = await api.put<T>(url, data);
      return response.data;
    } catch (err) {
      const axiosError = err as AxiosError<{ message?: string }>;
      error.value = axiosError.response?.data?.message || axiosError.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const del = async <T>(url: string): Promise<T> => {
    try {
      loading.value = true;
      const response = await api.delete<T>(url);
      return response.data;
    } catch (err) {
      const axiosError = err as AxiosError<{ message?: string }>;
      error.value = axiosError.response?.data?.message || axiosError.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    error,
    loading,
    get,
    post,
    put,
    del,
  };
}
