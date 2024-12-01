<template>
  <div class="role">
    <page-search :searchConfig="searchConfig" @getSearchData="searchData" @reset="reset"></page-search>
    <page-user-list :userListConfig="userListConfig" ref="listObj" @changeFlag="increase" @edit="edit"></page-user-list>
    <page-dialog :dialogConfig="dialogConfig" :selectNode="allNode" ref="formOpen" @getMeunList="getMeunListData"
      @cleanMeunTree="cleanMeunTree" @changePage="changePage">
      <template #menuList>
        <div class="meun">
          <label for="">菜单列表</label>
          <el-tree @check="clickTree" :data="meunList" show-checkbox node-key="id" :props="defaultProps"
            ref="elTreeRef" />
        </div>
      </template>
    </page-dialog>
  </div>
</template>

<script setup lang="ts" name="role">
import { storeToRefs } from 'pinia'
import { nextTick, ref } from 'vue'

import pageSearch from '@/components/page-search/page-search.vue'
import searchConfig from './page-config/search-config'

import pageUserList from '@/components/page-userList/page-userList.vue'
import userListConfig from './page-config/userList-config'

import pageDialog from '@/components/page-dialog/page-dialog.vue'
import dialogConfig from './page-config/dialog-config'

import usePageSearchBut from '@/hooks/pageSearchBut'
import usePageUserListBut from '@/hooks/pageUserListBut'

import useMainStore from '@/store/main/index'

import { getMenuTreeId } from '@/utils/getId'
import type { ElTree } from 'element-plus'

const { listObj, searchData, reset } = usePageSearchBut()
const { formOpen, increase, edit } = usePageUserListBut()

const defaultProps = {
  children: 'children',
  label: 'name',
}
const MainStore = useMainStore()
const { meunList } = storeToRefs(MainStore)


// 点击多选框数触发的事件
let allNode = ref({})
function clickTree(data1: any, data2: any) {
  let menuList = [...data2.checkedKeys, ...data2.halfCheckedKeys]
  allNode.value = { menuList }
}
// let checkedKeys: any[] = []
//获取点击编辑菜单树需要回显的数据
const elTreeRef = ref<InstanceType<typeof ElTree>>()
function getMeunListData(data: any) {
  nextTick(() => {
    const selectId = getMenuTreeId(data)
    elTreeRef.value?.setCheckedKeys(selectId)
  })
}
//调用这个函数，点击新增清除菜单树里面的数据
function cleanMeunTree() {
  elTreeRef.value?.setCheckedKeys([])
}

function changePage() {
  listObj.value?.changePage()
}
</script>

<style lang="less" scoped>
.meun {
  display: flex;
}

.meun label {
  margin-right: 5px;
}
</style>
