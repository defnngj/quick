<template>
  <div class="module">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模块管理</el-breadcrumb-item>
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

        <div class="node-create">
          <span style="float: right">
            <el-button type="text" plain size="mini" icon="el-icon-circle-plus-outline" @click="showCreate()">根节点</el-button>
          </span>
        </div>

        <el-tree
          :data="moduleData"
          show-checkbox
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
      </div>

      <div class="filter-line">
        <el-button type="primary" @click="showDebug()"  size="small">创建</el-button>
      </div>
      <el-breadcrumb separator="/" class="case-breadcrumb">
        <el-breadcrumb-item>{{ currentProjectName }}</el-breadcrumb-item>
        <el-breadcrumb-item>... {{ currentModuleName }}</el-breadcrumb-item>

      </el-breadcrumb>
      <!-- 用例列表 -->
      <div class="case-table">
        <!-- 表格 -->
         <el-table :data="caseData" v-loading="caseLoading" border>
          <el-table-column prop="name" label="名称" min-width="20%">
          </el-table-column>
          <el-table-column prop="method" label="方法" min-width="10%">
          </el-table-column>
          <el-table-column prop="url" label="URL" min-width="30%">
          </el-table-column>
          <el-table-column prop="module_name" label="模块" min-width="15%">
          </el-table-column>
          <el-table-column prop="create_time" label="创建" min-width="20%">
          </el-table-column>
          <el-table-column fixed="right" label="操作" width="100">
            <template slot-scope="scope">
              <el-button @click="showEdit(scope.row)" type="primary" size="mini" circle icon="el-icon-edit"></el-button>
              <el-button @click="deleteModule(scope.row)" type="danger" size="mini" circle icon="el-icon-delete"></el-button>
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
        title="创建用例"
        :visible.sync="caseDrawer"
        direction="rtl">
        <CaseDebug :cid=caseId></CaseDebug>
      </el-drawer>
    </el-card>

    <ModuleDialog v-if="showDailog" :moduleid=moduleId :projectid=projectId :parentid=parentId  :parentnode=parentNode  @cancel="cancelModule"></ModuleDialog>
  </div>
</template>

<script>
import ProjectApi from '../../request/project'
import ModuleApi from '../../request/module'
import ModuleDialog from './ModuleDialog.vue'
import CaseDebug from './CaseDebug.vue'

  let id = 1000;

  export default {
    components: {
      ModuleDialog,
      CaseDebug
    },
    data(){
      return {
        loading: false,
        caseLoading: false,
        currentProjectName: '',
        currentModuleName: '',
        moduleId: 0,
        caseData: [],
        showDailog: false,
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
        direction: 'rtl',
        caseId: 0
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
        this.showDailog = true
      },

      // 展开收起节点
      switchNode() {
        console.log("switchNode", this.switchTree)
        if (this.switchTree === false) {
          this.switchTree = true
        } else {
          this.switchTree = false
        }
      },

      // 显示编辑窗口
      showEdit(row) {
        this.moduleId = row.id
        this.showDailog = true
      },

      // 删除一条项目信息
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

      // 子组件的回调
      cancelModule() {
        this.showDailog = false
        this.moduleId = 0
        this.parentId = 0
        this.initModuleTree()
      },

      // 添加子节点
      append(data) {
        console.log("data", data, id)
        this.parentId = data.id
        this.parentNode = data
        this.showDailog = true
        // const newChild = { id: id++, label: 'testtest', children: [] };
        // if (!data.children) {
        //   this.$set(data, 'children', []);
        // }
        // data.children.push(newChild);
      },

      // 删除子节点
      async remove(node, data) {
        console.log("node", node)
        console.log("data", data.id)
        await this.deleteModule(data)
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.id === data.id);
        children.splice(index, 1);
      },

      //点击节点
      handleNodeClick(data) {
        console.log("click node", data)
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

      showDebug() {
        this.caseDrawer = true
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