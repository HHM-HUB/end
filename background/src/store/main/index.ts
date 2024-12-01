import { getDepartmentData, getMenuData, getRoleData } from "@/service/main"
import { defineStore } from "pinia"

interface IMain {
  //新增表单中，角色和部门数据
  departmentList: any[]
  RoleList: any[]
  meunList: any[]
}
const useMainStore = defineStore("main", {
  state: (): IMain => ({
    // 以下数据都是下拉菜单的数据
    departmentList: [],
    RoleList: [],
    meunList: []
  }),
  actions: {
    async getDepartmentRoleData() {
      const departmentData = await getDepartmentData()
      const RoleDate = await getRoleData()
      const menuData = await getMenuData()

      //把拿到的数据存入store中
      this.departmentList = departmentData.data.data.list
      this.RoleList = RoleDate.data.data.list
      this.meunList = menuData.data.data.list
    }
  }
})

export default useMainStore
