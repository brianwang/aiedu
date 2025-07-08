import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { login } from "../api/auth";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(null);
  const user = ref<any>(null);

  // 计算属性
  const isAuthenticated = computed(() => !!token.value);

  // 方法
  const setToken = (newToken: string) => {
    token.value = newToken;
    localStorage.setItem("token", newToken);
  };

  const setUser = (userData: any) => {
    user.value = userData;
    localStorage.setItem("user", JSON.stringify(userData));
  };

  const clearToken = () => {
    token.value = null;
    user.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  const initialize = () => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    
    if (storedToken) {
      token.value = storedToken;
    }
    
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser);
      } catch (error) {
        console.error("Failed to parse stored user data:", error);
        localStorage.removeItem("user");
      }
    }
  };

  const loginUser = async (credentials: { username: string; password: string }) => {
    try {
      const response = await login(credentials);
      const { access_token } = response.data;
      
      setToken(access_token);
      
      // 这里可以添加获取用户信息的API调用
      // const userResponse = await getUserInfo();
      // setUser(userResponse.data);
      
      return { success: true };
    } catch (error) {
      console.error("Login failed:", error);
      return { success: false, error };
    }
  };

  const logoutUser = () => {
    clearToken();
  };

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    setUser,
    clearToken,
    initialize,
    loginUser,
    logoutUser,
  };
});
