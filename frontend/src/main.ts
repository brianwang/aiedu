import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import naive from "naive-ui";
import { createPinia } from "pinia";
import { useAuthStore } from "./stores/auth";
import "./style.css";
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
// import pinia from "pinia";
const app = createApp(App);
app.use(router);
const pinia = createPinia();
app.use(pinia);
app.use(naive);
app.use(ElementPlus);

// 初始化认证状态
const authStore = useAuthStore();
authStore.initialize();

app.mount("#app");
