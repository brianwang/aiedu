<script setup lang="ts">
import { NForm, NFormItem, NInput, NButton, NTabs, NTabPane } from "naive-ui";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const activeTab = ref("login");
const loginForm = ref({
  username: "",
  password: "",
});
const registerForm = ref({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const handleLogin = () => {
  // 登录逻辑
  router.push("/");
};

const handleRegister = () => {
  // 注册逻辑
  activeTab.value = "login";
};
</script>

<template>
  <div class="auth">
    <NTabs v-model:value="activeTab" type="line">
      <NTabPane name="login" tab="登录">
        <NForm>
          <NFormItem label="用户名">
            <NInput
              v-model:value="loginForm.username"
              placeholder="请输入用户名"
            />
          </NFormItem>
          <NFormItem label="密码">
            <NInput
              v-model:value="loginForm.password"
              type="password"
              placeholder="请输入密码"
            />
          </NFormItem>
          <NButton type="primary" @click="handleLogin">登录</NButton>
        </NForm>
      </NTabPane>
      <NTabPane name="register" tab="注册">
        <NForm>
          <NFormItem label="用户名">
            <NInput
              v-model:value="registerForm.username"
              placeholder="请输入用户名"
            />
          </NFormItem>
          <NFormItem label="邮箱">
            <NInput
              v-model:value="registerForm.email"
              placeholder="请输入邮箱"
            />
          </NFormItem>
          <NFormItem label="密码">
            <NInput
              v-model:value="registerForm.password"
              type="password"
              placeholder="请输入密码"
            />
          </NFormItem>
          <NFormItem label="确认密码">
            <NInput
              v-model:value="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
            />
          </NFormItem>
          <NButton type="primary" @click="handleRegister">注册</NButton>
        </NForm>
      </NTabPane>
    </NTabs>
  </div>
</template>

<style scoped>
.auth {
  max-width: 500px;
  margin: 2rem auto;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
