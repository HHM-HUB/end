<template>
  <div class="main-header">
    <div class="left">
      <el-icon size="25px" @click="clickCrumbs">
        <component :is="isFFold ? 'Fold' : 'Expand'"></component>
      </el-icon>
      <div class="crumbs">
        <el-breadcrumb :separator-icon="ArrowRight">
          <el-breadcrumb-item>{{ obj.iterator.name }}</el-breadcrumb-item>
          <el-breadcrumb-item>{{ obj.key.name }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
    </div>
    <div class="content">
      <user-info></user-info>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, reactive, watchEffect } from 'vue';
import { ArrowRight } from '@element-plus/icons-vue'
import useLoginStore from '@/store/login';
import { useRoute } from 'vue-router';
import { mapUrlToMenu } from '@/utils/map-menu-to-router';


const emits = defineEmits(["isFold"])

const isFFold = ref(false)
function clickCrumbs() {
  isFFold.value = !isFFold.value
  emits("isFold", isFFold.value)
}

//设置面包屑
const loginStore = useLoginStore()
const menus = loginStore.menuInfos
const route = useRoute()
let obj = ref(mapUrlToMenu(menus, route.path))

// watch(route, (newValue) => {
//   const { key, iterator } = mapUrlToMenu(menus, newValue.path)
//   obj.key = key
//   obj.iterator = iterator
// })
watchEffect(() => {
  obj.value = mapUrlToMenu(menus, route.path)
})

// const obj = computed(() => {
//   return mapUrlToMenu(menus, route.path)
// })


</script>

<style lang="less" scoped>
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  font-size: 14px;

  .left {
    display: flex;
    align-items: center;

    .crumbs {
      margin-left: 20px;

      :deep(.el-breadcrumb__inner:nth-child(1)) {
        color: #000;
      }
    }

  }
}
</style>
