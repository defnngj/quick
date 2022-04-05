<template>
  <div class="module">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模块管理</el-breadcrumb-item>
        <el-breadcrumb-item>用例管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card">
      <!-- 项目/模块树 -->
      <div class="module-tree">
        
        <el-form label-width="80px" label-position="left">
          <el-form-item label="切换项目">
            <el-select v-model="projectId" filterable placeholder="选择项目" @change="selectProject">
              <el-option
                v-for="item in projectOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-form>

        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <div class="node-create">
              <span>模块列表</span>
              <span style="float: right">
                <el-button type="text" size="mini" icon="el-icon-circle-plus-outline" @click="showCreate()">根节点</el-button>
              </span>
            </div>
          </div>

          <el-tree
            :data="moduleData"
            node-key="id"
            :default-expand-all="switchTree"
            :expand-on-click-node="false"
            @node-click="handleNodeClick">
            <span class="custom-tree-node" slot-scope="{ node, data }">
              <span>{{ node.label }}</span>
              <span>
                <el-button
                  type="text"
                  size="mini"
                  @click="() => append(data)"
                  icon="el-icon-circle-plus-outline">
                </el-button>
                <el-button
                  type="text"
                  size="mini"
                  @click="() => remove(node, data)"
                  icon="el-icon-delete">
                </el-button>
              </span>
            </span>
          </el-tree>
        </el-card>
      </div>

      <div class="filter-line">
        <el-button type="primary" @click="createCase()"  size="small">创建</el-button>
      </div>
      <el-breadcrumb separator="/" class="case-breadcrumb">
        <el-breadcrumb-item>{{ currentProjectName }}</el-breadcrumb-item>
        <el-breadcrumb-item>{{ currentModuleName }}</el-breadcrumb-item>

      </el-breadcrumb>
      <!-- 用例列表 -->
      <div class="case-table">
        <!-- 表格 -->
         <el-table :data="caseData" v-loading="caseLoading" border @row-click="editCase">
          <el-table-column prop="name" label="名称" min-width="20%">
          </el-table-column>
          <el-table-column prop="method" label="方法" min-width="10%">
          </el-table-column>
          <el-table-column prop="url" label="URL" min-width="30%">
          </el-table-column>
          <el-table-column prop="module_name" label="模块" min-width="15%">
          </el-table-column>
          <el-table-column prop="create_time" label="创建" min-width="15%">
          </el-table-column>
          <el-table-column fixed="right" label="操作" min-width="10%">
            <template slot-scope="scope">
              <el-button type="danger" size="mini" circle icon="el-icon-delete"
                @click="deleteCase(scope.row)" 
                @click.stop="caseDrawer = false">
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        <!-- 分页 -->
        <!-- <div class="foot-page">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :page-sizes="[5, 10, 20, 50]" 
            :page-size=query.size
            background
            layout="total, sizes, prev, pager, next"
            :total=total>
          </el-pagination>
        </div> -->
      </div>

      <!-- 创建/编辑抽屉 -->
      <el-drawer
        :title="caseTitle"
        :visible.sync="caseDrawer"
        direction="rtl"
        @open="openDrawer"
        @close="closeDrawer">
        <CaseDialog v-if="showCaseInfo" :cid=caseId :mid=moduleId  @cancel="cancelCase"></CaseDialog>
      </el-drawer>
    </el-card>

    <ModuleDialog v-if="showModuleDailog" :moduleid=moduleId :projectid=projectId :parentid=parentId  :parentnode=parentNode  @cancel="cancelModule"></ModuleDialog>
  </div>
</template>

<script>
import ProjectApi from '../../request/project'
import ModuleApi from '../../request/module'
import CaseApi from '../../request/case'
import ModuleDialog from './ModuleDialog.vue'
import CaseDialog from './CaseDialog.vue'

  // let id = 1000;

  export default {
    components: {
      ModuleDialog,
      CaseDialog
    },
    data(){
      return {
        loading: false,
        caseLoading: false,
        currentProjectName: '',
        currentModuleName: '',
        moduleId: 0,
        caseData: [],
        showModuleDailog: false,
        total: 0,
        query: {
          page: 1,
          size: 5,
        },
        projectId: 1,
        parentId: 0,
        parentNode: null,
        projectOptions: [],
        moduleData: [],
        switchTree: false,
        caseDrawer: false,
        showCaseInfo: false,
        direction: 'rtl',
        caseId: 0,
        currentNodeData: null,
        caseTitle: "创建用例",
      }
    },
    created() {
    },
    mounted() {
      this.initProject()
    },
    methods: {
      // 初始化项目列表
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
          this.initModuleTree()
        } else {
          this.$message.error(resp.error.message);
        }
        await this.selectProject(this.projectId)
        this.loading = false
      },

      // 选择一个项目
      async selectProject(val) {
        this.projectId = val
        for(let i = 0; i < this.projectOptions.length; i++) {
          if (this.projectOptions[i].value == val) {
            this.currentProjectName = this.projectOptions[i].label
          } 
        }
        await this.initModuleTree()
      },

      // 初始化模块树
      async initModuleTree() {
        this.loading = true
        const resp = await ModuleApi.getModuleTree(this.projectId)
        if (resp.success == true) {
          this.moduleData = JSON.parse(JSON.stringify(resp.data))
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 添加根节点
      showCreate() {
        this.showModuleDailog = true
      },

      // 展开收起节点
      switchNode() {
        if (this.switchTree === false) {
          this.switchTree = true
        } else {
          this.switchTree = false
        }
      },

      // 显示编辑窗口
      showEdit(row) {
        this.moduleId = row.id
        this.showModuleDailog = true
      },

      // 删除一条模块（节点）信息
      async deleteModule(row) {
        this.$confirm('是否要删除模块?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          ModuleApi.deleteModule(row.id).then(resp =>{
            if (resp.success == true) {
              this.$message.success("删除成功！")
              this.initModuleTree()
            } else {
              this.$message.error("删除失败");
            }
          })
          
        }) .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            }); 
           this.initModuleTree()         
        });      
      },

      // 删除用例
      async deleteCase(row) {
        this.caseDrawer = false
        this.$confirm('是否要删除用例?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          CaseApi.deleteCase(row.id).then(resp =>{
            if (resp.success == true) {
              this.$message.success("删除成功！")
              this.getModuleCaseList(this.moduleId)
            } else {
              this.$message.error("删除失败");
            }
          })
          
        }) .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消删除'
            }); 
           this.initModuleTree()         
        });      
      },

      // 模块子组件的回调
      cancelModule() {
        this.showModuleDailog = false
        this.moduleId = 0
        this.parentId = 0
        this.initModuleTree()
      },

      // 添加子节点
      append(data) {
        this.parentId = data.id
        this.parentNode = data
        this.showModuleDailog = true
      },

      // 删除子节点
      async remove(node, data) {
        await this.deleteModule(data)
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
      },

      //点击节点
      handleNodeClick(data) {
        this.currentNodeData = data
        this.moduleId = data.id
        // this.parent_id = data.id
        this.currentModuleName = data.label
        this.getModuleCaseList(data.id)
      },

      // 初始化用例数据
      async getModuleCaseList(mid) {
        this.caseLoading = true
        const query = { page: 1, size: 5}
        const resp = await ModuleApi.getModuleCases(mid, query)
        if (resp.success == true) {
          this.caseData = resp.data.caseList
          this.total = resp.data.total
        } else {
          this.$message.error(resp.error.message);
        }
        this.caseLoading = false
      },

      createCase() {
        if(this.moduleId == 0) {
          this.$message.error("请选择模块")
          return
        }
        this.caseTitle = "创建用例"
        this.caseId = 0
        this.caseDrawer = true
      },
      
      editCase(row) {
        this.caseTitle = "用例详情"
        this.caseId = row.id
        this.caseDrawer = true
      },

      // 用例子组件的回调
      cancelCase() {
        this.handleNodeClick(this.currentNodeData)
        this.caseDrawer = false
      },

      // 打开抽屉
      openDrawer() {
        this.showCaseInfo = true
      },

      // 关闭抽屉
      closeDrawer() {
        this.showCaseInfo = false
      },

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
.module-tree {
  width: 18%;
  margin-right: 2%;
  height: 600px;
  float: left;
  overflow: auto;
}
.node-create {
  margin-top: 5px;
  margin-bottom: 5px;
  text-align: left;
  height: 28px;
}
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
.module-tree /deep/ .el-tree-node.is-expanded > .el-tree-node__children {
  display: inline;
}

.case-breadcrumb {
  float: left;
  width: 80%;
  margin-bottom: 10px;
}
.case-table {
  float: left;
  width: 80%;
}
</style>