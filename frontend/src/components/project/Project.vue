<template>
  <div class="project">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card" shadow="never">
      <div class="filter-line">
        <el-button cy-data="create-project" type="primary" @click="showCreate()">创建</el-button>
      </div>
      <el-row>
      <div v-for="(item, index) in tableData" :key="index">
        <el-col :span="7" class="project-card">
          <el-card class="box-card">
            <el-avatar shape="square" :size="100" fit="fill" :src="item.image"></el-avatar>
            <div slot="header" class="clearfix">
              <span>【{{item.id}}】{{item.name}} </span>
              <span style="float: right; padding: 3px 0">
                <el-dropdown style="left: 5px;">
                  <i class="el-icon-setting" style="margin-right: 15px"></i>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item>
                      <el-button cy-data="edit-project" @click="showEdit(item.id)" type="text" size="mini">编辑</el-button>
                    </el-dropdown-item>
                    <el-dropdown-item>
                      <el-button cy-data="delete-project" @click="deleteProject(item.id)" type="text">删除</el-button>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </span>
            </div>
            <div>
              {{item.describe}}
            </div>
          </el-card>
        </el-col>
      </div>
      </el-row>

      <!-- 分页 -->
      <div class="foot-page">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[5, 10, 20, 50]" 
          :page-size=query.size
          background
          layout="total, sizes, prev, pager, next"
          :total=total>
        </el-pagination>
      </div>
    </el-card>
    <projectDialog v-if="showDailog" :pid=projectId @cancel="cancelProject"></projectDialog>
  </div>
</template>

<script>
import ProjectApi from '../../request/project_v2'
import projectDialog from '../project/projectDialog'

  export default {
    components: {
      projectDialog
    },
    data(){
      return {
        loading: false,
        projectId: 0,
        tableData: [],
        showDailog: false,
        total: 0,
        query: {
          page: 1,
          size: 6,
        },
      }
    },
    created() {
    },
    mounted() {
      this.initProject()
    },
    methods: {
      async initProject() {
        this.loading = true
        const resp = await ProjectApi.getProjects(this.query)
        if (resp.success == true) {
          this.tableData = resp.data.projectList
          this.total = resp.data.total
          
          for(let i = 0; i < this.tableData.length; i++) {
            if (this.tableData[i].image == null) {
              this.tableData[i].image = 'static/images/default.jpeg'
            } else {
              this.tableData[i].image = 'static/images/' + this.tableData[i].image
            }
          }

        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 显示创建窗口
      showCreate() {
        this.showDailog = true
      },

      // 显示编辑窗口
      showEdit(pid) {
        this.projectId = pid
        this.showDailog = true
      },

      // 删除一条项目信息
      async deleteProject(pid) {
        const resp = await ProjectApi.deleteProject(pid)
        if (resp.success == true) {
          this.$message.success("删除成功！")
          this.initProject()
        } else {
          this.$message.error("删除失败");
        }

      },
      // 子组件的回调
      cancelProject() {
        this.showDailog = false
        this.projectId = 0
        this.initProject()
      },

      // 修改每页显示个数
      handleSizeChange(val) {
        this.query.size = val
        this.initProject()
      },

      // 点给第几页
      handleCurrentChange(val) {
        this.query.page = val
        this.initProject()
      }

    }

  }
</script>

<style scoped>
.filter-line {
  height: 50px;
  text-align: left;
}
.foot-page {
  margin-top: 20px;
    float: right;
    margin-bottom: 20px;
}
.project-card {
  margin-left: 15px;
  margin-right: 15px;
  margin-top: 15px;
  margin-bottom: 15px
}

</style>