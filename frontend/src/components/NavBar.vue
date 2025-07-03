<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Logo和品牌 -->
      <div class="navbar-brand">
        <router-link to="/" class="brand-link">
          <div class="logo">
            <svg viewBox="0 0 24 24" fill="currentColor" class="logo-icon">
              <path d="M12 2L2 7v10c0 5.55 3.84 9.739 9 11 5.16-1.261 9-5.45 9-11V7l-10-5z"/>
              <path d="M10 17l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
            </svg>
          </div>
          <span class="brand-text">智学平台</span>
        </router-link>
      </div>

      <!-- 导航菜单 -->
      <div class="navbar-menu" :class="{ active: mobileMenuOpen }">
        <div class="nav-links">
          <router-link to="/" class="nav-link" @click="closeMobileMenu">
            <svg viewBox="0 0 24 24" fill="currentColor" class="nav-icon">
              <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
            </svg>
            <span>首页</span>
          </router-link>
          
          <router-link to="/questions" class="nav-link" @click="closeMobileMenu" v-if="isAuthenticated">
            <svg viewBox="0 0 24 24" fill="currentColor" class="nav-icon">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
            </svg>
            <span>题库练习</span>
          </router-link>

          <router-link to="/exams" class="nav-link" @click="closeMobileMenu" v-if="isAuthenticated">
            <svg viewBox="0 0 24 24" fill="currentColor" class="nav-icon">
              <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
            </svg>
            <span>考试中心</span>
          </router-link>
        </div>

        <!-- 用户菜单 -->
        <div class="user-menu">
          <div v-if="isAuthenticated" class="user-profile">
            <button class="profile-button" @click="toggleUserDropdown">
              <div class="avatar">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
              <span class="username">学员</span>
              <svg viewBox="0 0 24 24" fill="currentColor" class="dropdown-icon">
                <path d="M7 10l5 5 5-5z"/>
              </svg>
            </button>
            
            <div class="dropdown-menu" :class="{ show: userDropdownOpen }">
              <a href="#" class="dropdown-item">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
                </svg>
                我的成绩
              </a>
              <a href="#" class="dropdown-item">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                学习进度
              </a>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item logout-btn" @click="logout">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.59L17 17l5-5z"/>
                </svg>
                退出登录
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 移动端菜单按钮 -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu">
        <span class="hamburger"></span>
        <span class="hamburger"></span>
        <span class="hamburger"></span>
      </button>
    </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, computed, ref } from "vue";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "NavBar",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const mobileMenuOpen = ref(false);
    const userDropdownOpen = ref(false);

    const isAuthenticated = computed(() => authStore.isAuthenticated());

    const logout = () => {
      authStore.clearToken();
      router.push("/login");
      userDropdownOpen.value = false;
      mobileMenuOpen.value = false;
    };

    const toggleMobileMenu = () => {
      mobileMenuOpen.value = !mobileMenuOpen.value;
    };

    const closeMobileMenu = () => {
      mobileMenuOpen.value = false;
    };

    const toggleUserDropdown = () => {
      userDropdownOpen.value = !userDropdownOpen.value;
    };

    return {
      isAuthenticated,
      mobileMenuOpen,
      userDropdownOpen,
      logout,
      toggleMobileMenu,
      closeMobileMenu,
      toggleUserDropdown,
    };
  },
});
</script>

<style scoped>
.navbar {
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.navbar-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

/* Logo和品牌 */
.navbar-brand {
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  align-items: center;
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1.25rem;
}

.logo {
  margin-right: var(--spacing-sm);
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--gradient-primary);
  border-radius: var(--radius-md);
  color: white;
}

.logo-icon {
  width: 20px;
  height: 20px;
}

.brand-text {
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 导航菜单 */
.navbar-menu {
  display: flex;
  align-items: center;
  flex: 1;
  justify-content: space-between;
  margin-left: var(--spacing-xxl);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.nav-link {
  display: flex;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-secondary);
  border-radius: var(--radius-md);
  transition: all 0.2s ease;
  font-weight: 500;
}

.nav-link:hover {
  color: var(--primary-color);
  background: rgba(74, 144, 226, 0.1);
}

.nav-link.router-link-active {
  color: var(--primary-color);
  background: rgba(74, 144, 226, 0.1);
}

.nav-icon {
  width: 18px;
  height: 18px;
  margin-right: var(--spacing-xs);
}

/* 用户菜单 */
.user-menu {
  position: relative;
}


.profile-button {
  display: flex;
  align-items: center;
  padding: var(--spacing-sm);
  background: none;
  border: none;
  color: var(--text-primary);
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background 0.2s ease;
}

.profile-button:hover {
  background: var(--bg-accent);
}

.avatar {
  width: 32px;
  height: 32px;
  background: var(--gradient-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: var(--spacing-sm);
}

.avatar svg {
  width: 18px;
  height: 18px;
}

.username {
  margin-right: var(--spacing-xs);
  font-weight: 500;
}

.dropdown-icon {
  width: 16px;
  height: 16px;
  transition: transform 0.2s ease;
}

.profile-button:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* 下拉菜单 */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  min-width: 200px;
  padding: var(--spacing-sm) 0;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  z-index: 1000;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  color: var(--text-primary);
  text-decoration: none;
  transition: background 0.2s ease;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
}

.dropdown-item:hover {
  background: var(--bg-accent);
}

.dropdown-item svg {
  width: 16px;
  height: 16px;
  margin-right: var(--spacing-sm);
  color: var(--text-secondary);
}

.dropdown-divider {
  height: 1px;
  background: var(--border-color);
  margin: var(--spacing-sm) 0;
}

.logout-btn {
  color: var(--danger-color);
}

.logout-btn:hover {
  background: rgba(231, 76, 60, 0.1);
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  flex-direction: column;
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--spacing-xs);
}

.hamburger {
  width: 20px;
  height: 2px;
  background: var(--text-primary);
  margin: 2px 0;
  transition: 0.3s;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: flex;
  }

  .navbar-menu {
    position: fixed;
    top: 70px;
    left: 0;
    right: 0;
    background: var(--bg-primary);
    border-top: 1px solid var(--border-color);
    flex-direction: column;
    padding: var(--spacing-lg);
    transform: translateY(-100vh);
    transition: transform 0.3s ease;
    margin-left: 0;
  }

  .navbar-menu.active {
    transform: translateY(0);
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-lg);
  }

  .nav-link {
    width: 100%;
    justify-content: flex-start;
    padding: var(--spacing-md);
  }

  .user-menu {
    width: 100%;
  }

  .dropdown-menu {
    position: static;
    opacity: 1;
    visibility: visible;
    transform: none;
    box-shadow: none;
    border: none;
    border-top: 1px solid var(--border-color);
    margin-top: var(--spacing-md);
    padding-top: var(--spacing-md);
  }
}
</style>
