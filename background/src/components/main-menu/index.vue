<template>
  <div class="main-menu">
    <div class="title">
      <img src="@/assets/img/logo.svg">
      <h2 v-show="!isFold">贵狮后台管理系统</h2>
    </div>
    <div class="menu">
      <el-menu background-color="#001529" text-color="#b7bdc3" :default-active="defaultActive" :collapse="isFold"
        :collapse-transition="false">
        <template v-for="item in menuInfos" :key="item.id">
          <el-sub-menu :index="item.id + ''">
            <template #title>
              <el-icon>
                <component :is="item.icon.split('-icon-')[1]"></component>
              </el-icon>
              <span>{{ item.name }}</span>
            </template>
            <template v-for="content in item.children" :key="content.id">
              <el-menu-item :index="content.id + ''" @click="clickMenu(content)">
                {{ content.name }}
              </el-menu-item>
            </template>
          </el-sub-menu>
        </template>
      </el-menu>
    </div>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import useLoginStore from '@/store/login'
import { mapUrlToMenu } from '@/utils/map-menu-to-router';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
defineProps({
  isFold: {
    type: Boolean,
    default: false
  }
})
const emit = defineEmits(["name"])
const loginStore = useLoginStore()
let menuInfos = loginStore.menuInfos

function clickMenu(content: any) {
  const url = content.url
  router.push(url)
  emit("name", url)
}

//菜单匹配
const route = useRoute()
const { key } = mapUrlToMenu(menuInfos, route.path)
const defaultActive = ref(key.id + "")


</script>

<style lang="less" scoped>
.main-menu {
  height: 100%;
  background-color: #0c2135;

  .title {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 10px;
    margin-bottom: 10px;

    img {
      width: 30px;
      height: 30px;
    }

    h2 {
      margin-left: 5px;
      font-size: 16px;
      color: #fff;
    }
  }

  .menu {
    .el-menu {
      border: none;

      .el-sub-menu {

        // 表示el-menu-item元素中的背景颜色
        .el-menu-item {
          background-color: #0c2135;
        }

        // 表示鼠标悬浮el-menu-item元素中的背景颜色
        .el-menu-item:hover {
          color: #fff;
          background-color: #053f76;
        }

        // 表示选中el-menu-item元素中的背景颜色
        .el-menu-item.is-active {
          color: #fff;
          background-color: #053f76;
        }
      }

    }
  }

}

.el-menu-item:hover {
  background-color: #053f76;
  // color: #409eff;
  color: #fff;
}
</style>
