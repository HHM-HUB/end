<template>
  <div class="phone">
    <el-form size="large">
      <el-form-item label="手机号">
        <el-input />
      </el-form-item>
      <el-form-item label="验证码">
        <el-input class="passwork" label-width="1000px" />
        <el-button type="primary">获取验证码</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">



</script>

<style lang="less" scoped>
.phone {
  color: red;
}

.passwork {
  display: inline-block;
  width: 120px;
  margin-right: 10px;
}
</style>
