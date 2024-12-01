<template>
  <div class="menu">
    <pageUserList :userListConfig="userListConfig"></pageUserList>
  </div>
</template>

<script setup lang="ts" name="menu">
import pageUserList from '@/components/page-userList/page-userList.vue'
import userListConfig from './page-config/userList-config'
</script>

<style scoped></style>
