<template>
  <div class="content app-container">
    <div class="filter-container">
    <el-time-picker
      is-range
      v-model="time_range"
      range-separator="至"
      start-placeholder="开始时间"
      end-placeholder="结束时间"
      placeholder="选择时间范围">
    </el-time-picker>
    
    <el-button  class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
      搜索
    </el-button>
    </div>

    <baidu-map class="bm-view" :center="center" :zoom="zoom" :map-style="mapStyle"  @ready="handler">

    </baidu-map>

  </div>
</template>

<script>
import axios from 'axios'
import qs from "qs"
import { node } from 'clipboard';

export default {
  name: "Mapv",
  data() {
    return {
      mapvLayer:"",
      MAP:0,

      // 时间选择变量
      time_range: [new Date(2016, 9, 10, 7, 0), new Date(2016, 9, 10, 8, 0)],

      // 弹出框是否弹出
      isShow_run:false,
      bikeID:0,
      center: { lng: 0, lat: 0 },
      zoom: 10,
      mapStyle: { style: "dark" },
      // 矩形窗口四个点
      // NorthEast_location: JSON.stringify({"x": 121.5, "y": 31.3}),
      // SouthWest_location: JSON.stringify({"x": 121.4, "y": 31.5}),
      polygonPath: [
        {lng: 0, lat: 0},
        {lng: 0, lat: 0}, 
        {lng: 0, lat: 0},
        {lng: 0, lat: 0}

      ],
      // 点击后信息窗口的经纬度对象
      massage_window_position:{
        lng:121.4,
        lat:31.3
      },
      // 点击每个点后的信息窗口
      infoWindow: {
        show: false,
        // contents: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
      }
    };
  },
  watch: {},
  mounted() {
    // console.log(mapv.OpenlayersLayer, mapv.DataSet, mapv.utilCityCenter)
  },
  methods: {
    // 从后端获取数据
    handleFilter(){
      var mapv = require("mapv");
        if(this.mapvLayer != ""){
          this.mapvLayer.hide()
        }
        var randomCount = 1000;

        var data = [];

        var citys = ["北京","天津","上海","重庆","石家庄","太原","呼和浩特","哈尔滨","长春","沈阳","济南","南京","合肥","杭州","南昌","福州","郑州","武汉","长沙","广州","南宁","西安","银川","兰州","西宁","乌鲁木齐","成都","贵阳","昆明","拉萨","海口"];
        

        // function getRndInteger_lng() {
        //     return Math.floor(Math.random() * (120.9 - 116.2 + 1) ) + 116.2;
        // }
        // function getRndInteger_lat() {
        //     return Math.floor(Math.random() * (39 - 30 + 1) ) + 30;
        // }
        // // 构造数据
        // while (randomCount--) {
        //     // var cityCenter = mapv.utilCityCenter.getCenterByCityName(citys[parseInt(Math.random() * citys.length)]);
        //     data.push({
        //         geometry: {
        //             type: 'Point',
        //             coordinates: [getRndInteger_lng(), getRndInteger_lat()]
        //         },
        //         count: 30 * Math.random(),
        //         time: 100 * Math.random()
        //     });
        // }

        this.$axios.post(
            this.$baseURL+'data/listDataByAreaAndTime', 
            qs.stringify({
                time: JSON.stringify({"first":7,"second":8})
            }),
            { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
        )
      .then((response)=>{
            // console.log(response.data.list[0])
            console.log(response.data.list[0].length)
            for(var i=0; i<response.data.list[0].length; i++){
                console.log(response.data.list[0][i].end_location_x)
                data.push({
                    geometry: {
                        type: 'Point',
                        coordinates: [response.data.list[0][i].end_location_x, response.data.list[0][i].end_location_y]
                    }
                });
            }
            // console.log(data)
            // console.log('---------------')
            var dataSet = new mapv.DataSet(data);
            // console.log(dataSet)
            var options = {
                // shadowColor: 'rgba(255, 250, 50, 1)',
                // shadowBlur: 10,
                fillStyle: 'rgba(255, 50, 0, 1.0)', // 非聚合点的颜色
                size: 5, // 非聚合点的半径
                minSize: 8, // 聚合点最小半径
                maxSize: 31, // 聚合点最大半径
                globalAlpha: 0.8, // 透明度
                clusterRadius: 150, // 聚合像素半径
                methods: {
                    click: function(item) {
                        console.log(item);  // 点击事件
                    }
                },
                maxZoom: 19, // 最大显示级别
                label: { // 聚合文本样式
                    show: true, // 是否显示
                    fillStyle: 'white',
                    // shadowColor: 'yellow',
                    // font: '20px Arial',
                    // shadowBlur: 10,
                },
                gradient: { 0: "blue", 0.5: 'yellow', 1.0: "rgb(255,0,0)"}, // 聚合图标渐变色
                draw: 'cluster'
            }


            var mapvLayer = new mapv.baiduMapLayer(this.MAP, dataSet, options);
        })
      .catch((error)=>{
              alert(2)
            // console.info(error);
            });
        

      
    },
   
    handler({ BMap, map }) {
      map.enableScrollWheelZoom(true); // 开启鼠标滚轮缩放
      // map.setMapStyle({
      //       style: 'night'
      //   });
      map.setMapStyle({
            styleJson: [{
                "featureType": "water",
                "elementType": "all",
                "stylers": {
                    "color": "#031628"
                }
            }, {
                "featureType": "land",
                "elementType": "geometry",
                "stylers": {
                    "color": "#000102"
                }
            }, {
                "featureType": "highway",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#000000"
                }
            }, {
                "featureType": "highway",
                "elementType": "geometry.stroke",
                "stylers": {
                    "color": "#147a92"
                }
            }, {
                "featureType": "arterial",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#000000"
                }
            }, {
                "featureType": "arterial",
                "elementType": "geometry.stroke",
                "stylers": {
                    "color": "#0b3d51"
                }
            }, {
                "featureType": "local",
                "elementType": "geometry",
                "stylers": {
                    "color": "#000000"
                }
            }, {
                "featureType": "railway",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#000000"
                }
            }, {
                "featureType": "railway",
                "elementType": "geometry.stroke",
                "stylers": {
                    "color": "#08304b"
                }
            }, {
                "featureType": "subway",
                "elementType": "geometry",
                "stylers": {
                    "lightness": -70
                }
            }, {
                "featureType": "building",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#000000"
                }
            }, {
                "featureType": "all",
                "elementType": "labels.text.fill",
                "stylers": {
                    "color": "#857f7f"
                }
            }, {
                "featureType": "all",
                "elementType": "labels.text.stroke",
                "stylers": {
                    "color": "#000000"
                }
            }, {
                "featureType": "building",
                "elementType": "geometry",
                "stylers": {
                    "color": "#022338"
                }
            }, {
                "featureType": "green",
                "elementType": "geometry",
                "stylers": {
                    "color": "#062032"
                }
            }, {
                "featureType": "boundary",
                "elementType": "all",
                "stylers": {
                    "color": "#465b6c"
                }
            }, {
                "featureType": "manmade",
                "elementType": "all",
                "stylers": {
                    "color": "#022338"
                }
            }, {
                "featureType": "label",
                "elementType": "all",
                "stylers": {
                    "color": "#022338",
                    "visibility": "off"
                }
            }]
        });
      
      // console.log(BMap, map);
      this.center.lng = 121.4;
      this.center.lat = 31.4;
      this.zoom = 5;
      var randomCount = 31;
      var citys = [
        "北京",
        "天津",
        "上海",
        "重庆",
        "石家庄",
        "太原",
        "呼和浩特",
        "哈尔滨",
        "长春",
        "沈阳",
        "济南",
        "南京",
        "合肥",
        "杭州",
        "南昌",
        "福州",
        "郑州",
        "武汉",
        "长沙",
        "广州",
        "南宁",
        "西安",
        "银川",
        "兰州",
        "西宁",
        "乌鲁木齐",
        "成都",
        "贵阳",
        "昆明",
        "拉萨",
        "海口"
      ];
      this.MAP = map
      // console.log(this.MAP)
      // list: [{"NorthEast_location": {"x": 121.5, "y": 31.4}, "SouthWest_location": {"x": 121.3, "y": 31.5}}, {"NorthEast_location": {"x": 121.8, "y": 31.1}, "SouthWest_location": {"x": 121.5, "y": 31.3}}], time: {"first":7,"second":8}
// 从后端导入数据

    }
  }
};
</script>

<style lang="scss" scoped>
.content {
  height: 100%;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  .bm-view {
    width: 100%;
    height: 81vh;
  }
}
.run_button{
  background-color: rgb(46, 194, 144);
  color: white;
}
</style>
<style>
/*去除百度地图版权*/
.anchorBL {
  display: none;
}
</style>