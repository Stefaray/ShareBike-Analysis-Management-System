<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import adminDashboard from './admin'
import editorDashboard from './editor'
import axios from 'axios'
import qs from "qs"

export default {
  name: 'Dashboard',
  components: { adminDashboard, editorDashboard },
  data() {
    return {
      currentRole: 'adminDashboard'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (!this.roles.includes('admin')) {
      this.currentRole = 'editorDashboard'
    }
    this.$axios.post(
                  this.$baseURL+'data/queryDayChangeByArea', 
                  qs.stringify({
                      // location: JSON.stringify({"x":parseFloat(this.bike_around.center_lng),"y":parseFloat(this.bike_around.center_lat)}),
                      NorthEast_location: JSON.stringify({"x":121.6,"y":31.23}),
                      SouthWest_location: JSON.stringify({"x":121.33,"y":31.33}),
                      date:               JSON.stringify({"first":"2016-08-01","second": "2016-08-31"})

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
  }
}
</script>
