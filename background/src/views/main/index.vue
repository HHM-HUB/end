<template>
  <div class="main">
    <el-container>
      <el-aside :width="isFlag ? '60px' : '200px'">
        <main-menu :isFold="isFlag"></main-menu>
      </el-aside>
      <el-container>
        <el-header height="50px">
          <main-header @isFold="isFold"></main-header>
        </el-header>
        <el-main>
          <!-- <RouterView v-slot="props">
            <KeepAlive>
              <component :is="props.Component"></component>
            </KeepAlive>
          </RouterView> -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';


const isFlag = ref(false)
function isFold(fold: any) {
  isFlag.value = fold
}


</script>

<style lang="less" scoped>
.main {
  height: 100%;
  user-select: none;

  .el-container {
    height: 100%;

    .el-aside {
      transition: width .3s ease;

      &::-webkit-scrollbar {
        display: none;
        overflow: hidden;
      }
    }

    .el-header {
      border-bottom: 2px #303133 solid;
    }

    .el-main {
      background-color: #F0F2F5;
    }
  }
}
</style>
