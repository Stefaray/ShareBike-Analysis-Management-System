<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.title" placeholder="Search..." style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-select v-model="listQuery.importance" placeholder="Imp" clearable style="width: 120px" class="filter-item">
        <el-option v-for="item in importanceOptions" :key="item" :label="item" :value="item" />
      </el-select>
      
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        搜索
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        添加
      </el-button>
      <el-button v-waves :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-download" @click="handleDownload">
        导出
      </el-button>
      <!-- <el-checkbox v-model="showReviewer" class="filter-item" style="margin-left:15px;" @change="tableKey=tableKey+1">
        reviewer
      </el-checkbox> -->
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;"
      @sort-change="sortChange"
    >
      <el-table-column label="进行订单ID" prop="id" sortable="custom" align="center" width="150" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.bindid }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户ID" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.userid }}</span>
        </template>
      </el-table-column>
      <el-table-column label="单车ID" width="185px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.bikeid }}</span>
        </template>
      </el-table-column>
      <el-table-column label="开始时间" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.start_time | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      <el-table-column label="起始点经度" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.start_location_x }}</span>
        </template>
      </el-table-column>
      <el-table-column label="起始点纬度" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.start_location_y }}</span>
        </template>
      </el-table-column>


      <el-table-column label="操作" align="center" width="200" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="success" size="mini" @click="handleUpdate(row,$index)">
            结束订单
          </el-button>

        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />
    
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible_end_order">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px; ">

        
        <el-form-item label="结束点经度" prop="location">
          <el-input v-model="temp.end_location_x" type="number"/>
        </el-form-item>
        <el-form-item label="结束点纬度" prop="location">
          <el-input v-model="temp.end_location_y" type="number" />
        </el-form-item>
        
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="end_order_data()">
          确认
        </el-button>
      </div>

    </el-dialog>

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px; ">

        <!-- <el-form-item label="进行订单ID" prop="title">
          <el-input v-model="temp.bindid" />
        </el-form-item> -->
        <el-form-item label="用户名" prop="title">
          <el-input v-model="temp.username" />
        </el-form-item>
        <el-form-item label="单车ID" prop="title">
          <el-input v-model="temp.bikeid" />
        </el-form-item>
        <!-- <el-form-item label="订单起始时间" prop="timestamp">
          <el-date-picker v-model="temp.start_time" type="datetime" placeholder="Please pick a date" />
        </el-form-item> -->
        <el-form-item label="起始点经度" prop="location">
          <el-input v-model="temp.start_location_x" type="number"/>
        </el-form-item>
        <el-form-item label="起始点纬度" prop="location">
          <el-input v-model="temp.start_location_y" type="number" />
        </el-form-item>
        
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确认
        </el-button>
      </div>
    </el-dialog>


    

    <el-dialog :visible.sync="dialogPvVisible" title="Reading statistics">
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel" />
        <el-table-column prop="pv" label="Pv" />
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { fetchList, fetchPv, createArticle, updateArticle, deleteArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import axios from 'axios'
import qs from "qs"

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      row:{},
      msg: "",
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 50,
        importance: '进行订单ID',
        title: '',
        sort: '+id'
      },
      importanceOptions: ['订单ID','单车ID','用户ID','开始时间','结束时间','起始点经度','起始点纬度','结束点经度','结束点纬度'],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        
      },
      dialogFormVisible: false,
      dialogFormVisible_end_order:false,
      dialogStatus: '',
      textMap: {
        update: '编辑订单',
        create: '添加订单'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        // title: [{ required: true, message: '该项不能为空', trigger: 'blur' }],
        // location:[{  type: 'number', required: true, message: '地点不能为空', trigger: 'change' }]
        location:[{  type: 'number' }]

      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
    console.log(1)
    // this.getList()
    
  },
  
  methods: {
    

    getList() {
      
      this.listLoading = true
      
      console.log(this.listQuery.page)
      this.$axios.post(
                this.$baseURL+'order/going_order', 
                qs.stringify({
                    query: JSON.stringify(this.listQuery)
                    }),
                { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
                )
      .then((response)=>{
            //  console.log(response.data.map[0])
            //  this.total_data.push(response.data.map)
             console.log(response)
             this.list = response.data.items
             this.total = response.data.total
             this.listLoading = false

      })
      .catch((error)=>{
              alert(2)
            // console.info(error);
      });



    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {

          this.$axios.post(
                this.$baseURL+'order/addGoingOrder', 
                qs.stringify({
                    data: JSON.stringify(this.temp)
                    }),
                { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
                )
          .then((response)=>{

                console.log(response)
                this.temp.bindid = response.data.bind.bindid
                this.temp.userid = response.data.bind.userid
                this.temp.start_time = response.data.bind.start_time
                console.log(this.temp)
                console.log(this.list)
                this.list.unshift(this.temp)
                this.dialogFormVisible = false
                
                alert('操作成功！')
          })
          .catch((error)=>{
                  alert(2)
                // console.info(error);
          });
        }
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464

         


          this.$axios.post(
                this.$baseURL+'order/order_UPDATE', 
                qs.stringify({
                    data: JSON.stringify(tempData)
                    }),
                { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
                )
          .then((response)=>{
                const index = this.list.findIndex(v => v.id === this.temp.id)
                this.list.splice(index, 1, this.temp)
                this.dialogFormVisible = false
                alert('操作成功！')
          })
          .catch((error)=>{
                  alert(2)
                // console.info(error);
          });

        }
      })
    },
    handleDelete(row, index) {

          this.$axios.post(
                this.$baseURL+'order/order_DELETE', 
                qs.stringify({
                    data: JSON.stringify(row)
                    }),
                { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
          )
          .then((response)=>{
                this.list.splice(index, 1)
                alert('操作成功！')
          })
          .catch((error)=>{
                  alert(2)
                // console.info(error);
          });


      
    },
    end_order_data(){
        this.$axios.post(
                this.$baseURL+'order/endGoingOrder', 
                qs.stringify({
                    data: JSON.stringify(this.temp)
                    }),
                { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
          )
          .then((response)=>{
                this.list.splice(this.temp.index, 1)
                this.dialogFormVisible_end_order = false
                alert('操作成功！')
                
          })
          .catch((error)=>{
                  alert(2)
                // console.info(error);
          });
    },

    // --------------------------------------------------
    handleUpdate(row,index) {
      this.temp = Object.assign({}, row) // copy obj
      // console.log(row)
      this.temp.index = index
      console.log(this.temp)
      // console.log(index)
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible_end_order = true
      // this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    // --------------------------------------------------

    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作Success',
        type: 'success'
      })
      row.status = status
    },
    sortChange(data) {
      const { prop, order } = data
      if (prop === 'id') {
        this.sortByID(order)
      }
    },
    sortByID(order) {
      if (order === 'ascending') {
        this.listQuery.sort = '+id'
      } else {
        this.listQuery.sort = '-id'
      }
      this.handleFilter()
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    
    
    
    
    handleFetchPv(pv) {
      fetchPv(pv).then(response => {
        this.pvData = response.data.pvData
        this.dialogPvVisible = true
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
        const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
        const data = this.formatJson(filterVal)
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: 'table-list'
        })
        this.downloadLoading = false
      })
    },
    formatJson(filterVal) {
      return this.list.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    }
  }
}
</script>
