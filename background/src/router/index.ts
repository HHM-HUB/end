import { TOKEN } from "@/global/constants"
import { fristMenu } from "@/utils/map-menu-to-router"
import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      redirect: "/main"
    },
    {
      path: "/login",
      component: () => import("../views/login/index.vue"),
      meta: {
        title: "登录"
      }
    },
    {
      path: "/main",
      name: "main",
      component: () => import("../views/main/index.vue"),
      meta: {
        title: "后台管理系统-首页"
      }
    },
    {
      path: "/:pathMatch(.*)*",
      component: () => import("../views/not-found/index.vue")
    }
  ]
})

router.beforeEach((to) => {
  const token = localStorage.getItem(TOKEN)
  if (to.path !== "/login" && !token) {
    return "/login"
  }

  if (to.path === "/main") {
    return fristMenu
  }
})

router.afterEach((to) => {
  if (to.path === "/login") {
    document.title = to.meta.title as string
  }
  if (to.path === fristMenu) {
    document.title = to.meta.title as string
  }
})
export default router
