<template>
  <div class="login">
    <div class="main">
      <h1>后台管理系统</h1>
      <!-- tap标签栏 -->
      <div class="taps">
        <el-tabs type="border-card" stretch v-model="activeName">
          <el-tab-pane name="account" label="账号登录">
            <template #label>
              <div class="accountLabel">
                <el-icon>
                  <UserFilled />
                </el-icon>
                <span>账号登录</span>
              </div>
            </template>
            <login-account ref="account"></login-account>
          </el-tab-pane>
          <el-tab-pane name="phone" label="手机登录">
            <template #label>
              <div class="accountLabel">
                <el-icon>
                  <Iphone />
                </el-icon>
                <span>手机登录</span>
              </div>
            </template>
            <login-phone></login-phone>
          </el-tab-pane>
        </el-tabs>
      </div>
      <!-- 记住密码和忘记密码 -->
      <div class="rememberPass">
        <el-checkbox v-model="isKeepPass" label="记住密码" />
        <el-link :underline="false">忘记密码</el-link>
      </div>
      <!-- 立即登录 -->
      <div class="register">
        <el-button class="but" size="large" type="primary" @click="clickLogin">立即登录</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { KEEP_PASSWORK } from '@/global/constants';
import { MYLocalStorage } from '@/utils/storage';
import { ref, watch } from 'vue';
import loginAccount from './components/login-account.vue'
import loginPhone from './components/login-phone.vue'


const isKeepPass = ref<any>(MYLocalStorage.getLocalStorage(KEEP_PASSWORK) ?? false)
//通过watch监听isKeepPass（记住或不记住密码）改变，把新值记录到本地储存。
watch(isKeepPass, (newValue) => {
  MYLocalStorage.setLocalStorage(KEEP_PASSWORK, newValue)
})
const activeName = ref("account")
const account = ref<InstanceType<typeof loginAccount>>()
function clickLogin() {
  if (activeName.value === "account") {
    //点击登录，调用登录函数
    account.value?.fooAccount(isKeepPass.value)
  } else {
    console.log("你使用的手机号登录")
  }
}
</script>

<style lang="less" scoped>
.login {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: url(../../assets/img/login-bg.svg) no-repeat;

  .main {
    width: 330px;

    h1 {
      text-align: center;
    }

    .taps {
      .accountLabel {
        display: flex;
        justify-content: center;
        align-items: center;

        span {
          margin-left: 8px;
        }
      }

    }

    .rememberPass {
      display: flex;
      justify-content: space-between;
    }

    .register {
      .but {
        width: 100%;
      }
    }
  }

  .main>div {
    margin-top: 10px;
  }
}
</style>
