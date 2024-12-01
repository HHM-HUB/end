<template>
  <div class="main-header">
    <div class="title">
      <h3>用户列表</h3>
      <el-button type="primary" size="large" @click="addUser">新增用户</el-button>
    </div>
    <div class="form">
      <el-table :data="list" border style="width: 100%">
        <el-table-column align="center" type="selection" width="50" />
        <el-table-column align="center" label="序号" type="index" width="60" />
        <el-table-column align="center" prop="name" label="用户名" width="100" />
        <el-table-column align="center" prop="realname" label="真实姓名" width="100" />
        <el-table-column align="center" prop="cellphone" label="手机号" width="150" />
        <el-table-column align="center" prop="enable" label="状态" width="80">
          <template #default="item">
            <el-button type="primary" size="small" plain>{{ item.row.enable ? "启用" : "禁用" }} </el-button>
          </template>
        </el-table-column>

        <el-table-column align="center" prop="createAt" label="创建时间">
          <template #default="item">
            {{ formatUTC(item.row.createAt) }}
          </template>
        </el-table-column>

        <el-table-column align="center" prop="updateAt" label="更新时间">
          <template #default="item">
            {{ formatUTC(item.row.updateAt) }}
          </template>
        </el-table-column>
        <el-table-column align="center" label="操作" width="130">
          <template #default="item">
            <el-button type="primary" icon="EditPen" link size="small" @click="edit(item.row)">编辑</el-button>
            <el-button type="danger" icon="Delete" link size="small" @click="deleteUser(item.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-pagination v-model:current-page="currentPage" v-model:page-size="pageSize" :page-sizes="[5, 10, 15, 20]"
      layout="total, sizes, prev, pager, next, jumper" :total="userCount" @size-change="handleSizeChange"
      @current-change="handleCurrentChange" />


  </div>
</template>

<script setup lang="ts">
import useSystemStore from '@/store/main/system'
import { storeToRefs } from 'pinia';
import { formatUTC } from '@/utils/formatDate'
import { ref } from 'vue';
const systemStore = useSystemStore()
const { list, userCount } = storeToRefs(systemStore)

//分页相关数据
const currentPage = ref(1)
const pageSize = ref(10)
getListDate()
function handleSizeChange() {
  getListDate()
}
function handleCurrentChange() {
  getListDate()
}

//请求数据函数
function getListDate(from?: any) {
  const size = pageSize.value
  const offset = (currentPage.value - 1) * 10
  const info = { size, offset, ...from }
  systemStore.getUserList(info)
}

//删除用户函数
function deleteUser(id: number) {
  systemStore.getDeleteUser(id)
}

const emit = defineEmits(["changeFlag", "edit"])
// 新增用户按钮函数
function addUser() {
  emit("changeFlag")
}

// 编辑用户按钮函数
function edit(data: any) {
  emit("edit", data)
}
defineExpose({
  getListDate
})
</script>

<style lang="less" scoped>
.main-header {
  padding: 0px 40px 15px;
  margin: 15px 0;
  border-radius: 8px;
  background-color: #fff;

  .title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;

  }

  .form {
    .el-table {
      :deep(.el-table__cell) {
        padding: 10px 0;
        // background-color: aqua;
      }
    }

  }

  .el-pagination {
    display: flex;
    justify-content: center;
    margin-top: 15px;
  }
}
</style>
