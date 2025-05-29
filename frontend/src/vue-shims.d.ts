declare module "vue-router" {
  import type { Component } from "vue";

  interface RouteMeta {
    requiresAuth?: boolean;
    guestOnly?: boolean;
  }

  interface RouteRecordRaw {
    path: string;
    name?: string;
    component?: Component;
    meta?: RouteMeta;
  }

  interface RouterOptions {
    history?: any;
    routes: RouteRecordRaw[];
  }

  interface Router {
    beforeEach(guard: (to: any, from: any, next: any) => void): void;
    push(to: string): void;
    push(to: { name: string }): void;
  }

  export function createRouter(options: RouterOptions): Router;
  export function createWebHistory(base?: string): any;
  export function createWebHashHistory(base?: string): any;
  export function createMemoryHistory(base?: string): any;
  export function useRouter(): Router;
}
