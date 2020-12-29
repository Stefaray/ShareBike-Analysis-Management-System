<template>
  <div class="content app-container">
    <div class="filter-container">
    <el-input v-model="boundary.NorthEast_location_lng" placeholder="东北经度坐标..." style="width: 200px;" class="filter-item" />
    <el-input v-model="boundary.NorthEast_location_lat" placeholder="东北纬度坐标..." style="width: 200px;" class="filter-item" />
    <el-input v-model="boundary.SouthWest_location_lng" placeholder="西南经度坐标..." style="width: 200px;" class="filter-item" />
    <el-input v-model="boundary.SouthWest_location_lat" placeholder="西南纬度坐标..." style="width: 200px;" class="filter-item" />
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

    <baidu-map class="bm-view" :center="center" :zoom="zoom" :map-style="mapStyle" @ready="handler">
      <bm-polygon :path="polygonPath" stroke-color="blue" :stroke-opacity="0.1" :stroke-weight="2" :editing="true" @lineupdate="updatePolygonPath"/>
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
import { node } from 'clipboard';

export default {
  name: "Mapv",
  data() {
    return {
      mapvLayer:"",
      MAP:0,
      boundary:{
        
        NorthEast_location_lng:"",
        NorthEast_location_lat:"",
        SouthWest_location_lng:"",
        SouthWest_location_lat:"",

        // NorthEast_location_lng:121.5,
        // NorthEast_location_lat:31.4,
        // SouthWest_location_lng:121.4,
        // SouthWest_location_lat:31.5,
      },
      // 时间选择变量
      time_range: [new Date(2016, 9, 10, 7, 0), new Date(2016, 9, 10, 8, 0)],

      // 弹出框是否弹出
      isShow_run:false,
      bikeID:0,
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
      if(this.boundary.NorthEast_location_lng == "" || this.boundary.SouthWest_location_lng == "" ||
         this.boundary.NorthEast_location_lat == "" || this.boundary.SouthWest_location_lat == "")
      {
        alert("请输入正确的坐标值")
      }
      else{
        this.polygonPath[0].lng = this.polygonPath[3].lng = parseFloat(this.boundary.SouthWest_location_lng)
        this.polygonPath[1].lng = this.polygonPath[2].lng = parseFloat(this.boundary.NorthEast_location_lng)
        this.polygonPath[0].lat = this.polygonPath[1].lat = parseFloat(this.boundary.NorthEast_location_lat)
        this.polygonPath[2].lat = this.polygonPath[3].lat = parseFloat(this.boundary.SouthWest_location_lat)
        // console.log(this.polygonPath)
        this.push_multipoints()
      }
      
    },
    // 布置海量点
    push_multipoints(){
        var mapv = require("mapv");
        if(this.mapvLayer != ""){
          this.mapvLayer.hide()
        }
        var node_data = {
            "0":{"x":108.154518, "y":36.643346},
            "1":{"x":121.485124, "y":31.235317},
        };
        var edge_data = [
            // {"source":"1", "target":"0"}
        ]

        var data = [];
        console.log(parseFloat(this.boundary.NorthEast_location_lng))
        console.log(parseFloat(this.boundary.SouthWest_location_lng))
        console.log(parseFloat(this.boundary.SouthWest_location_lat))
        console.log(parseFloat(this.boundary.NorthEast_location_lat))
        this.$axios.post(
                  this.$baseURL+'data/dataByAreaAndTime', 
                  qs.stringify({
                      NorthEast_location: JSON.stringify({"x": parseFloat(this.boundary.NorthEast_location_lng), "y": parseFloat(this.boundary.NorthEast_location_lat)}),
                      SouthWest_location: JSON.stringify({"x": parseFloat(this.boundary.SouthWest_location_lng), "y": parseFloat(this.boundary.SouthWest_location_lat)}),
                      time:               JSON.stringify({"first":this.time_range[0].getHours(),"second": this.time_range[1].getHours()})
                      
                  }),
                  { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
                  )
        .then((response)=>{
                data = []
                
                // alert(response.data)
                console.info(response.data.res);
                var total_num = response.data.res.length
                console.log(total_num)
                for(var i=0; i<total_num; i++){
                  // 导入数据
                  node_data[i*2] = {
                      x: response.data.res[i].start_location_x,
                      y: response.data.res[i].start_location_y
                  }
                  node_data[i*2+1] = {
                      x: response.data.res[i].end_location_x,
                      y: response.data.res[i].end_location_y
                  }
                  edge_data.push(
                      {"source": 2*i, "target": i*2+1}
                  );
                }
                console.log(node_data)
                console.log(edge_data)
                

                var fbundling = mapv.utilForceEdgeBundling()
                        .nodes(node_data)
                        .edges(edge_data);
                
                var results = fbundling();  
                console.log(results.length)
                var data = [];
                var timeData = [];

                for (var i = 0; i < results.length; i++) {
                    var line = results[i];
                    var coordinates = [];
                    for (var j = 0; j < line.length; j++) {
                        coordinates.push([line[j].x, line[j].y]);
                        timeData.push({
                            geometry: {
                                type: 'Point',
                                coordinates: [line[j].x, line[j].y]
                            },
                            count: 1,
                            time: j
                        });
                    }
                    data.push({
                        geometry: {
                            type: 'LineString',
                            coordinates: coordinates
                        }
                    });
                }

                var dataSet = new mapv.DataSet(data);

                var options = {
                    strokeStyle: 'rgba(55, 50, 250, 0.3)',
                    globalCompositeOperation: 'lighter',
                    shadowColor: 'rgba(55, 50, 250, 0.5)',
                    shadowBlur: 10,
                    methods: {
                        click: function (item) {
                        }
                    },
                    lineWidth: 1.0,
                    draw: 'simple'
                }

                this.mapvLayer = new mapv.baiduMapLayer(this.MAP, dataSet, options);

                var dataSet = new mapv.DataSet(timeData);

                var options = {
                    fillStyle: 'rgba(255, 250, 250, 0.9)',
                    globalCompositeOperation: 'lighter',
                    size: 1.5,
                    animation: {
                        type: 'time',
                        stepsRange: {
                            start: 0,
                            end: 100
                        },
                        trails: 1,
                        duration: 5,
                    },
                    draw: 'simple'
                }

                this.mapvLayer = new mapv.baiduMapLayer(this.MAP, dataSet, options);
              })
        .catch((error)=>{
                alert(2)
              // console.info(error);
              });
        // console.log(data)
      },
    // "骑行成功！！"
    ok_run() {
      this.$notify.open({
        type: 'success',
        title: `骑行成功！！！`,
      });
      // 将新增的骑行订单反馈到后台
      this.$axios.post(
            this.$baseURL+'order/addGoingOrder', 
            qs.stringify({
                username:           this.$root.username,
                bikeid:             this.bikeID,
                start_location_x:   this.massage_window_position.lng,
                start_location_y:   this.massage_window_position.lat
            }),
            { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
      )
      .then((response)=>{
             console.log(response)
            })
      .catch((error)=>{
              alert(2)
            // console.info(error);
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

    // 矩形窗口
    updatePolygonPath (e) {
      this.polygonPath = e.target.getPath()
    },
    addPolygonPoint () {
      // this.polygonPath.push({lng: 116.404, lat: 39.915})
    },
    handler({ BMap, map }) {
      map.enableScrollWheelZoom(true); // 开启鼠标滚轮缩放
      map.setMapStyle({
            styleJson: [{
                "featureType": "water",
                "elementType": "all",
                "stylers": {
                    "color": "#044161"
                }
            }, {
                "featureType": "land",
                "elementType": "all",
                "stylers": {
                    "color": "#091934"
                }
            }, {
                "featureType": "boundary",
                "elementType": "geometry",
                "stylers": {
                    "color": "#064f85"
                }
            }, {
                "featureType": "railway",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            }, {
                "featureType": "highway",
                "elementType": "geometry",
                "stylers": {
                    "color": "#004981"
                }
            }, {
                "featureType": "highway",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#005b96",
                    "lightness": 1
                }
            }, {
                "featureType": "highway",
                "elementType": "labels",
                "stylers": {
                    "visibility": "on"
                }
            }, {
                "featureType": "arterial",
                "elementType": "geometry",
                "stylers": {
                    "color": "#004981",
                    "lightness": -39
                }
            }, {
                "featureType": "arterial",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#00508b"
                }
            }, {
                "featureType": "poi",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            }, {
                "featureType": "green",
                "elementType": "all",
                "stylers": {
                    "color": "#056197",
                    "visibility": "off"
                }
            }, {
                "featureType": "subway",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            }, {
                "featureType": "manmade",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            }, {
                "featureType": "local",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            }, {
                "featureType": "arterial",
                "elementType": "labels",
                "stylers": {
                    "visibility": "off"
                }
            }, {
                "featureType": "boundary",
                "elementType": "geometry.fill",
                "stylers": {
                    "color": "#029fd4"
                }
            }, {
                "featureType": "building",
                "elementType": "all",
                "stylers": {
                    "color": "#1a5787"
                }
            }, {
                "featureType": "label",
                "elementType": "all",
                "stylers": {
                    "visibility": "off"
                }
            }, {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": {
                    "color": "#ffffff"
                }
            }, {
                "featureType": "poi",
                "elementType": "labels.text.stroke",
                "stylers": {
                    "color": "#1e1c1c"
                }
            }, {
                "featureType": "administrative",
                "elementType": "labels",
                "stylers": {
                    "visibility": "off"
                }
            },{
                "featureType": "road",
                "elementType": "labels",
                "stylers": {
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