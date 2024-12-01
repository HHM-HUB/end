<template>
  <div class="main-form">
    <el-dialog v-model="centerDialogVisible" :title="flag ? '新建用户' : '编辑用户'" width="30%" center>
      <div class="form">
        <el-form :model="formDate" label-width="70px">
          <el-form-item label="用户名" prop="name">
            <el-input v-model="formDate.name" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item v-if="flag" label="密码" prop="password">
            <el-input v-model="formDate.password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item label="真实姓名" prop="realname">
            <el-input v-model="formDate.realname" placeholder="请输入真实姓名" />
          </el-form-item>
          <el-form-item label="手机号" prop="cellphone">
            <el-input v-model="formDate.cellphone" placeholder="请输入手机号" />
          </el-form-item>
          <el-form-item label="角色" prop="roleId">
            <el-select v-model="formDate.roleId" placeholder="请选择角色" style="width: 100%;">
              <template v-for="item in RoleList" :key="item.id">
                <el-option :label="item.name" :value="item.id" />
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="部门" prop="departmentId">
            <el-select v-model="formDate.departmentId" placeholder="请选择部门" style="width: 100%;">
              <template v-for="item in departmentList" :key="item.id">
                <el-option :label="item.name" :value="item.id" />
              </template>
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="centerDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createUser">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import useMainStore from '@/store/main/index'
import useSystemStore from "@/store/main/system"
import { storeToRefs } from 'pinia';


const formDate = reactive<any>({
  name: "",
  realname: "",
  password: "",
  cellphone: "",
  roleId: "",
  departmentId: ""
})

const flag = ref(true)
let id = ref()
console.log(formDate)
//控制新建用户窗口弹窗函数
const centerDialogVisible = ref(false)
function changeVisible(form?: any, falg = true) {
  centerDialogVisible.value = true
  flag.value = true
  if (!falg) {
    for (const key in form) {
      for (const formDateKey in formDate) {
        if (key === formDateKey) formDate[key] = form[key]
      }
    }
    flag.value = false
    id.value = form.id
  } else {
    for (const key in formDate) {
      formDate[key] = ""
    }
  }
}

//拿到角色部位数据
const mainStore = useMainStore()
const { departmentList, RoleList } = storeToRefs(mainStore)

//点击确定创建用户 修改用户
const systemStore = useSystemStore()
function createUser() {
  if (!flag.value && id) {
    console.log(formDate)
    systemStore.getUpdateUser(formDate, id.value)
  } else {
    systemStore.getCreateUser(formDate)
  }

  centerDialogVisible.value = false
}
defineExpose({
  changeVisible
})
</script>

<style lang="less" scoped>
.main-form {
  .form {
    padding: 0 20px;
  }
}
</style>
