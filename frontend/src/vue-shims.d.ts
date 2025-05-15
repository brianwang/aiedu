declare module "*.vue" {
  import { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

interface ImportMeta {
  env: {
    VITE_API_URL?: string;
    // 其他环境变量...
  };
}
