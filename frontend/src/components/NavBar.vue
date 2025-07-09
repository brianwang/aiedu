<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <span class="brand-icon">🎓</span>
          <span class="brand-text">AI智能教育平台</span>
        </router-link>
      </div>

      <div class="nav-menu" :class="{ active: isMenuOpen }">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/question-bank" class="nav-link">题库</router-link>
        <router-link to="/exam" class="nav-link">考试</router-link>
        <router-link to="/ai" class="nav-link">AI学习</router-link>
        <router-link to="/teachers" class="nav-link">教师</router-link>
        <router-link to="/courses" class="nav-link">课程</router-link>
        <router-link to="/community" class="nav-link">社区</router-link>
      </div>

      <div class="nav-auth">
        <template v-if="isAuthenticated">
          <div class="user-menu" @click="toggleUserMenu">
            <span class="user-avatar">{{ userInitials }}</span>
            <span class="user-name">{{ userName }}</span>
            <span class="dropdown-arrow">▼</span>

            <div class="dropdown-menu" v-if="showUserMenu">
              <router-link to="/member-center" class="dropdown-item">
                <span class="icon">👤</span>
                个人中心
              </router-link>
              <router-link
                v-if="isTeacher"
                to="/teacher-dashboard"
                class="dropdown-item"
              >
                <span class="icon">📊</span>
                教师面板
              </router-link>
              <div class="dropdown-divider"></div>
              <button @click="logout" class="dropdown-item logout-btn">
                <span class="icon">🚪</span>
                退出登录
              </button>
            </div>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="auth-btn login-btn">登录</router-link>
          <router-link to="/register" class="auth-btn register-btn"
            >注册</router-link
          >
        </template>
      </div>

      <div class="nav-toggle" @click="toggleMenu">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

// 响应式数据
const isMenuOpen = ref(false);
const showUserMenu = ref(false);

// 计算属性
const isAuthenticated = computed(() => authStore.isAuthenticated);
const userName = computed(() => authStore.user?.username || "用户");
const userInitials = computed(() => {
  const name = authStore.user?.username || "";
  return name.substring(0, 2).toUpperCase();
});
const isTeacher = computed(
  () => authStore.user?.role === "teacher" || authStore.user?.role === "admin"
);

// 方法
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

const logout = async () => {
  try {
    await authStore.logout();
    showUserMenu.value = false;
    router.push("/login");
  } catch (error) {
    console.error("退出登录失败:", error);
  }
};

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  const userMenu = document.querySelector(".user-menu");
  if (userMenu && !userMenu.contains(event.target)) {
    showUserMenu.value = false;
  }
};

// 生命周期
onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  font-weight: bold;
  font-size: 1.5rem;
}

.brand-icon {
  font-size: 2rem;
  margin-right: 0.5rem;
}

.brand-text {
  font-size: 1.2rem;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-auth {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.login-btn {
  color: white;
  border: 2px solid white;
}

.login-btn:hover {
  background: white;
  color: #667eea;
}

.register-btn {
  background: white;
  color: #667eea;
}

.register-btn:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.user-menu {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.user-menu:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  font-size: 0.9rem;
}

.user-name {
  color: white;
  font-weight: 500;
}

.dropdown-arrow {
  color: white;
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.user-menu:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  min-width: 200px;
  padding: 0.5rem 0;
  margin-top: 0.5rem;
  z-index: 1000;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  color: #333;
  text-decoration: none;
  transition: background 0.3s ease;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
}

.dropdown-item:hover {
  background: #f8f9fa;
}

.dropdown-item .icon {
  font-size: 1rem;
}

.dropdown-divider {
  height: 1px;
  background: #e9ecef;
  margin: 0.5rem 0;
}

.logout-btn {
  color: #dc3545;
}

.logout-btn:hover {
  background: #f8d7da;
}

.nav-toggle {
  display: none;
  flex-direction: column;
  cursor: pointer;
  gap: 4px;
}

.nav-toggle span {
  width: 25px;
  height: 3px;
  background: white;
  border-radius: 2px;
  transition: all 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .nav-menu {
    position: fixed;
    top: 100%;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    flex-direction: column;
    padding: 2rem;
    gap: 1rem;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
  }

  .nav-menu.active {
    transform: translateY(0);
    opacity: 1;
    visibility: visible;
  }

  .nav-toggle {
    display: flex;
  }

  .nav-toggle.active span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
  }

  .nav-toggle.active span:nth-child(2) {
    opacity: 0;
  }

  .nav-toggle.active span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -6px);
  }

  .nav-container {
    padding: 0 1rem;
  }

  .brand-text {
    display: none;
  }
}

@media (max-width: 480px) {
  .nav-auth {
    gap: 0.5rem;
  }

  .auth-btn {
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
  }

  .user-name {
    display: none;
  }
}
</style>
