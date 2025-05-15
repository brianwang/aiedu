<template>
  <nav>
    <router-link to="/">首页</router-link>
    <router-link to="/questions">题库管理</router-link>
    <router-link to="/auth" v-if="!isAuthenticated">登录</router-link>
    <button v-else @click="logout">退出</button>
  </nav>
</template>

<script lang="ts">
import { defineComponent, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "NavBar",
  setup() {
    const store = useStore();
    const router = useRouter();

    const isAuthenticated = computed(() => store.state.auth.isAuthenticated);

    const logout = () => {
      store.dispatch("auth/logout");
      router.push("/auth");
    };

    return {
      isAuthenticated,
      logout,
    };
  },
});
</script>

<style scoped>
nav {
  padding: 1rem;
  background: #f0f0f0;
  margin-bottom: 2rem;
}

nav a {
  margin-right: 1rem;
  text-decoration: none;
  color: #333;
}

nav a.router-link-exact-active {
  color: #42b983;
  font-weight: bold;
}

button {
  background: none;
  border: none;
  color: #333;
  cursor: pointer;
  font-size: inherit;
}
</style>
