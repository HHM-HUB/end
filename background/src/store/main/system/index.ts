import {
  deleteUser,
  getUserListData,
  createUser,
  updateUser,
  getPageListData,
  deletePageListData,
  createPageListData,
  editPageListData
} from "@/service/main/system"
import { defineStore } from "pinia"
import { ElMessage } from "element-plus"

interface Istate {
  list: any[]
  userCount: number
  pageList: any[]
  pageCount: number
}

const useSystemStore = defineStore("system", {
  state: (): Istate => ({
    //用户的列表
    list: [],
    userCount: 0,

    // page的列表
    pageList: [],
    pageCount: 0
  }),
  actions: {
    // user页面的增删改查
    async getUserList(info: any) {
      console.log(info)
      const res = await getUserListData(info)
      this.list = res.data.data.list
      this.userCount = res.data.data.totalCount
      console.log(this.list)
    },
    async getDeleteUser(id: number) {
      const res = await deleteUser(id)
      if (res.data.code === 0) {
        ElMessage({
          message: "删除成功",
          type: "success"
        })
      } else {
        ElMessage({
          message: "该数据不能删除",
          type: "warning"
        })
      }

      //删除完数据调用这个函数重新刷新页面
      this.getUserList({ size: 10, offset: 0 })
    },
    async getCreateUser(form: any) {
      const res = await createUser(form)
      //新建完毕重新请求数据
      this.getUserList({ size: 10, offset: 0 })
      console.log(res)
      if (res.data.code === 0) {
        ElMessage({
          message: "新建用户成功",
          type: "success"
        })
      } else {
        ElMessage.error("创建失败，请检查输入是否合法")
      }
    },
    async getUpdateUser(form: any, id: number) {
      const res = await updateUser(form, id)
      console.log(res)
      if (res.data.code === 0) {
        ElMessage({
          message: "修改用户成功",
          type: "success"
        })
      }

      this.getUserList({ size: 10, offset: 0 })
    },

    // page页面的增删改查
    async getPageListData(pageName: string, form: any) {
      //切换页面的时候，先清空数据，防止上一个页面内容的残留
      // this.pageList = []
      const res = await getPageListData(pageName, form)
      console.log(res)
      this.pageList = res.data.data.list
      this.pageCount = res.data.data.totalCount
      // console.log(this.pageList, this.pageCount)
    },
    async deletePageListData(pageName: string, id: number) {
      const res = await deletePageListData(pageName, id)
      if (res.data.code === 0) {
        ElMessage({
          message: "删除成功",
          type: "success"
        })
      } else {
        ElMessage({
          message: "该数据不能删除",
          type: "warning"
        })
      }
      //删除完数据调用这个函数重新刷新页面
      this.getPageListData(pageName, { size: 10, offset: 0 })
    },
    async createPageListData(pageName: string, form: any) {
      const res = await createPageListData(pageName, form)
      console.log(res)
      this.getPageListData(pageName, { size: 10, offset: 0 })
      console.log("-----------")
      if (res.data.code === 0) {
        ElMessage({
          message: "新建成功",
          type: "success"
        })
      } else {
        ElMessage.error("创建失败，请检查输入是否合法")
      }
    },
    async editPageListData(pageName: string, form: any, id: number) {
      const res = await editPageListData(pageName, form, id)
      this.getPageListData(pageName, { size: 10, offset: 0 })
      if (res.data.code === 0) {
        ElMessage({
          message: "修改成功",
          type: "success"
        })
      }
    }
  }
})

export default useSystemStore
