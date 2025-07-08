<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧装饰区域 -->
      <div class="login-visual">
        <div class="visual-content">
          <div class="brand-section">
            <h1 class="brand-title">智学平台</h1>
            <p class="brand-subtitle">开启智能学习新时代</p>
          </div>
          
          <div class="features-list">
            <div class="feature-item">
              <div class="feature-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                </svg>
              </div>
              <div class="feature-content">
                <h3>智能题库</h3>
                <p>海量精选题目，个性化推荐</p>
              </div>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
                </svg>
              </div>
              <div class="feature-content">
                <h3>学习分析</h3>
                <p>数据驱动，精准定位薄弱环节</p>
              </div>
            </div>
            
            <div class="feature-item">
              <div class="feature-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
              </div>
              <div class="feature-content">
                <h3>成长激励</h3>
                <p>成就系统，让学习更有动力</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="login-form-section">
        <div class="form-container">
          <div class="form-header">
            <h2 class="form-title">欢迎回来</h2>
            <p class="form-subtitle">登录您的账户继续学习</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="form-group">
              <label for="username" class="form-label">
                <svg viewBox="0 0 24 24" fill="currentColor" class="label-icon">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
                用户名
              </label>
              <input 
                v-model="form.username" 
                type="text" 
                id="username" 
                class="form-input"
                placeholder="请输入用户名"
                required 
              />
            </div>

            <div class="form-group">
              <label for="password" class="form-label">
                <svg viewBox="0 0 24 24" fill="currentColor" class="label-icon">
                  <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
                </svg>
                密码
              </label>
              <input 
                v-model="form.password" 
                type="password" 
                id="password" 
                class="form-input"
                placeholder="请输入密码"
                required 
              />
            </div>

            <div class="form-options">
              <label class="checkbox-container">
                <input type="checkbox" class="checkbox-input">
                <span class="checkmark"></span>
                <span class="checkbox-text">记住我</span>
              </label>
              <a href="#" class="forgot-password">忘记密码？</a>
            </div>

            <button type="submit" class="login-button btn-primary" :disabled="loading">
              <svg v-if="loading" viewBox="0 0 24 24" fill="currentColor" class="loading-icon">
                <path d="M12 4V2A10 10 0 0 0 2 12h2a8 8 0 0 1 8-8z"/>
              </svg>
              <span>{{ loading ? "登录中..." : "立即登录" }}</span>
            </button>

            <div class="register-link">
              <span class="register-text">还没有账户？</span>
              <button type="button" @click="gotoRegister" class="register-link-btn">
                立即注册
              </button>
            </div>

            <div v-if="error" class="error-message">
              <svg viewBox="0 0 24 24" fill="currentColor" class="error-icon">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
              </svg>
              {{ error }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

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
        
        const result = await authStore.loginUser({
          username: form.username,
          password: form.password,
        });
        
        if (result.success) {
          router.push("/");
        } else {
          error.value = "登录失败，请检查用户名和密码";
        }
      } catch (err) {
        error.value = (err as Error).message || "登录失败，请检查用户名和密码";
      } finally {
        loading.value = false;
      }
    };
    
    const gotoRegister = () => {
      router.push("/register");
    };

    return {
      form,
      loading,
      error,
      handleLogin,
      gotoRegister,
    };
  },
});
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-md);
}

.login-container {
  display: flex;
  max-width: 1200px;
  width: 100%;
  background: var(--bg-primary);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  min-height: 600px;
}

/* 左侧装饰区域 */
.login-visual {
  flex: 1;
  background: var(--gradient-primary);
  padding: var(--spacing-xl) var(--spacing-xxl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  position: relative;
  min-height: 500px;
}

.visual-content {
  max-width: 380px;
  text-align: center;
  transform: translateY(-20px);
}

.brand-section {
  margin-bottom: var(--spacing-xl);
}


.brand-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  background: linear-gradient(45deg, #ffffff, #e3f2fd);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.brand-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.feature-item {
  display: flex;
  align-items: center;
  text-align: left;
  padding: var(--spacing-lg);
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg);
  backdrop-filter: blur(10px);
}

.feature-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--spacing-lg);
  flex-shrink: 0;
}

.feature-icon svg {
  width: 24px;
  height: 24px;
}

.feature-content h3 {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.feature-content p {
  font-size: 0.9rem;
  opacity: 0.8;
  margin: 0;
}

/* 右侧登录表单 */
.login-form-section {
  flex: 1;
  padding: var(--spacing-xxl);
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-container {
  width: 100%;
  max-width: 400px;
}

.form-header {
  text-align: center;
  margin-bottom: var(--spacing-xxl);
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.form-subtitle {
  color: var(--text-secondary);
  margin: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  display: flex;
  align-items: center;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.label-icon {
  width: 18px;
  height: 18px;
  margin-right: var(--spacing-xs);
  color: var(--text-secondary);
}

.form-input {
  padding: var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 1rem;
  transition: all 0.2s ease;
  background: var(--bg-primary);
}

.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
  outline: none;
}

.form-input::placeholder {
  color: var(--text-light);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  font-size: 0.875rem;
  color: var(--text-secondary);
  user-select: none;
}

.checkbox-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  height: 18px;
  width: 18px;
  background-color: var(--bg-primary);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-sm);
  margin-right: var(--spacing-sm);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.checkbox-container:hover .checkmark {
  border-color: var(--primary-color);
}

.checkbox-container .checkbox-input:checked ~ .checkmark {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 4px;
  top: 1px;
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-container .checkbox-input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.forgot-password {
  color: var(--primary-color);
  font-size: 0.875rem;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.login-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 50px;
}

.loading-icon {
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.register-link {
  text-align: center;
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

.register-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin-right: var(--spacing-sm);
}

.register-link-btn {
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s ease;
  padding: 0;
  margin: 0;
  min-height: auto;
}

.register-link-btn:hover {
  color: var(--primary-dark);
}

.error-message {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  background: rgba(231, 76, 60, 0.1);
  color: var(--danger-color);
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  border: 1px solid rgba(231, 76, 60, 0.2);
}

.error-icon {
  width: 16px;
  height: 16px;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .login-container {
    flex-direction: column;
    max-width: 500px;
  }
  
  .login-visual {
    padding: var(--spacing-xl);
  }
  
  .features-list {
    flex-direction: row;
    flex-wrap: wrap;
    gap: var(--spacing-md);
  }
  
  .feature-item {
    flex: 1;
    min-width: 200px;
  }
}

@media (max-width: 768px) {
  .login-page {
    padding: var(--spacing-sm);
  }
  
  .login-container {
    min-height: auto;
  }
  
  .login-visual {
    padding: var(--spacing-lg);
  }
  
  .login-form-section {
    padding: var(--spacing-lg);
  }
  
  .brand-title {
    font-size: 2rem;
  }
  
  .features-list {
    flex-direction: column;
  }
  
  .feature-item {
    flex-direction: column;
    text-align: center;
    padding: var(--spacing-md);
  }
  
  .feature-icon {
    margin-right: 0;
    margin-bottom: var(--spacing-sm);
  }
}
</style>
