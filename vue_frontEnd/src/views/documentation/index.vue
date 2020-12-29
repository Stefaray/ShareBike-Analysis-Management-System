<template>
  <div class="content app-container">
    <div class="filter-container">
    <el-input v-model="bike_around.center_lng" placeholder="中心点坐标经度..." style="width: 200px;" class="filter-item" />
    <el-input v-model="bike_around.center_lat" placeholder="中心点坐标纬度..." style="width: 200px;" class="filter-item" />
    <el-input v-model="bike_around.radius" placeholder="半径(公里)..." style="width: 200px;" class="filter-item" />
    <el-button  class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
      搜索
    </el-button>
    </div>

    <baidu-map class="bm-view" :center="center" :zoom="zoom" :map-style="mapStyle" @ready="handler">
      <!-- 圆形边框 -->
      <bm-circle :center="circlePath.center" :radius="bike_around.radius*1000" stroke-color="blue" :stroke-opacity="0.5" :stroke-weight="2" @lineupdate="updateCirclePath" :editing="true"></bm-circle>      <!-- 信息窗口 -->
      <!-- 信息窗口 -->
      <bm-info-window :position="massage_window_position" title="共享单车信息" :show="infoWindow.show" @close="infoWindowClose" @open="infoWindowOpen">
        <p> 单车编号：{{ bikeID }} </p>
        <p> 经度：{{ massage_window_position.lng }} </p>
        <p> 纬度：{{ massage_window_position.lat }} </p>
        <button @click="run" class="run_button">骑行</button>
      </bm-info-window>
    </baidu-map>

<!-- 模态框----“确认骑行此单车吗” -->
    <modal title="信息确认" :is-show="isShow_run" :show-header="true" @close="isShow_run=false" ok-text="确定" cancel-text="取消" :on-ok="ok_run">
      <!-- <h4>Text in a modal</h4> -->
      <p>
        您确认骑行此为单车（编号：{{bikeID}}）吗？
      </p>
    </modal>
    <!-- <button @click="run" class="button is-primary">自定义按钮文字</button> -->

  </div>
</template>

<script>
import axios from 'axios'
import qs from "qs"

export default {
  name: "Mapv",
  data() {
    return {
      circlePath: {
        center: {
          lng: 0,
          lat: 0
        },
        radius: 100
      },
      MAP:0,
      bike_around:{
        center_lng:"",
        center_lat:"",
        radius:""
      },
      // 时间选择变量
      time_range: [new Date(2016, 9, 10, 7, 0), new Date(2016, 9, 10, 8, 0)],

      // 弹出框是否弹出
      isShow_run:false,
      mapvLayer:"",
      bikeID:0,
      bike_status:0,
      center: { lng: 0, lat: 0 },
      zoom: 5,
      mapStyle: { style: "dark" },
      // 矩形窗口四个点
      // NorthEast_location: JSON.stringify({"x": 121.5, "y": 31.3}),
      // SouthWest_location: JSON.stringify({"x": 121.4, "y": 31.5}),
      polygonPath: [
        {lng: 0, lat: 0},
        {lng: 0, lat: 0}, 
        {lng: 0, lat: 0},
        {lng: 0, lat: 0}
        // {lng: 121.4, lat: 31.3},
        // {lng: 121.5, lat: 31.3}, 
        // {lng: 121.5, lat: 31.5},
        // {lng: 121.4, lat: 31.5}
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
      // console.log(typeof(this.time_range))
      // console.log(this.time_range[0].getHours())
      if(this.bike_around.center_lng == 0 || this.bike_around.center_lat == 0 )
      {
        alert("请输入正确的坐标值")
      }
      else{
        // this.polygonPath[0].lng = this.polygonPath[3].lng = parseFloat(this.boundary.SouthWest_location_lng)
        // this.polygonPath[1].lng = this.polygonPath[2].lng = parseFloat(this.boundary.NorthEast_location_lng)
        // this.polygonPath[0].lat = this.polygonPath[1].lat = parseFloat(this.boundary.NorthEast_location_lat)
        // this.polygonPath[2].lat = this.polygonPath[3].lat = parseFloat(this.boundary.SouthWest_location_lat)
        // console.log(this.polygonPath)
        // 赋值，画出圆形边框
        this.circlePath.radius = this.bike_around.radius * 1000
        this.circlePath.center.lng = this.bike_around.center_lng
        this.circlePath.center.lat = this.bike_around.center_lat

        this.push_around_bike()
      }
      
    },
    Rad(d){
           return d * Math.PI / 180.0;//经纬度转换成三角函数中度分表形式。
    },
    //计算距离，参数分别为第一点的纬度，经度；第二点的纬度，经度
    GetDistance(lat1,lng1,lat2,lng2){
        var radLat1 = this.Rad(lat1);
        var radLat2 = this.Rad(lat2);
        var a = radLat1 - radLat2;
        var  b = this.Rad(lng1) - this.Rad(lng2);
        var s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a/2),2) +
        Math.cos(radLat1)*Math.cos(radLat2)*Math.pow(Math.sin(b/2),2)));
        s = s *6378.137 ;// EARTH_RADIUS;
        s = Math.round(s * 10000) / 10000; //输出为公里
        //s=s.toFixed(4);
        return s;
    },
    // 布置海量点
    push_around_bike(){
        var mapv = require("mapv");
        var data = [];
        if(this.bike_around.radius == 0){
          this.bike_around.radius = 1
        }
        if(this.mapvLayer != ""){
          this.mapvLayer.hide()
        }
        
        
        console.log(this.circlePath.radius)
        this.$axios.post(
                  this.$baseURL+'data/queryBikesByPointAndRadius'+'/'+this.bike_around.radius, 
                  qs.stringify({
                      location: JSON.stringify({"x":parseFloat(this.bike_around.center_lng),"y":parseFloat(this.bike_around.center_lat)}),
                  }),
                  { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
                  )
        .then((response)=>{
                data = []
                // var sum = 0
                var total_num = response.data.res.length
                console.log(total_num)
                console.log(response.data.res)
                for(var i=0; i<total_num; i++){
                  // 导入数据
                  if(this.GetDistance(this.circlePath.center.lat,this.circlePath.center.lng,response.data.res[i].location_y,response.data.res[i].location_x)*1000 <= this.circlePath.radius){
                    // console.log(this.GetDistance(this.circlePath.center.lat,this.circlePath.center.lng,response.data.res[i].location_y,response.data.res[i].location_x))
                    // sum+=1
                    data.push({
                      geometry: {
                        type: "Point",
                        coordinates: [
                          response.data.res[i].location_x,
                          response.data.res[i].location_y
                        ],
                        bikeID:response.data.res[i].bikeid,
                        bike_status:response.data.res[i].status
                      },
                    });
                  }
                }
                // console.log(data)
                  var dataSet = new mapv.DataSet(data);
                  // console.log(dataSet);
                  console.log(this.infoWindow)
                  // console.log(infoWindow1)
                  var options = {
                    fillStyle: "rgba(255, 50, 50, 0.6)",
                    shadowColor: "rgba(255, 50, 50, 0)",
                    shadowBlur: 30,
                    // globalCompositeOperation: "lighter",
                    methods: {
                      click: (item)=> {
                        if(item){
                          // console.log(item.geometry.coordinates);
                          console.log(item.geometry.bikeID)
                          this.infoWindowOpen()
                          console.log(this.infoWindow)
                          this.bikeID = item.geometry.bikeID
                          this.massage_window_position.lng = item.geometry.coordinates[0]
                          this.massage_window_position.lat = item.geometry.coordinates[1]
                        }
                      }
                    },
                    size: 5,
                    draw: "simple"
                  };

                  this.mapvLayer = new mapv.baiduMapLayer(this.MAP, dataSet, options);
                  // console.log("hello2");
                  // this.center.lng = 105.403119;
                  // this.center.lat = 38.028658;
                  // this.zoom = 5;
                  this.mapvLayer.show(); // 显示图层
                  
                console.log(response.data.res.length)
              })
        .catch((error)=>{
                alert(2)
              // console.info(error);
              });
        console.log(data)
      },
    // "骑行成功！！"
    ok_run() {
      var data = {
          username:           this.$root.username,
          bikeid:             this.bikeID,
          start_location_x:   this.massage_window_position.lng,
          start_location_y:   this.massage_window_position.lat
      }
      // 将新增的骑行订单反馈到后台
      this.$axios.post(
            this.$baseURL+'order/addGoingOrder', 
            qs.stringify({data:JSON.stringify(data)}),
            { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
      )
      .then((response)=>{
            // alert('hahaha')
             console.log(response)
             this.$notify.open({
              type: 'success',
              title: `骑行成功！！！`,
             });
        })
      .catch((error)=>{
            alert("您有正在骑行的订单，请及时处理！")
            console.info(error);
            });
      // console.log(this.$root.username)
    },
    // 点击每个单车的信息窗口函数
    infoWindowClose (e) {
      this.infoWindow.show = false
    },
    infoWindowOpen (e) {
      this.infoWindow.show = true
      // this.infoWindow.contents = abc
    },
    run () {
      // this.infoWindow.contents = ''
      this.isShow_run = true
    },

    // 圆形窗口
    updateCirclePath (e) {
      this.circlePath.center = e.target.getCenter()
      this.circlePath.radius = e.target.getRadius()
    },
    handler({ BMap, map }) {
      map.enableScrollWheelZoom(true); // 开启鼠标滚轮缩放
      map.setMapStyle({
            style: 'light'
        });
      this.center.lng = 105.403119;
      this.center.lat = 38.028658;
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