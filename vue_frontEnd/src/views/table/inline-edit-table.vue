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
      <el-table-column label="用户ID" prop="id" sortable="custom" align="center" width="100" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.userid }}</span>
        </template>
      </el-table-column>
      <el-table-column label="用户名" min-width="110px">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.title }}</span>
          <el-tag>{{ row.username }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="注册时间" width="150px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.register_date | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="电话" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.phone }}</span>
        </template>
      </el-table-column>

      <el-table-column label="邮箱" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.email }}</span>
        </template>
      </el-table-column>

      <el-table-column label="余额" width="110px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.money }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="230" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button v-if="row.identity=='1'" size="mini" type="success" @click="handleModifyStatus(row,'0')">
            用户
          </el-button>
          <el-button v-else-if="row.identity=='0'" size="mini" @click="handleModifyStatus(row,'1')">
            管理员
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" @click="handleDelete(row,$index)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="120px" style="width: 400px; margin-left:50px; ">
        <!-- <el-form-item label="订单ID" prop="title">
          <el-input v-model="temp.orderid" />
        </el-form-item> -->
        
        <!-- <el-form-item label="用户ID" prop="title">
          <el-input v-model="temp.userid" />
        </el-form-item> -->
        <el-form-item label="用户名" prop="title">
          <el-input v-model="temp.username" />
        </el-form-item>
        <el-form-item label="密码" prop="location">
          <el-input v-model="temp.password" type="number" />
        </el-form-item>
        <el-form-item label="电话" prop="location">
          <el-input v-model="temp.phone" type="number"/>
        </el-form-item>
        <el-form-item label="邮箱" prop="location">
          <el-input v-model="temp.email"  />
        </el-form-item>
        <el-form-item label="余额" prop="location">
          <el-input v-model="temp.money" type="number" />
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
import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
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
      row:{
        status:'1'
      },
      msg: "",
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 50,
        importance: '用户ID',
        title: '',
        // type: undefined,
        sort: '+id'
      },
      importanceOptions: ['用户ID','用户名','注册时间','电话','邮箱','余额','用户类别'],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        password:123456
      },
      dialogFormVisible: false,
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
        // title: [{ required: true, message: 'title is required', trigger: 'blur' }],
        location:[{  type: 'number' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    

    getList() {
      
      this.listLoading = true
      
      console.log(this.listQuery.page)
      this.$axios.post(
                this.$baseURL+'user/order_table', 
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
          // this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          // this.temp.author = 'vue-element-admin'
          // alert(111)
          //替换所有的换行符
          // this.temp.track = this.temp.track.replace(/\r\n/g,"#")
          // this.temp.track = this.temp.track.replace(/\n/g,"#");
          // //替换所有的空格（中文空格、英文空格都会被替换）
          // this.temp.track = this.temp.track.replace(/\s/g,"#");

          this.$axios.post(
                this.$baseURL+'user/order_ADD', 
                qs.stringify({
                    data: JSON.stringify(this.temp)
                    }),
                { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
                )
          .then((response)=>{

                console.log(response)
                this.temp.userid = response.data.userid
                console.log('temp:')
                console.log(this.temp)
                console.log(this.list)
                this.list.unshift(this.temp)
                this.dialogFormVisible = false
                this.temp.register_date = new Date();
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
                this.$baseURL+'user/order_UPDATE', 
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
      
          // console.log(row)
          // deleteArticle(row).then(() => {
          //       this.$notify({
          //         title: 'Success',
          //         message: 'Delete Successfully',
          //         type: 'success',
          //         duration: 2000
          //       })
          //       this.list.splice(index, 1)
          // })
  

          this.$axios.post(
                this.$baseURL+'user/order_DELETE', 
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
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleModifyStatus(row, identity) {
      
      this.$axios.post(
                this.$baseURL+'user/user_SWITCH', 
                qs.stringify({
                    data: JSON.stringify(row)
                    }),
                { headers:{ 'Content-Type':'application/x-www-form-urlencoded' }},
          )
          .then((response)=>{
                this.$message({
                  message: '操作Success',
                  type: 'success'
                })
                if(row.identity == '0'){
                  row.identity = '1'
                }
                else{
                  row.identity = '0'
                }
                // row.identity = identity
                // alert('操作成功！')
          })
          .catch((error)=>{
                  alert(2)
                // console.info(error);
          });
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
        identity:'1',
        // status: 'user',
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
