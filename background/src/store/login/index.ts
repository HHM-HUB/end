import { defineStore } from "pinia"
import { getMenuInfo, getuserInfo, loginInterface } from "@/service"
import router from "@/router"
import { TOKEN, USER_INFO, USER_MENU } from "@/global/constants"
import { ElMessage } from "element-plus"
import { MYLocalStorage } from "@/utils/storage"
import { mapMenuToRoute } from "@/utils/map-menu-to-router"
import useMainStore from "../main"
interface stateType {
  token: string
  userInfos: any
  menuInfos: any
}
const useLoginStore = defineStore("login", {
  state: (): stateType => ({
    token: "",
    userInfos: {},
    menuInfos: []
  }),
  actions: {
    async getLoginToken(formData: { account: string; password: string }) {
      const res = await loginInterface(formData).catch((err: any) => {
        const message = err.response.data
        ElMessage.error(message)
      })
      if (res) {
        const id = res.data.data.id
        this.token = res.data.data.token

        //1.把token保存到浏览器中（在浏览器刷新的时候不会丢失token）
        MYLocalStorage.setLocalStorage(TOKEN, this.token)

        // 2.把登录用户信息保存到本地
        const userInfos = await getuserInfo(id)
        const user = userInfos.data.data
        this.userInfos = user
        MYLocalStorage.setLocalStorage(USER_INFO, user)

        // 3.根据用户信息，请求用户（角色）对应的菜单
        const menuInfo = await getMenuInfo(id)
        const menu = menuInfo.data.data
        console.log(user)
        console.log(id)
        console.log(menuInfo)

        MYLocalStorage.removeLocalStorage(USER_MENU)
        this.menuInfos = menu
        MYLocalStorage.setLocalStorage(USER_MENU, menu)

        const mainStore = useMainStore()
        mainStore.getDepartmentRoleData()

        //  4.通过菜单动态注册路由
        mapMenuToRoute(menu, "main")
      }

      //2.在点击登录按钮的时候，跳转到main页面
      router.replace("/main")
    },
    //刷新重新获取本地保存的信息，和重新执行注册路由函数
    getInfosRoute() {
      const token = MYLocalStorage.getLocalStorage(TOKEN)
      const userInfos = MYLocalStorage.getLocalStorage(USER_INFO)
      const menuInfos = MYLocalStorage.getLocalStorage(USER_MENU)
      if (token && userInfos && menuInfos) {
        this.token = token
        this.userInfos = userInfos
        this.menuInfos = menuInfos
        mapMenuToRoute(this.menuInfos, "main")
      }
      //刷新页面重新请求数据
      const mainStore = useMainStore()
      mainStore.getDepartmentRoleData()
    }
  }
})

export default useLoginStore
