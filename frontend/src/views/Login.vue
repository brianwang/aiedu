<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2>用户登录</h2>
      <div class="form-group">
        <label for="username">用户名</label>
        <input v-model="form.username" type="text" id="username" required />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input v-model="form.password" type="password" id="password" required />
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? "登录中..." : "登录" }}
      </button>
      <p v-if="error" class="error-message">{{ error }}</p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { login } from "@/api/auth";

export default defineComponent({
  name: "LoginView",
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    const form = reactive({
      username: "",
      password: "",
    });
    const loading = ref(false);
    const error = ref("");

    const handleLogin = async () => {
      try {
        loading.value = true;
        error.value = "";
        const { data } = await login({
          username: form.username,
          password: form.password,
        });
        authStore.setToken(data.access_token);
        router.push("/test");
      } catch (err) {
        error.value = (err as Error).message || "登录失败";
      } finally {
        loading.value = false;
      }
    };

    return {
      form,
      loading,
      error,
      handleLogin,
    };
  },
});
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.login-form {
  width: 300px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #ccc;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>
