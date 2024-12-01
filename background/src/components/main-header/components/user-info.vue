<template>
  <div class="userInfo">
    <div class="left">
      <el-icon>
        <ChatLineRound />
      </el-icon>
      <el-icon>
        <Postcard />
      </el-icon>
      <el-icon>
        <span class="red-dot"></span>
        <Message />
      </el-icon>
    </div>
    <div class="right">
      <el-dropdown>
        <span class="el-dropdown-link">
          <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
          <span>{{ loginStore.userInfos.name || "核心用户" }}</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="backLogin">
              <span>退出登录</span>
            </el-dropdown-item>
            <el-dropdown-item divided>个人信息</el-dropdown-item>
            <el-dropdown-item divided>修改密码</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { TOKEN } from '@/global/constants';
import router from '@/router';
import useLoginStore from '@/store/login'
import { MYLocalStorage } from '@/utils/storage';
const loginStore = useLoginStore()

//退出登录
function backLogin() {
  MYLocalStorage.removeLocalStorage(TOKEN)
  router.push("/login")
}
</script>

<style lang="less" scoped>
.userInfo {
  display: flex;
  align-items: center;
  cursor: pointer;

  .left {
    .el-icon {
      position: relative;
      font-size: 20px;
      margin-right: 10px;
    }

    .red-dot {
      position: absolute;
      width: 8px;
      height: 8px;
      background-color: red;
      border-radius: 50%;
      right: -3px;
      top: -0px;
    }
  }

  .right {
    .el-dropdown-link {
      display: flex;
      align-items: center;

      .el-avatar {
        width: 35px;
        height: 35px;
        margin: 0 5px;
      }
    }
  }
}
</style>
