<template>
  <div class="overview">
    <el-row :gutter="15">
      <template v-for="item in countData" :key="item">
        <el-col :span="6">
          <show-text :top-text="item.title" :number1="item.number1" :number2="item.number2" :bottom-text="item.subtitle"
            :tooltip-text="item.tips" :amount="item.amount">
          </show-text>
        </el-col>
      </template>
    </el-row>

    <el-row class="middle" :gutter="15">
      <el-col :span="12">
        <title-card header="饼图(商品个数)">
          <pie :data="mapPieData" />
        </title-card>
      </el-col>
      <el-col :span="12">
        <title-card header="玫瑰饼图(商品销量)">
          <rose-pie :data="mapRosePieData" />
        </title-card>
      </el-col>
    </el-row>

    <el-row :gutter="15">
      <el-col :span="12">
        <title-card header="折线图(商品收藏)">
          <category :value="mapFavorData.value" :name="mapFavorData.name" />
        </title-card>
      </el-col>
      <el-col :span="12">
        <title-card header="条形图(商品统计)">
          <direct :value="mapDirectData.value" :name="mapDirectData.name" />
        </title-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import dashboardStore from '@/store/main/analysis/dashboard';
import showText from './components/showText.vue'
import titleCard from './components/titleCard.vue'
import pie from '@/components/page-echarts/pie-config.vue'
import rosePie from '@/components/page-echarts/rosePie-config.vue'
import category from '@/components/page-echarts/category-config.vue'
import direct from '@/components/page-echarts/direct-config.vue'
import { storeToRefs } from 'pinia';
import { computed } from 'vue';
import { transformEchartsLineData, transformEchartsPieData } from '@/utils/networkDataTransform';


//进入这个页面，就调用异步函数请求数据
const useDashboardStore = dashboardStore()
useDashboardStore.fetchAnalysisDateAction()

//请求下来数据之后，拿到数据(useDashboardStore是一个对象，所以通过解构拿到)
const { countData, pieData, rosePieData, favorData, mapData } = storeToRefs(useDashboardStore)

const mapPieData = computed(() => transformEchartsPieData(pieData.value))

const mapRosePieData = computed(() => transformEchartsPieData(rosePieData.value))

const mapFavorData = computed(() => transformEchartsLineData(favorData.value))

const mapDirectData = computed(() => transformEchartsLineData(rosePieData.value))

</script>

<style lang="less" scoped>
.middle {
  margin: 15px 0;

}

/deep/ .el-card__header {
  text-align: center;
  font-size: 14px;
  color: #999;
  padding: 10px 20px;
}
</style>
