<template>
  <div class="content app-container">
    <div class="filter-container">
        <el-input v-model="boundary.NorthEast_location_lng" placeholder="东北经度坐标..." style="width: 200px;" class="filter-item" />
        <el-input v-model="boundary.NorthEast_location_lat" placeholder="东北纬度坐标..." style="width: 200px;" class="filter-item" />
        <el-input v-model="boundary.SouthWest_location_lng" placeholder="西南经度坐标..." style="width: 200px;" class="filter-item" />
        <el-input v-model="boundary.SouthWest_location_lat" placeholder="西南纬度坐标..." style="width: 200px;" class="filter-item" />
        
        <el-button  class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
          搜索
        </el-button>
    </div>
    <div :id="id" class="tmp" ></div>
  </div>
</template>

<style scoped>
  .tmp{
    width: 100%;
    height: 550px;
  }
</style>

<script>
import echarts from 'echarts'
import resize from './mixins/resize'
import axios from 'axios'
import qs from "qs"

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    id: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '200px'
    },
    height: {
      type: String,
      default: '200px'
    }
  },
  data() {
    return {
      chart: null,
      boundary:{
        NorthEast_location_lng:"",
        NorthEast_location_lat:"",
        SouthWest_location_lng:"",
        SouthWest_location_lat:"",
      },
      total_data:[
            709,
            1917,
            2455,
            2610,
            1719,
            1433,
            1544,
            3285,
            5208,
            3372,
            2484,
            4078
          ]
    }
  },
  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    handleFilter(){
        this.$axios.post(
                  this.$baseURL+'data/queryHourChangeByArea', 
                  qs.stringify({
                      // location: JSON.stringify({"x":parseFloat(this.bike_around.center_lng),"y":parseFloat(this.bike_around.center_lat)}),
                      NorthEast_location: JSON.stringify({"x":this.boundary.NorthEast_location_lng,"y":this.boundary.NorthEast_location_lat}),
                      SouthWest_location: JSON.stringify({"x":this.boundary.SouthWest_location_lng,"y":this.boundary.SouthWest_location_lat}),
                      time:               JSON.stringify({"first":0,"second": 23})

                  }),
                  { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
                  )
        .then((response)=>{
              //  console.log(response.data.map[0])
              //  this.total_data.push(response.data.map)
               this.total_data = Object.values(response.data.map)
               console.log(this.total_data)
               this.initChart()

        })
        .catch((error)=>{
                alert(2)
              // console.info(error);
        });
    },
    initChart() {
      this.chart = echarts.init(document.getElementById(this.id))
      const xData = (function() {
        const data = []
        for (let i = 0; i < 23; i++) {
          data.push(i + ':00')
        }
        return data
      }())
      this.chart.setOption({})
      this.chart.setOption({
        backgroundColor: '#344b58',
        title: {
          text: 'statistics',
          x: '20',
          top: '20',
          textStyle: {
            color: '#fff',
            fontSize: '22'
          },
          subtextStyle: {
            color: '#90979c',
            fontSize: '16'
          }
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            textStyle: {
              color: '#fff'
            }
          }
        },
        grid: {
          left: '5%',
          right: '5%',
          borderWidth: 0,
          top: 150,
          bottom: 95,
          textStyle: {
            color: '#fff'
          }
        },
        legend: {
          x: '5%',
          top: '10%',
          textStyle: {
            color: '#90979c'
          },
          data: ['一天中每个时间段订单数', 'male', 'average']
        },
        calculable: true,
        xAxis: [{
          type: 'category',
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          splitLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          splitArea: {
            show: false
          },
          axisLabel: {
            interval: 0

          },
          data: xData
        }],
        yAxis: [{
          type: 'value',
          splitLine: {
            show: false
          },
          axisLine: {
            lineStyle: {
              color: '#90979c'
            }
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            interval: 0
          },
          splitArea: {
            show: false
          }
        }],
        dataZoom: [{
          show: true,
          height: 30,
          xAxisIndex: [
            0
          ],
          bottom: 30,
          start: 10,
          end: 80,
          handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
          handleSize: '110%',
          handleStyle: {
            color: '#d3dee5'

          },
          textStyle: {
            color: '#fff' },
          borderColor: '#90979c'

        }, {
          type: 'inside',
          show: true,
          height: 15,
          start: 1,
          end: 35
        }],
        series: [{
          name: '一天中每个时间段订单数',
          type: 'bar',
          stack: 'total',
          barMaxWidth: 35,
          barGap: '10%',
          itemStyle: {
            normal: {
              color: 'rgba(255,144,128,1)',
              label: {
                show: true,
                textStyle: {
                  color: '#fff'
                },
                position: 'insideTop',
                formatter(p) {
                  return p.value > 0 ? p.value : ''
                }
              }
            }
          },
          data: this.total_data
        },

        ]
      })
    }
  }
}
</script>
