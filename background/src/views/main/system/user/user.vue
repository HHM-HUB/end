<template>
  <div class="user">
    <div class="search">
      <mainSearch @getSearchData="searchData" @reset="reset"></mainSearch>
    </div>
    <div class="header">
      <mainHeader ref="listObj" @changeFlag="changeFlag" @edit="editUser"></mainHeader>
    </div>
    <div class="form">
      <mainForm ref="flag"></mainForm>
    </div>
  </div>
</template>

<script setup lang="ts">
import mainSearch from "./components/main-search.vue";
import mainHeader from "./components/main-header.vue";
import mainForm from "./components/main-form.vue";
import { ref } from "vue";

//搜索函数
const listObj = ref<InstanceType<typeof mainHeader>>()
function searchData(form: any) {
  listObj?.value?.getListDate(form)
}


// 重置函数
function reset() {
  listObj?.value?.getListDate()
}

//点击新建用户函数
const flag = ref()
function changeFlag() {
  flag?.value.changeVisible()
}

// 编辑用户函数
function editUser(data: any) {
  flag?.value.changeVisible(data, false)
}
</script>

<style lang="less" scoped>
.user {
  color: #000;

  .search {
    margin-bottom: 20px;
  }
}
</style>
