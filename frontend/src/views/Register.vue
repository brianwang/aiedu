<template>
  <div class="register-container">
    <h1>用户注册</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名</label>
        <input
          v-model="form.username"
          type="text"
          id="username"
          required
          minlength="3"
          maxlength="50"
        />
      </div>

      <div class="form-group">
        <label for="email">邮箱</label>
        <input v-model="form.email" type="email" id="email" required />
      </div>

      <div class="form-group">
        <label for="password">密码</label>
        <input
          v-model="form.password"
          type="password"
          id="password"
          required
          minlength="8"
          maxlength="100"
        />
      </div>

      <div class="form-group">
        <label for="confirmPassword">确认密码</label>
        <input
          v-model="form.confirmPassword"
          type="password"
          id="confirmPassword"
          required
          minlength="8"
          maxlength="100"
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "注册中..." : "注册" }}
      </button>
    </form>

    <p class="login-link">
      已有账号？<router-link to="/login">登录</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { register } from "@/api/auth";
import { useToast } from "vue-toast-notification";

const router = useRouter();
const toast = useToast();

const form = ref({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const loading = ref(false);

const handleSubmit = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    toast.error("两次输入的密码不一致");
    return;
  }

  try {
    loading.value = true;
    await register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      confirm_password: form.value.confirmPassword,
    });

    toast.success("注册成功");
    router.push("/login");
  } catch (error: any) {
    toast.error(error.response?.data?.detail || "注册失败");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.login-link {
  margin-top: 1rem;
  text-align: center;
}
</style>
