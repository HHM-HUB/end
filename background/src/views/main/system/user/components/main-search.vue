<template>
  <div class="main-search">
    <el-form :model="form" ref="formRef" size="large">
      <el-row :gutter="80">
        <el-col :span="8">
          <el-form-item label="用户名" label-width="100" prop="userName">
            <el-input v-model="form.name" placeholder='请输入用户名' />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="真实姓名" prop="name">
            <el-input v-model="form.realname" placeholder='请输入真实姓名' />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="form.cellphone" placeholder='请输入手机号' />
          </el-form-item>
        </el-col>

        <el-col :span="8">
          <el-form-item label="用户状态" label-width="100" prop="select">
            <el-select v-model="form.enable" placeholder="121212" style="width: 100%">
              <el-option label="启用" :value="1" />
              <el-option label="禁用" :value="0" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="选择日期" prop="date">
            <el-date-picker v-model="form.createAt" type="daterange" range-separator="-" start-placeholder="开始日期"
              end-placeholder="结束日期" />
          </el-form-item>
        </el-col>
      </el-row>

    </el-form>

    <div class="buts">
      <el-button icon="Refresh" size="large" @click="reset">重置</el-button>
      <el-button type="primary" size="large" icon="Search" @click="search">搜索</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ElForm } from 'element-plus';
import { reactive, ref } from 'vue';
const emit = defineEmits(["getSearchData", "reset"])


const form = reactive({
  name: "",
  realname: "",
  cellphone: "",
  enable: 1,
  createAt: ""
})
const formRef = ref<InstanceType<typeof ElForm>>()
//重置按钮函数
function reset() {
  formRef.value?.resetFields()
  form.createAt = ""
  emit("reset")
}
// 搜索按钮函数
function search() {
  emit("getSearchData", form)
}
</script>

<style lang="less" scoped>
.main-search {
  padding: 40px 40px;
  margin-bottom: 15px;
  border-radius: 8px;
  background-color: #fff;

  .buts {
    text-align: right;
  }
}
</style>
