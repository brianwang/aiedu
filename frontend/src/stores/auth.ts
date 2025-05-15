import { defineStore } from "pinia";
import { ref } from "vue";
import { login } from "../api/auth";

export const useAuthStore = defineStore("auth", () => {
  const token = ref<string | null>(null);

  const isAuthenticated = () => !!token.value;

  const setToken = (newToken: string) => {
    token.value = newToken;
    localStorage.setItem("token", newToken);
  };

  const clearToken = () => {
    token.value = null;
    localStorage.removeItem("token");
  };

  const initialize = () => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      token.value = storedToken;
    }
  };

  return {
    token,
    isAuthenticated,
    setToken,
    clearToken,
    initialize,
  };
});
