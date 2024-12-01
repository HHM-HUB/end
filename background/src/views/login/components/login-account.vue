<template>
  <div class="account">
    <el-form :model="formData" :rules="rules" size="large" ref="formRef">
      <el-form-item prop="account" label="账号">
        <el-input v-model="formData.account" />
      </el-form-item>
      <el-form-item prop="password" label="密码">
        <el-input v-model="formData.password" type="password" show-password />
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
// 声明这个对象为规则相应的类型，有更加友好的提示
import type { FormRules, ElForm } from 'element-plus'
import { ElMessage } from 'element-plus'
import useLoginStore from '@/store/login';
import { MYLocalStorage } from '@/utils/storage';
import { ACCOUNT, PASSWROM } from '@/global/constants';
const formRef = ref<InstanceType<typeof ElForm>>()

const formData = reactive({
  account: MYLocalStorage.getLocalStorage(ACCOUNT) ?? "",
  password: MYLocalStorage.getLocalStorage(PASSWROM) ?? ""
})

// 定义规则是定义在一个对象里面,规则名字需pattechange要和rules对应，每一个key值都和prop值一一对应
const rules: FormRules = {
  // 对应一个数组，因为一个表单可能有多个规则.requiredb表示是否必填，trigger表示提示触发规则为失去焦点,pattern为正值规则
  account: [
    { required: true, message: "输入的账号不能为空", trigger: "blur" },
    { min: 6, max: 16, message: "长度必须为6-16位", trigger: "change" },
    // { pattern: /^[\d\w]{6,16}/, message: "账号长度为6-16位，且不能包括违法符号", trigger: "blur" },
  ],
  password: [
    { required: true, message: "输入的密码不能为空", trigger: "blur" },
    // { pattern: /^[\d\w]{6,16}/, message: "密码长度为6-16位，且不能包括违法符号", trigger: "blur" },
    { min: 6, max: 16, message: "长度必须为6-16位", trigger: "change" }
  ]
}

//拿到login中的store
const loginStore = useLoginStore()
function fooAccount(isKeepPass: boolean) {
  formRef.value?.validate(async (res, err) => {
    if (res) {
      // 发送请求，拿到token
      loginStore.getLoginToken(formData).then(() => {
        console.log(isKeepPass)
        //登录成功后,通过是否选择记住密码，来是否保存密码
        if (isKeepPass) {
          MYLocalStorage.setLocalStorage(ACCOUNT, formData.account)
          MYLocalStorage.setLocalStorage(PASSWROM, formData.password)
        } else {
          MYLocalStorage.removeLocalStorage(ACCOUNT)
          MYLocalStorage.removeLocalStorage(PASSWROM)
        }
      })


    } else {
      let message: string | undefined = ""
      if (err?.account !== undefined) {
        message = err?.account[0].message
      }
      if (err?.password !== undefined && !message) {
        message = err?.password[0].message
      }
      ElMessage.error(message)
    }
  })
}

defineExpose({
  fooAccount
})
</script>

<style lang="less" scoped>
.account {
  color: red;
}
</style>
