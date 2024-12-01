<template>
  <div class="menu">
    <page-search :searchConfig="searchConfig" @getSearchData="searchData" @reset="reset"></page-search>
    <page-user-list :userListConfig="userListConfig" ref="listObj" @changeFlag="increase" @edit="edit">
      <template #department="item">
        <div>---{{ item.row.name }}</div>
      </template>
    </page-user-list>

    <page-dialog :dialogConfig="mainStoreRef" ref="formOpen" @changePage="changePage"></page-dialog>
  </div>
</template>

<script setup lang="ts" name="menu">
import pageSearch from '@/components/page-search/page-search.vue'
import searchConfig from './page-config/search-config'
import userListConfig from './page-config/userList-config'
import dialogConfig from './page-config/dialog-config'


import { computed } from 'vue';
import useMainStore from '@/store/main'

import usePageSearchBut from '@/hooks/pageSearchBut'
import usePageUserListBut from '@/hooks/pageUserListBut'

// 获取部门的下拉菜单
const mainStoreRef = computed(() => {

  const mainStore = useMainStore()
  const newDialogConfig = dialogConfig
  const list = mainStore.departmentList

  const newList = list.map(item => {
    return { label: item.name, value: item.id }
  })

  newDialogConfig.dialogItem.forEach(item => {
    if (item.prop === "parentId") {
      // 添加之前先清空之前的数据
      item.options = []
      item.options?.push(...newList)
    }
  })
  return newDialogConfig
})



//拿到搜索按钮函数和重置按钮函数
const { listObj, searchData, reset } = usePageSearchBut()

//拿到新增按钮函数和编辑用户按钮函数
const { formOpen, increase, edit } = usePageUserListBut()


function changePage() {
  listObj.value?.changePage()
}
</script>

<style scoped></style>
