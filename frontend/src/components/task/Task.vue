<template>
  <div class="task">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>任务管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card">
      <div class="filter-line">
        <span>选择项目 </span>
        <el-select v-model="projectId" size="small" filterable placeholder="请选择项目" @change="selectProject">
          <el-option
            v-for="item in projectOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <span style="margin-left: 20px;">
          <el-button type="primary" size="small" @click="showCreate()">创建</el-button>
        </span>
      </div>
      <!-- 表格 -->
      <el-table :data="tableData"
          v-loading="loading"
          element-loading-text="拼命加载中"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)"
          style="width: 100%">
        <el-table-column prop="name" label="名称" min-width="20%">
        </el-table-column>
        <el-table-column prop="describe" label="描述" min-width="30%">
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="15%">
          <template slot-scope="scope">
            <span v-if="scope.row.status === 0">
              <el-tag>未执行</el-tag>
            </span>
            <span v-else-if="scope.row.status === 1">
              <el-tag>执行中</el-tag>
            </span>
            <span v-else-if="scope.row.status === 2">
              <el-tag>已完成</el-tag>
            </span>
            <span v-else>
              <el-tag>{{scope.row.status}}</el-tag>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="30%">
        </el-table-column>
        <el-table-column fixed="right" label="任务" width="50">
          <template slot-scope="scope">
            <el-button @click="runTask(scope.row)" type="primary" size="mini" circle icon="el-icon-time"></el-button>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="editTask(scope.row)" type="primary" size="mini" circle icon="el-icon-edit"></el-button>
            <el-button @click="deleteTask(scope.row)" type="danger" size="mini" circle icon="el-icon-delete"></el-button>
          </template>
        </el-table-column>
      </el-table>
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
    <TaskDialog v-if="showDailog" :tid=taskId :pid=projectId @cancel="cancelTask"></TaskDialog>
  </div>
</template>

<script>
import ProjectApi from '../../request/project'
import TaskApi from '../../request/task'
import TaskDialog from './TaskDialog.vue'

  export default {
    components: {
      TaskDialog
    },
    data() {
      return {
        loading: false,
        projectId: 1,
        projectName: '',
        projectOptions: [],
        taskId: 0,
        tableData: [],
        showDailog: false,
        total: 0,
        query: {
          page: 1,
          size: 5,
        },
        taskHeartbeat:null,
        name: 'hello',
      }
    },
    created() {
      this.initProject()
    },
    mounted() {
      this.initTask()
      // this.taskHeartbeat = setInterval(() => {
      //   this.initTask()
      // }, 5000);
    },
    destroyed() {
      // 销毁时候清除定时器
      clearInterval(this.taskHeartbeat);
    },
    methods: {
      async initProject() {
        this.loading = true
        const pQuery = {
          page: 1,
          size: 1000,
        }
        const resp = await ProjectApi.getProjects(pQuery)
        if (resp.success == true) {
          const projectData = resp.data.projectList
          this.projectOptions = []
          for (let i = 0; i < projectData.length; i++) {
            this.projectOptions.push({
              value: projectData[i].id,
              label: projectData[i].name
            })
          }
          this.projectId = this.projectOptions[0].value
          // this.initModuleTree()
        } else {
          this.$message.error(resp.error.message);
        }
        await this.selectProject(this.projectId)
        this.loading = false
      },

      async initTask() {
        this.loading = true
        this.query.project = this.projectId
        const resp = await TaskApi.getTasks(this.query)
        if (resp.success == true) {
          this.tableData = resp.data.taskList
          this.total = resp.data.total
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 选择一个项目
      async selectProject(val) {
        this.projectId = val
        for(let i = 0; i < this.projectOptions.length; i++) {
          if (this.projectOptions[i].value == val) {
            this.projectName = this.projectOptions[i].label
            this.projectId = this.projectOptions[i].value
          }
        }
        await this.initTask()
      },
      // 显示创建窗口
      showCreate() {
        this.showDailog = true
      },

      // 显示编辑窗口
      editTask(row) {
        this.taskId = row.id
        this.showDailog = true
      },

      // 删除一条任务信息
      async deleteTask(row) {
        const resp = await TaskApi.deleteTask(row.id)
        if (resp.success == true) {
          this.$message.success("删除成功！")
          this.initTask()
        } else {
          this.$message.error("删除失败");
        }
      },

      
      // 子组件的回调
      cancelTask() {
        this.showDailog = false
        this.taskId = 0
        this.initTask()
      },
      
      // 删除一条任务信息
      async runTask(row) {
        const resp = await TaskApi.runTask(row.id)
        if (resp.success == true) {
          this.$message.success("运行成功！")
          this.initTask()
        } else {
          this.$message.error("运行失败");
        }
      },

      // 修改每页显示个数
      handleSizeChange(val) {
        this.query.size = val
        this.initTask()
      },

      // 点给第几页
      handleCurrentChange(val) {
        this.query.page = val
        this.initTask()
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

</style>
