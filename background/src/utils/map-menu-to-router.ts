import router from "@/router"

// 把菜单的第一个url返回出去
export let fristMenu = ""

//这个函数是注册动态路由的函数，需要传入注册的菜单数组，和父组件的name
export function mapMenuToRoute(menu: any[], name: string) {
  // 获取所有的路由对象放到数组中
  const routers = []
  const files: Record<string, any> = import.meta.glob("@/router/main/**/*.ts", {
    eager: true
  })
  for (const key in files) {
    routers.push(files[key].default)
  }

  // 根据菜单去匹配对应的路由
  for (const iterator of menu) {
    for (const key of iterator.children) {
      const route = routers.find((item) => key.url === item.path)
      router.addRoute(name, route)
      if (!fristMenu && router) fristMenu = key.url
    }
  }
}

export function mapUrlToMenu(menu: any[], url: string): any {
  for (const iterator of menu) {
    for (const key of iterator.children) {
      if (url === key.url) return { key, iterator }
    }
  }
}
